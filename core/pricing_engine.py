"""
Pricing Engine for Babbitt Quote Generator
Centralized pricing calculations and business rules
"""

from typing import Dict, List, Optional, Any, Tuple
from database.db_manager import DatabaseManager
from core.spare_parts_manager import SparePartsManager
from utils.logger import get_logger

logger = get_logger(__name__)

class PricingEngine:
    """
    Main pricing calculation engine
    Handles all pricing logic and business rules
    """
    
    def __init__(self):
        """Initialize pricing engine with database connection"""
        self.db = DatabaseManager()
        self.spare_parts_manager = SparePartsManager(self.db)
        
    def calculate_complete_pricing(self, 
                                 model_code: str, 
                                 voltage: str, 
                                 material_code: str, 
                                 probe_length: float, 
                                 option_codes: Optional[List[str]] = None, 
                                 insulator_code: Optional[str] = None, 
                                 connection_info: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Calculate complete pricing for a configuration
        
        This is the main entry point for all pricing calculations
        
        Args:
            model_code: Product model (LS2000, LS2100, etc.)
            voltage: Voltage specification (115VAC, 24VDC, etc.)
            material_code: Probe material code (S, H, TS, etc.)
            probe_length: Probe length in inches
            option_codes: List of option codes (XSP, VR, etc.)
            insulator_code: Insulator material code (TEF, U, etc.)
            connection_info: Process connection details
            
        Returns:
            Dict containing detailed pricing breakdown
        """
        import math
        
        try:
            # Round up any non-whole number lengths for pricing
            original_length = probe_length
            probe_length = math.ceil(probe_length)
            
            logger.info(f"Calculating pricing for {model_code}-{voltage}-{material_code}-{probe_length}\"")
            
            # Initialize result structure
            pricing_result = {
                'base_price': 0.0,
                'length_cost': 0.0,
                'length_surcharge': 0.0,
                'option_cost': 0.0,
                'insulator_cost': 0.0,
                'connection_cost': 0.0,
                'total_price': 0.0,
                'breakdown': [],
                'option_details': [],
                'warnings': [],
                'calculation_notes': [],
                'success': True,
                'original_length': original_length,
                'pricing_length': probe_length
            }
            
            # Add note if length was rounded up
            if original_length != probe_length:
                pricing_result['calculation_notes'].append(f"Length rounded up from {original_length:.1f}\" to {probe_length:.0f}\" for pricing")
                pricing_result['breakdown'].append(f"Length rounded up: {original_length:.1f}\" → {probe_length:.0f}\"")
            
            
            # 1. Calculate base price (model + material + voltage)
            base_price_result = self._calculate_base_price(model_code, voltage, material_code)
            pricing_result['base_price'] = base_price_result['total']
            pricing_result['breakdown'].extend(base_price_result['breakdown'])
            
            # 2. Calculate length-based pricing
            length_result = self._calculate_length_pricing(material_code, model_code, probe_length)
            pricing_result['length_cost'] = length_result['length_cost']
            pricing_result['length_surcharge'] = length_result['surcharge']
            pricing_result['breakdown'].extend(length_result['breakdown'])
            
            # 3. Calculate option pricing
            if option_codes:
                option_result = self._calculate_option_pricing(option_codes, probe_length, model_code)
                pricing_result['option_cost'] = option_result['total_cost']
                pricing_result['option_details'] = option_result['options']
                pricing_result['breakdown'].extend(option_result['breakdown'])
            
            # 4. Calculate insulator pricing
            if insulator_code:
                insulator_result = self._calculate_insulator_pricing(insulator_code, material_code, model_code)
                pricing_result['insulator_cost'] = insulator_result['cost']
                pricing_result['breakdown'].extend(insulator_result['breakdown'])
            
            # 5. Calculate process connection pricing
            if connection_info:
                connection_result = self._calculate_connection_pricing(connection_info)
                pricing_result['connection_cost'] = connection_result['cost']
                pricing_result['breakdown'].extend(connection_result['breakdown'])
            
            # 6. Calculate total
            total_price = (
                pricing_result['base_price'] + 
                pricing_result['length_cost'] + 
                pricing_result['length_surcharge'] + 
                pricing_result['option_cost'] + 
                pricing_result['insulator_cost'] + 
                pricing_result['connection_cost']
            )
            
            pricing_result['total_price'] = total_price
            pricing_result['breakdown'].append(f"TOTAL: ${total_price:.2f}")
            
            # Add calculation summary
            pricing_result['calculation_notes'].append(f"Pricing calculated for {model_code} configuration")
            pricing_result['calculation_notes'].append(f"Base model price includes {material_code} material")
            if probe_length != 10.0:  # Assuming 10" is standard
                pricing_result['calculation_notes'].append(f"Length adjustments for {probe_length}\" probe")
            
            # Log successful calculation
            logger.info(f"Pricing calculated successfully: ${total_price:.2f}")
            
            return pricing_result
            
        except Exception as e:
            logger.error(f"Pricing calculation failed for {model_code}: {str(e)}")
            return {
                'base_price': 0.0,
                'length_cost': 0.0,
                'length_surcharge': 0.0,
                'option_cost': 0.0,
                'insulator_cost': 0.0,
                'connection_cost': 0.0,
                'total_price': 0.0,
                'breakdown': [f"ERROR: {str(e)}"],
                'option_details': [],
                'warnings': [f"Pricing calculation failed: {str(e)}"],
                'calculation_notes': [],
                'success': False,
                'error': str(e)
            }
    
    def _calculate_base_price(self, model_code: str, voltage: str, material_code: str) -> Dict[str, Any]:
        """Calculate base price including model, voltage, and material adders"""
        result = {
            'total': 0.0,
            'breakdown': [],
            'components': {}
        }
        
        try:
            # Get model base price
            model_info = self.db.get_model_info(model_code)
            if model_info:
                model_price = model_info['base_price']
                result['total'] += model_price
                result['components']['model'] = model_price
                result['breakdown'].append(f"Base Model ({model_code}): ${model_price:.2f}")
            
            # Add material price adder
            material_info = self.db.get_material_info(material_code)
            if material_info:
                material_adder = material_info['base_price_adder']
                if material_adder > 0:
                    result['total'] += material_adder
                    result['components']['material'] = material_adder
                    result['breakdown'].append(f"Material Adder ({material_code}): ${material_adder:.2f}")
            
            # Add voltage price adder (if any)
            voltage_info = self.db.execute_query(
                "SELECT * FROM voltages WHERE model_family = ? AND voltage = ?", 
                (model_code, voltage)
            )
            if voltage_info:
                voltage_adder = voltage_info[0].get('price_adder', 0.0)
                if voltage_adder > 0:
                    result['total'] += voltage_adder
                    result['components']['voltage'] = voltage_adder
                    result['breakdown'].append(f"Voltage Adder ({voltage}): ${voltage_adder:.2f}")
            
        except Exception as e:
            result['breakdown'].append(f"Base price calculation error: {str(e)}")
            logger.error(f"Base price calculation failed: {str(e)}")
        
        return result
    
    def _calculate_length_pricing(self, material_code: str, model_family: str, probe_length: float) -> Dict[str, Any]:
        """Calculate length-based pricing including surcharges"""
        result = {
            'length_cost': 0.0,
            'surcharge': 0.0,
            'breakdown': []
        }
        
        try:
            # Get model info to determine model base length
            model_info = self.db.get_model_info(model_family)
            if not model_info:
                return result
            
            model_base_length = model_info['base_length']
            
            # Get material info for material base length and pricing
            material_info = self.db.get_material_info(material_code)
            if not material_info:
                return result
            
            # Calculate length cost based on material type
            if material_info['length_adder_per_foot'] > 0:
                # Per-foot materials use stepped calculation
                length_cost = self._calculate_stepped_foot_pricing(
                    model_base_length, 
                    probe_length, 
                    material_info['length_adder_per_foot']
                )
                
                if length_cost > 0:
                    # Calculate how many foot adders were applied
                    num_adders = self._count_foot_adders(model_base_length, probe_length)
                    result['breakdown'].append(f"Length Cost ({num_adders} foot adders @ ${material_info['length_adder_per_foot']:.0f}/ft): ${length_cost:.2f}")
                    
            elif material_info['length_adder_per_inch'] > 0:
                # Per-inch materials use continuous calculation from material base length
                material_base_length = material_info['material_base_length']
                extra_length = max(0, probe_length - material_base_length)
                
                if extra_length > 0:
                    length_cost = extra_length * material_info['length_adder_per_inch']
                    result['breakdown'].append(f"Length Cost ({extra_length:.1f}\" extra @ ${material_info['length_adder_per_inch']:.2f}/in): ${length_cost:.2f}")
                else:
                    length_cost = 0.0
            else:
                length_cost = 0.0
            
            result['length_cost'] = length_cost
            
            # Calculate nonstandard length surcharge
            if (material_info['nonstandard_length_surcharge'] > 0 and 
                probe_length > 96.0):  # Nonstandard threshold for most materials
                surcharge = material_info['nonstandard_length_surcharge']
                result['surcharge'] = surcharge
                result['breakdown'].append(f"Nonstandard Length Surcharge (>96\"): ${surcharge:.2f}")
            
        except Exception as e:
            result['breakdown'].append(f"Length pricing error: {str(e)}")
            logger.error(f"Length pricing calculation failed: {str(e)}")
        
        return result
    
    def _calculate_stepped_foot_pricing(self, model_base_length: float, probe_length: float, adder_per_foot: float) -> float:
        """
        Calculate stepped foot pricing based on foot thresholds.
        For 10" base models: first adder at 11", then 24", 36", 48", etc.
        For 6" base models: first adder at 7", then 18", 30", 42", etc. (every 12" from base)
        """
        if probe_length <= model_base_length:
            return 0.0
        
        # Calculate foot thresholds based on model base length
        if model_base_length == 10.0:
            # For 10" base: thresholds at 11", 25", 37", 49", 61", 73", 85", 97", 109", 121"...
            thresholds = [11.0]
            next_threshold = 25.0
            while next_threshold <= 121.0:  # Reasonable upper limit
                thresholds.append(next_threshold)
                next_threshold += 12.0
        elif model_base_length == 6.0:
            # For 6" base (FS10000): first adder at 7", then every 12" from base: 18", 30", 42", 54"...
            thresholds = [7.0]  # First adder at base + 1"
            next_threshold = model_base_length + 12.0  # Start at 18" (6" + 12")
            while next_threshold <= 120.0:  # Reasonable upper limit
                thresholds.append(next_threshold)
                next_threshold += 12.0  # Continue every 12": 30", 42", 54", etc.
        else:
            # For other base lengths, use simple 12" increments from base + 1"
            thresholds = [model_base_length + 1.0]
            next_threshold = model_base_length + 12.0
            while next_threshold <= model_base_length + 120.0:
                thresholds.append(next_threshold)
                next_threshold += 12.0
        
        # Count how many thresholds the probe length exceeds
        num_adders = 0
        for threshold in thresholds:
            if probe_length >= threshold:
                num_adders += 1
            else:
                break
        
        return num_adders * adder_per_foot
    
    def _count_foot_adders(self, model_base_length: float, probe_length: float) -> int:
        """Count how many foot adders are applied for a given probe length"""
        if probe_length <= model_base_length:
            return 0
        
        # Use same logic as _calculate_stepped_foot_pricing but just count
        if model_base_length == 10.0:
            thresholds = [11.0, 25.0, 37.0, 49.0, 61.0, 73.0, 85.0, 97.0, 109.0, 121.0]
        elif model_base_length == 6.0:
            # For 6" base: first adder at 7", then every 12" from base: 18", 30", 42", 54"...
            thresholds = [7.0, 18.0, 30.0, 42.0, 54.0, 66.0, 78.0, 90.0, 102.0, 114.0]
        else:
            thresholds = [model_base_length + 1.0]
            next_threshold = model_base_length + 12.0
            while next_threshold <= model_base_length + 120.0:
                thresholds.append(next_threshold)
                next_threshold += 12.0
        
        num_adders = 0
        for threshold in thresholds:
            if probe_length >= threshold:
                num_adders += 1
            else:
                break
        
        return num_adders
    
    def _calculate_od_option_foot_pricing(self, model_base_length: float, probe_length: float, adder_per_foot: float) -> float:
        """
        Calculate 3/4"OD option stepped foot pricing with strict 12" increments.
        For 3/4"OD: 11" = first adder, 22" = second adder, 34" = third adder, etc.
        Every 12" from model base length + 1".
        """
        if probe_length <= model_base_length:
            return 0.0
        
        # Calculate thresholds: base + 1", base + 12", base + 24", base + 36", etc.
        thresholds = []
        for i in range(10):  # Generate up to 10 thresholds (reasonable limit)
            if i == 0:
                threshold = model_base_length + 1.0  # First threshold at base + 1"
            else:
                threshold = model_base_length + (12.0 * i)  # Subsequent thresholds every 12"
            
            if threshold > 120.0:  # Stop at reasonable upper limit
                break
            thresholds.append(threshold)
        
        # Count how many thresholds the probe length exceeds
        num_adders = 0
        for threshold in thresholds:
            if probe_length >= threshold:
                num_adders += 1
            else:
                break
        
        return num_adders * adder_per_foot
    
    def _calculate_option_pricing(self, option_codes: List[str], probe_length: float, model_code: Optional[str] = None) -> Dict[str, Any]:
        """Calculate pricing for all options"""
        result = {
            'total_cost': 0.0,
            'options': [],
            'breakdown': []
        }
        
        try:
            for code in option_codes:
                option_cost = 0.0
                option_name = code
                
                # Check for bent probe degree format (e.g., 90DEG, 45DEG)
                if code.endswith('DEG'):
                    try:
                        degree = int(code[:-3])
                        if 0 <= degree <= 180:
                            option_cost = 50.0  # Fixed price for bent probe
                            option_name = f'Bent Probe ({degree}°)'
                            result['options'].append({
                                'code': code,
                                'name': option_name,
                                'price': option_cost,
                                'price_type': 'fixed'
                            })
                    except ValueError:
                        pass
                
                elif code == '3/4"OD':
                    # Special handling for 3/4" OD probe: $175 base + $175 per foot in strict 12" increments
                    # 11" = 1st adder, 22" = 2nd adder, 34" = 3rd adder, etc.
                    model_info = self.db.get_model_info(model_code) if model_code else None
                    model_base_length = model_info['base_length'] if model_info else 10.0  # Default to 10" if not found
                    
                    base_cost = 175.0
                    # Use OD-specific stepped foot pricing: strict 12" increments from base + 1"
                    stepped_foot_cost = self._calculate_od_option_foot_pricing(model_base_length, probe_length, 175.0)
                    option_cost = base_cost + stepped_foot_cost
                    option_name = '3/4" Diameter Probe'
                    
                    # Calculate how many foot adders were applied for breakdown
                    num_adders = int(stepped_foot_cost / 175.0) if stepped_foot_cost > 0 else 0
                    
                    result['options'].append({
                        'code': code,
                        'name': option_name,
                        'price': option_cost,
                        'price_type': 'base_plus_stepped_foot',
                        'base_cost': base_cost,
                        'stepped_foot_cost': stepped_foot_cost,
                        'num_foot_adders': num_adders,
                        'model_base_length': model_base_length
                    })
                
                else:
                    # Regular option from database
                    option_info = self.db.get_option_info(code)
                    if option_info:
                        option_cost = option_info['price']
                        option_name = option_info['name']
                        result['options'].append({
                            'code': code,
                            'name': option_name,
                            'price': option_cost,
                            'price_type': option_info['price_type']
                        })
                
                if option_cost > 0:
                    result['total_cost'] += option_cost
                    result['breakdown'].append(f"Option {code} ({option_name}): ${option_cost:.2f}")
            
        except Exception as e:
            result['breakdown'].append(f"Option pricing error: {str(e)}")
            logger.error(f"Option pricing calculation failed: {str(e)}")
        
        return result
    
    def _calculate_insulator_pricing(self, insulator_code: str, material_code: str, model_code: Optional[str] = None) -> Dict[str, Any]:
        """Calculate insulator pricing with material-specific rules"""
        result = {
            'cost': 0.0,
            'breakdown': []
        }
        
        try:
            insulator_info = self.db.get_insulator_info(insulator_code)
            if insulator_info:
                cost = insulator_info['price_adder']
                
                # Special rule: If probe material is 'h', teflon insulation adder is not applied
                if material_code.upper() == 'H' and insulator_code.upper() == 'TEF':
                    result['cost'] = 0.0
                    result['breakdown'].append(f"Insulator ({insulator_info['name']}): $0.00 (Not applied - Material H)")
                # Special rule: If base insulator is Teflon, teflon insulation adder is not applied
                elif model_code and insulator_code.upper() == 'TEF':
                    model_info = self.db.get_model_info(model_code)
                    if model_info and model_info.get('default_insulator', '').upper() == 'TEF':
                        result['cost'] = 0.0
                        result['breakdown'].append(f"Insulator ({insulator_info['name']}): $0.00 (Not applied - Base insulator is Teflon)")
                elif cost > 0:
                    result['cost'] = cost
                    result['breakdown'].append(f"Insulator ({insulator_info['name']}): ${cost:.2f}")
            
        except Exception as e:
            result['breakdown'].append(f"Insulator pricing error: {str(e)}")
            logger.error(f"Insulator pricing calculation failed: {str(e)}")
        
        return result
    
    def _calculate_connection_pricing(self, connection_info: Dict[str, str]) -> Dict[str, Any]:
        """Calculate process connection pricing"""
        result = {
            'cost': 0.0,
            'breakdown': []
        }
        
        try:
            conn_type = connection_info.get('type', 'NPT')
            size = connection_info.get('size', '3/4"')
            material = connection_info.get('material', 'SS')
            rating = connection_info.get('rating')
            
            connection_cost = self.db.calculate_connection_cost(conn_type, size, material, rating)
            if connection_cost > 0:
                display_text = self.db.format_connection_display(conn_type, size, material, rating)
                result['cost'] = connection_cost
                result['breakdown'].append(f"Process Connection ({display_text}): ${connection_cost:.2f}")
            
        except Exception as e:
            result['breakdown'].append(f"Connection pricing error: {str(e)}")
            logger.error(f"Connection pricing calculation failed: {str(e)}")
        
        return result
    
    def get_pricing_summary(self, pricing_result: Dict[str, Any]) -> str:
        """Generate a formatted pricing summary"""
        lines = [
            "PRICING BREAKDOWN",
            "=" * 30
        ]
        
        for item in pricing_result.get('breakdown', []):
            lines.append(f"  {item}")
        
        if pricing_result.get('calculation_notes'):
            lines.append("")
            lines.append("NOTES:")
            lines.append("-" * 10)
            for note in pricing_result['calculation_notes']:
                lines.append(f"  • {note}")
        
        return "\n".join(lines)
    
    def validate_pricing_configuration(self, 
                                     model_code: str, 
                                     material_code: str, 
                                     option_codes: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that the pricing configuration is valid
        
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        is_valid = True
        
        try:
            # Check if model exists in database
            model_info = self.db.get_model_info(model_code)
            if not model_info:
                warnings.append(f"Model {model_code} not found in pricing database")
                is_valid = False
            
            # Check if material exists
            material_info = self.db.get_material_info(material_code)
            if not material_info:
                warnings.append(f"Material {material_code} not found in pricing database")
            
            # Check options
            for option_code in option_codes:
                if not option_code.endswith('DEG') and option_code != '3/4"OD':
                    option_info = self.db.get_option_info(option_code)
                    if not option_info:
                        warnings.append(f"Option {option_code} not found in pricing database")
            
        except Exception as e:
            warnings.append(f"Pricing validation error: {str(e)}")
            is_valid = False
        
        return is_valid, warnings
    
    # SPARE PARTS PRICING METHODS
    
    def calculate_spare_parts_pricing(self, spare_parts_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate total pricing for a list of spare parts
        
        Args:
            spare_parts_list: List of spare part dictionaries with part_number, quantity, and optional specifications
            
        Returns:
            Dict containing spare parts pricing breakdown and totals
        """
        try:
            result = {
                'spare_parts': [],
                'subtotal': 0.0,
                'total_parts': 0,
                'breakdown': [],
                'warnings': [],
                'success': True
            }
            
            if not spare_parts_list:
                result['breakdown'].append("No spare parts included")
                return result
            
            for part_item in spare_parts_list:
                part_pricing = self.spare_parts_manager.calculate_spare_part_quote(
                    part_number=part_item['part_number'],
                    quantity=part_item.get('quantity', 1),
                    specifications=part_item.get('specifications', {})
                )
                
                if 'error' not in part_pricing:
                    result['spare_parts'].append(part_pricing)
                    result['subtotal'] += part_pricing['total_price']
                    result['total_parts'] += part_pricing['quantity']
                    result['breakdown'].append(part_pricing['line_item'])
                else:
                    result['warnings'].append(part_pricing['error'])
                    logger.warning(f"Spare parts pricing error: {part_pricing['error']}")
            
            if result['subtotal'] > 0:
                result['breakdown'].append(f"Spare Parts Subtotal: ${result['subtotal']:,.2f}")
            
            logger.info(f"Spare parts pricing calculated: {result['total_parts']} parts, ${result['subtotal']:,.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Spare parts pricing calculation failed: {str(e)}")
            return {
                'spare_parts': [],
                'subtotal': 0.0,
                'total_parts': 0,
                'breakdown': [f"ERROR: {str(e)}"],
                'warnings': [f"Spare parts calculation failed: {str(e)}"],
                'success': False,
                'error': str(e)
            }
    
    def calculate_complete_quote_pricing(self, 
                                       model_code: str, 
                                       voltage: str, 
                                       material_code: str, 
                                       probe_length: float, 
                                       option_codes: Optional[List[str]] = None, 
                                       insulator_code: Optional[str] = None, 
                                       connection_info: Optional[Dict[str, str]] = None,
                                       spare_parts_list: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Calculate complete quote pricing including products and spare parts
        
        Args:
            model_code: Product model
            voltage: Voltage specification
            material_code: Material code
            probe_length: Probe length in inches
            option_codes: List of option codes
            insulator_code: Insulator material code
            connection_info: Process connection details
            spare_parts_list: List of spare parts with quantities and specifications
            
        Returns:
            Dict containing complete quote pricing breakdown
        """
        try:
            logger.info(f"Calculating complete quote pricing for {model_code} with {len(spare_parts_list or [])} spare parts")
            
            # Calculate main product pricing
            product_pricing = self.calculate_complete_pricing(
                model_code=model_code,
                voltage=voltage,
                material_code=material_code,
                probe_length=probe_length,
                option_codes=option_codes,
                insulator_code=insulator_code,
                connection_info=connection_info
            )
            
            # Calculate spare parts pricing
            spare_parts_pricing = self.calculate_spare_parts_pricing(spare_parts_list or [])
            
            # Combine results
            quote_total = product_pricing['total_price'] + spare_parts_pricing['subtotal']
            
            complete_result = {
                'product_pricing': product_pricing,
                'spare_parts_pricing': spare_parts_pricing,
                'quote_total': quote_total,
                'formatted_total': f'${quote_total:,.2f}',
                'breakdown': [],
                'warnings': [],
                'success': product_pricing['success'] and spare_parts_pricing['success']
            }
            
            # Build combined breakdown
            complete_result['breakdown'].append("=== PRODUCT PRICING ===")
            complete_result['breakdown'].extend(product_pricing['breakdown'])
            
            if spare_parts_pricing['spare_parts']:
                complete_result['breakdown'].append("")
                complete_result['breakdown'].append("=== SPARE PARTS ===")
                complete_result['breakdown'].extend(spare_parts_pricing['breakdown'])
            
            complete_result['breakdown'].append("")
            complete_result['breakdown'].append(f"QUOTE TOTAL: ${quote_total:,.2f}")
            
            # Combine warnings
            complete_result['warnings'].extend(product_pricing.get('warnings', []))
            complete_result['warnings'].extend(spare_parts_pricing.get('warnings', []))
            
            logger.info(f"Complete quote pricing calculated: ${quote_total:,.2f}")
            
            return complete_result
            
        except Exception as e:
            logger.error(f"Complete quote pricing calculation failed: {str(e)}")
            return {
                'product_pricing': {'total_price': 0.0, 'success': False},
                'spare_parts_pricing': {'subtotal': 0.0, 'success': False},
                'quote_total': 0.0,
                'formatted_total': '$0.00',
                'breakdown': [f"ERROR: {str(e)}"],
                'warnings': [f"Quote calculation failed: {str(e)}"],
                'success': False,
                'error': str(e)
            }
    
    def get_spare_parts_recommendations(self, model_code: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recommended spare parts for a model with pricing"""
        try:
            recommendations = self.spare_parts_manager.get_recommended_spare_parts(model_code, limit)
            
            # Add quick pricing for each recommendation
            for part in recommendations:
                pricing = self.spare_parts_manager.calculate_spare_part_quote(part['part_number'], 1)
                if 'error' not in pricing:
                    part['unit_price'] = pricing['unit_price']
                    part['formatted_price'] = f"${pricing['unit_price']:,.2f}"
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get spare parts recommendations: {str(e)}")
            return []
    
    def validate_spare_parts_configuration(self, spare_parts_list: List[Dict[str, Any]], model_code: str) -> Dict[str, Any]:
        """Validate spare parts configuration for compatibility and requirements"""
        try:
            result = {
                'valid': True,
                'errors': [],
                'warnings': [],
                'validated_parts': []
            }
            
            for part_item in spare_parts_list:
                validation = self.spare_parts_manager.validate_spare_part_order(
                    part_number=part_item['part_number'],
                    model_code=model_code,
                    specifications=part_item.get('specifications', {})
                )
                
                if not validation['valid']:
                    result['valid'] = False
                    result['errors'].extend(validation.get('errors', []))
                
                result['warnings'].extend(validation.get('warnings', []))
                result['validated_parts'].append({
                    'part_number': part_item['part_number'],
                    'validation': validation
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Spare parts validation failed: {str(e)}")
            return {
                'valid': False,
                'errors': [f"Validation failed: {str(e)}"],
                'warnings': [],
                'validated_parts': []
            }


# Convenience function for backward compatibility
def calculate_total_price(model_code: str, voltage: str, material_code: str, 
                         probe_length: float, option_codes: Optional[List[str]] = None, 
                         insulator_code: Optional[str] = None, 
                         connection_info: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Convenience function that creates a PricingEngine instance and calculates pricing
    
    This maintains backward compatibility with existing code
    """
    engine = PricingEngine()
    return engine.calculate_complete_pricing(
        model_code, voltage, material_code, probe_length, 
        option_codes, insulator_code, connection_info
    )

# Test the pricing engine
if __name__ == "__main__":
    print("Testing Pricing Engine...")
    
    try:
        engine = PricingEngine()
        
        # Test basic pricing
        result = engine.calculate_complete_pricing(
            model_code="LS2000",
            voltage="115VAC", 
            material_code="S",
            probe_length=10.0,
            option_codes=["XSP", "VR"],
            insulator_code="U"
        )
        
        print(f"✅ Test successful!")
        print(f"Total Price: ${result['total_price']:.2f}")
        print(f"Base Price: ${result['base_price']:.2f}")
        print("\nBreakdown:")
        for item in result['breakdown']:
            print(f"  {item}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
"""
Part Number Parser for Babbitt Quote Generator
Parses complex part numbers like: LS2000-115VAC-S-10"-XSP-VR-8"TEFINS
"""

import re
from typing import Dict, List, Optional, Any
from database.db_manager import DatabaseManager

class PartNumberParser:
    def __init__(self):
        """Initialize parser with database connection"""
        self.db = DatabaseManager()
        
        # Load current data from database
        self.material_codes = self.db.get_material_codes()
        self.option_codes = self.db.get_option_codes()
        self.insulator_codes = self.db.get_insulator_codes()
        
        # Fallback hardcoded values if database unavailable
        if not self.material_codes:
            self.material_codes = {
                'S': '316 Stainless Steel',
                'H': 'Halar Coated',
                'TS': 'Teflon Sleeve', 
                'U': 'UHMWPE Blind End',
                'T': 'Teflon Blind End',
                'C': 'Ceramic',
                'CPVC': 'CPVC Blind End'
            }
        
        if not self.option_codes:
            self.option_codes = {
                'XSP': 'Extra Static Protection',
                'VR': 'Vibration Resistance',
                # 'BP': 'Bent Probe',  # Now handled as degree format (e.g., 90DEG)
                'CP': 'Cable Probe',
                'SSTAG': 'Stainless Steel Tag',
                # 'TEF': 'Teflon Insulator',  # Now handled as insulator via XINS format
                # 'PEEK': 'PEEK Insulator',   # Now handled as insulator via XINS format
                'SSHSE': 'Stainless Steel Housing',
                'VRHSE': 'Epoxy Housing',
                '3/4"OD': '3/4" Diameter Probe'
            }
        
        if not self.insulator_codes:
            self.insulator_codes = {
                'TEF': 'Teflon',
                'UHMWPE': 'UHMWPE',
                'DEL': 'Delrin',
                'PEEK': 'PEEK',
                'CER': 'Ceramic',
                'U': 'UHMWPE'
            }
        
        # Default values by model (enhanced with database info)
        self.model_defaults = {
            'LS2000': {
                'process_connection_type': 'NPT',
                'process_connection_size': '3/4"',
                'process_connection_material': 'S',
                'oring_material': 'Viton',
                'insulator_material': 'U',
                'insulator_length': 4.0,
                'probe_diameter': '½"',
                'housing_type': 'Cast Aluminum, NEMA 7, C, D; NEMA 9, E, F, & G',
                'output_type': '10 Amp SPDT Relay',
                'max_pressure': 300,
                'max_temperature': 180
            },
            'LS2100': {
                'process_connection_type': 'NPT',
                'process_connection_size': '3/4"', 
                'process_connection_material': 'S',
                'oring_material': 'Viton',
                'insulator_material': 'TEF',
                'insulator_length': 4.0,
                'probe_diameter': '½"',
                'housing_type': 'Cast Aluminum, NEMA 7, C, D; NEMA 9, E, F, & G',
                'output_type': '8mA-16mA Loop',
                'max_pressure': 300,
                'max_temperature': 450
            },
            'LS6000': {
                'process_connection_type': 'NPT',
                'process_connection_size': '1"',
                'process_connection_material': 'S',
                'oring_material': 'Viton',
                'insulator_material': 'DEL',
                'insulator_length': 4.0,
                'probe_diameter': '½"',
                'housing_type': 'Cast Aluminum, Explosion Proof',
                'output_type': '5 Amp DPDT Relay',
                'max_pressure': 1500,
                'max_temperature': 250
            },
            'LS7000': {
                'process_connection_type': 'NPT',
                'process_connection_size': '1"',
                'process_connection_material': 'S',
                'oring_material': 'Viton',
                'insulator_material': 'TEF',
                'insulator_length': 4.0,
                'probe_diameter': '½"',
                'housing_type': 'Cast Aluminum, NEMA 7, D',
                'output_type': '2 Form C contacts 5 Amp DPDT',
                'max_pressure': 1500,
                'max_temperature': 450
            }
        }
    
    def parse_part_number(self, part_number: str) -> Dict[str, Any]:
        """
        Parse a complete part number into all components
        Example: LS2000-115VAC-S-10"-XSP-VR-8"TEFINS
        """
        try:
            # Clean up the part number
            part_number = part_number.strip().upper()
            
            # Split by hyphens
            parts = part_number.split('-')
            
            if len(parts) < 4:
                raise ValueError(f"Invalid part number format: {part_number}")
            
            # Basic components
            result = {
                'original_part_number': part_number,
                'model': parts[0],
                'voltage': parts[1], 
                'probe_material': parts[2],
                'probe_length': self._parse_length(parts[3]),
                'options': [],
                'insulator': None,
                'process_connection': None,
                'calculated_specs': {},
                'pricing': {},
                'errors': [],
                'warnings': []
            }
            
            # Get model defaults
            defaults = self.model_defaults.get(result['model'], {})
            result.update(defaults)
            
            # Apply material-specific business rules
            self._apply_material_rules(result)
            
            # Parse remaining parts (options, insulators, connections)
            if len(parts) > 4:
                remaining_parts = parts[4:]
                self._parse_options_and_modifiers(remaining_parts, result)
            
            # Calculate derived specifications
            self._calculate_specifications(result)
            
            # Calculate pricing
            self._calculate_pricing(result)
            
            # Validate configuration
            self._validate_configuration(result)
            
            return result
            
        except Exception as e:
            return {
                'original_part_number': part_number,
                'error': str(e),
                'errors': [str(e)],
                'success': False
            }
    
    def _parse_length(self, length_part: str) -> float:
        """Parse length from string like '10"' or '12.5"'"""
        # Remove quotes and extract number
        length_str = length_part.replace('"', '').replace("'", '')
        try:
            return float(length_str)
        except ValueError:
            return 10.0  # Default length
    
    def _parse_options_and_modifiers(self, parts: List[str], result: Dict[str, Any]):
        """Parse options, insulators, and connection modifiers"""
        
        for part in parts:
            # Check for insulator pattern (ends with INS)
            if part.endswith('INS'):
                result['insulator'] = self._parse_insulator(part)
            
            # Check for bent probe degree format (e.g., 90DEG, 45DEG)
            elif part.endswith('DEG'):
                bent_probe_info = self._parse_bent_probe(part)
                if bent_probe_info:
                    result['options'].append(bent_probe_info)
                else:
                    result['warnings'].append(f"Invalid bent probe format: {part}")
            
            # Check for known option codes
            elif part in self.option_codes:
                result['options'].append({
                    'code': part,
                    'name': self.option_codes[part]
                })
            
            # Check for process connection override
            elif any(conn in part for conn in ['NPT', 'RF', 'TRICLAMP']):
                result['process_connection'] = self._parse_connection_override(part)
            
            # Check for housing option
            elif part in ['SS']:  # Stainless Steel housing
                result['housing_type'] = 'Stainless Steel, NEMA 4X'
                result['options'].append({
                    'code': 'SSHSE',
                    'name': 'Stainless Steel Housing'
                })
            
            # Unknown option - add as warning
            else:
                result['warnings'].append(f"Unknown option or modifier: {part}")
    
    def _apply_material_rules(self, result: Dict[str, Any]):
        """Apply material-specific business rules"""
        
        probe_material = result.get('probe_material', 'S')
        
        # Business Rule: Halar coating requires Teflon insulator
        if probe_material == 'H':  # Halar coated probe
            # Only change if no explicit insulator override in part number
            if not result.get('insulator'):
                result['insulator_material'] = 'TEF'  # Switch to Teflon
                result['warnings'].append("Halar coating: Insulator automatically changed to Teflon")
    
    def _parse_insulator(self, insulator_part: str) -> Dict[str, Any]:
        """
        Parse insulator specification like '8"TEFINS'
        Returns: {'length': 8.0, 'material': 'TEF', 'material_name': 'Teflon'}
        """
        # Pattern: NUMBER + " + MATERIAL + INS
        match = re.match(r'(\d+(?:\.\d+)?)"([A-Z]+)INS', insulator_part)
        
        if match:
            length = float(match.group(1))
            material_code = match.group(2)
            material_name = self.insulator_codes.get(material_code, f"Unknown ({material_code})")
            
            return {
                'length': length,
                'material': material_code,
                'material_name': material_name,
                'original': insulator_part
            }
        
        return {
            'length': 4.0,
            'material': 'UNKNOWN',
            'material_name': f"Unknown ({insulator_part})",
            'original': insulator_part
        }
    
    def _parse_connection_override(self, connection_part: str) -> Dict[str, Any]:
        """Parse process connection override like '1"NPT' or '2"150#RF'"""
        
        # NPT pattern: SIZE + NPT
        npt_match = re.match(r'(\d+(?:/\d+)?)"NPT', connection_part)
        if npt_match:
            size = npt_match.group(1) + '"'
            return {
                'type': 'NPT',
                'size': size,
                'rating': None,
                'display': f'{size}NPT'
            }
        
        # Flange pattern: SIZE + RATING + RF  
        flange_match = re.match(r'(\d+(?:/\d+)?)"(\d+)#RF', connection_part)
        if flange_match:
            size = flange_match.group(1) + '"'
            rating = flange_match.group(2) + '#'
            return {
                'type': 'Flange',
                'size': size,
                'rating': rating,
                'display': f'{size}{rating}RF'
            }
        
        # Default if can't parse
        return {
            'type': 'UNKNOWN',
            'size': 'UNKNOWN',
            'rating': None,
            'display': connection_part
        }
    
    def _parse_bent_probe(self, bent_probe_part: str) -> Optional[Dict[str, Any]]:
        """
        Parse bent probe degree specification like '90DEG', '45DEG', '180DEG'
        Returns: {'code': '90DEG', 'name': 'Bent Probe (90°)', 'degree': 90}
        """
        # Pattern: NUMBER + DEG
        match = re.match(r'(\d+)DEG', bent_probe_part)
        
        if match:
            degree = int(match.group(1))
            
            # Validate degree range (0-180)
            if 0 <= degree <= 180:
                return {
                    'code': f'{degree}DEG',
                    'name': f'Bent Probe ({degree}°)',
                    'degree': degree,
                    'price': 50.0,  # Fixed price for all bent probe configurations
                    'category': 'probe'
                }
            
        return None
    
    def _calculate_specifications(self, result: Dict[str, Any]):
        """Calculate derived specifications based on configuration"""
        
        # Max temperature from insulator material
        insulator_material = None
        if result.get('insulator'):
            insulator_material = result['insulator']['material']
        else:
            # Use default insulator material (which may have been updated by material rules)
            insulator_material = result.get('insulator_material', 'U')
        
        temp_ratings = {
            'TEF': 450,
            'UHMWPE': 180,
            'U': 180,
            'DEL': 250,
            'PEEK': 550,
            'CER': 800
        }
        result['max_temperature'] = temp_ratings.get(insulator_material, 180)
        
        # Max pressure from connection size
        if result.get('process_connection'):
            size = result['process_connection']['size']
            # Simplified pressure ratings
            if '3/4' in size:
                result['max_pressure'] = 300
            elif '1' in size:
                result['max_pressure'] = 300
            elif '2' in size:
                result['max_pressure'] = 150
        
        # Probe material name
        probe_material = result.get('probe_material', 'S')
        result['probe_material_name'] = self.material_codes.get(probe_material, f"Unknown ({probe_material})")
        
        # Check for 3/4" OD option and update probe diameter
        option_codes = [opt.get('code', '') for opt in result.get('options', [])]
        if '3/4"OD' in option_codes:
            result['probe_diameter'] = '¾"'
        
        # Calculate base insulator length based on probe length
        probe_length = result.get('probe_length', 10.0)
        base_insulator_length = self._calculate_base_insulator_length(probe_length)
        result['base_insulator_length'] = base_insulator_length
        
        # Add base insulator length to insulator information if present
        if result.get('insulator'):
            result['insulator']['base_length'] = base_insulator_length
        else:
            # If no explicit insulator, use base length as actual length
            result['insulator_length'] = base_insulator_length
            result['insulator_base_length'] = base_insulator_length
    
    def _calculate_pricing(self, result: Dict[str, Any]):
        """Calculate pricing for the parsed part number"""
        try:
            model = result.get('model', '')
            voltage = result.get('voltage', '')
            material = result.get('probe_material', 'S')
            length = result.get('probe_length', 10.0)
            
            # Get option codes
            option_codes = [opt['code'] for opt in result.get('options', [])]
            
            # Get insulator code
            insulator_code = None
            if result.get('insulator'):
                insulator_code = result['insulator']['material']
            else:
                # Use default insulator
                insulator_code = result.get('insulator_material', 'U')
            
            # Get process connection info
            connection_info = None
            if result.get('process_connection'):
                connection_info = {
                    'type': result['process_connection'].get('type', 'NPT'),
                    'size': result['process_connection'].get('size', '3/4"'),
                    'material': 'SS',  # Default to stainless steel
                    'rating': result['process_connection'].get('rating')
                }
            
            # Calculate pricing using database
            pricing = self.db.calculate_total_price(
                model, voltage, material, length, option_codes, insulator_code, connection_info
            )
            
            # Add pricing to result
            result['pricing'] = pricing
            
            # Update options with detailed pricing information from database
            if pricing.get('option_details'):
                option_details_map = {opt['code']: opt for opt in pricing['option_details']}
                
                for option in result.get('options', []):
                    if option['code'] in option_details_map:
                        # Merge database pricing details into the option
                        db_option = option_details_map[option['code']]
                        option.update({
                            'price': db_option.get('price', 0),
                            'price_type': db_option.get('price_type', 'fixed'),
                            'base_cost': db_option.get('base_cost'),
                            'per_foot_cost': db_option.get('per_foot_cost'),
                            'probe_length_feet': db_option.get('probe_length_feet')
                        })
            
        except Exception as e:
            result['warnings'].append(f"Pricing calculation failed: {str(e)}")
            result['pricing'] = {
                'total_price': 0.0,
                'base_price': 0.0,
                'length_cost': 0.0,
                'length_surcharge': 0.0,
                'option_cost': 0.0,
                'insulator_cost': 0.0,
                'connection_cost': 0.0,
                'error': str(e)
            }
    
    def _validate_configuration(self, result: Dict[str, Any]):
        """Validate the configuration for compatibility issues"""
        
        # Check for incompatible combinations
        if result.get('probe_material') == 'C':  # Cable probe
            # Cable probe can't have bent probe option
            for option in result.get('options', []):
                if option['code'].endswith('DEG'):  # Bent probe in degree format
                    result['errors'].append("Cable probe cannot be combined with bent probe option")
        
        # Check length limits
        probe_length = result.get('probe_length', 0)
        probe_material = result.get('probe_material', 'S')
        
        if probe_material == 'H' and probe_length > 72:
            result['warnings'].append("Halar coating limited to 72 inches - consider Teflon Sleeve for longer probes")
        
        # Check model-specific limitations
        model = result.get('model', '')
        if model == 'LS2000':
            # LS2000 specific checks
            if 'XSP' not in [opt['code'] for opt in result.get('options', [])]:
                result['warnings'].append("LS2000 has limited static protection - consider XSP option for plastic pellets/resins")
    
    def get_quote_data(self, parsed_part: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quote data from parsed part number"""
        
        # Get pricing information
        pricing = parsed_part.get('pricing', {})
        
        quote_data = {
            'part_number': parsed_part.get('original_part_number', ''),
            'model': parsed_part.get('model', ''),
            'voltage': parsed_part.get('voltage', ''),
            'probe_material': parsed_part.get('probe_material_name', ''),
            'probe_material_name': parsed_part.get('probe_material_name', ''),
            'probe_length': parsed_part.get('probe_length', ''),
            'process_connection': self._format_connection_display(parsed_part),
            'insulator': self._format_insulator_display(parsed_part),
            'base_insulator_length': parsed_part.get('base_insulator_length', 4.0),
            'probe_diameter': parsed_part.get('probe_diameter', '½"'),
            'housing': parsed_part.get('housing_type', ''),
            'output': parsed_part.get('output_type', ''),
            'max_temperature': parsed_part.get('max_temperature', ''),
            'max_pressure': parsed_part.get('max_pressure', ''),
            'options': self._format_options_display(parsed_part),
            'errors': parsed_part.get('errors', []),
            'warnings': parsed_part.get('warnings', []),
            
            # Pricing information
            'total_price': pricing.get('total_price', 0.0),
            'base_price': pricing.get('base_price', 0.0),
            'length_cost': pricing.get('length_cost', 0.0),
            'length_surcharge': pricing.get('length_surcharge', 0.0),
            'option_cost': pricing.get('option_cost', 0.0),
            'insulator_cost': pricing.get('insulator_cost', 0.0),
            'connection_cost': pricing.get('connection_cost', 0.0),
            'price_breakdown': self._format_price_breakdown(pricing)
        }
        
        return quote_data
    
    def _format_price_breakdown(self, pricing: Dict[str, Any]) -> List[str]:
        """Format price breakdown for display"""
        breakdown = []
        
        if pricing.get('base_price', 0) > 0:
            breakdown.append(f"Base Price: ${pricing['base_price']:.2f}")
        
        if pricing.get('length_cost', 0) > 0:
            breakdown.append(f"Length Cost: ${pricing['length_cost']:.2f}")
        
        if pricing.get('length_surcharge', 0) > 0:
            breakdown.append(f"Length Surcharge: ${pricing['length_surcharge']:.2f}")
        
        if pricing.get('option_cost', 0) > 0:
            breakdown.append(f"Options: ${pricing['option_cost']:.2f}")
        
        if pricing.get('insulator_cost', 0) > 0:
            breakdown.append(f"Insulator: ${pricing['insulator_cost']:.2f}")
        
        if pricing.get('connection_cost', 0) > 0:
            breakdown.append(f"Process Connection: ${pricing['connection_cost']:.2f}")
        
        if pricing.get('total_price', 0) > 0:
            breakdown.append(f"TOTAL: ${pricing['total_price']:.2f}")
        
        return breakdown
    
    def _format_connection_display(self, parsed_part: Dict[str, Any]) -> str:
        """Format process connection for display"""
        if parsed_part.get('process_connection'):
            return parsed_part['process_connection']['display']
        else:
            # Use defaults
            conn_type = parsed_part.get('process_connection_type', 'NPT')
            conn_size = parsed_part.get('process_connection_size', '3/4"')
            return f"{conn_size}{conn_type}"
    
    def _format_insulator_display(self, parsed_part: Dict[str, Any]) -> str:
        """Format insulator for display"""
        if parsed_part.get('insulator'):
            ins = parsed_part['insulator']
            actual_length = ins['length']
            base_length = ins.get('base_length', parsed_part.get('base_insulator_length', 4.0))
            material_name = ins['material_name']
            
            # Show both actual and base length if they differ
            if actual_length != base_length:
                return f"{actual_length:.1f}\" {material_name} (Base: {base_length:.1f}\")"
            else:
                return f"{actual_length:.1f}\" {material_name}"
        else:
            # Use defaults
            material = parsed_part.get('insulator_material', 'U')
            material_name = self.insulator_codes.get(material, material)
            base_length = parsed_part.get('base_insulator_length', 4.0)
            actual_length = parsed_part.get('insulator_length', base_length)
            
            # Show both actual and base length if they differ
            if actual_length != base_length:
                return f"{actual_length:.1f}\" {material_name} (Base: {base_length:.1f}\")"
            else:
                return f"{actual_length:.1f}\" {material_name}"
    
    def _format_options_display(self, parsed_part: Dict[str, Any]) -> List[str]:
        """Format options for display"""
        options = []
        for option in parsed_part.get('options', []):
            options.append(f"{option['code']}: {option['name']}")
        
        return options

    def _calculate_base_insulator_length(self, probe_length: float) -> float:
        """
        Calculate base insulator length based on probe length for quote templates.
        
        Rules:
        - Probe length >= 8": Base insulator length = 4"
        - Probe length 5-7": Base insulator length = 2" 
        - Probe length <= 4": Base insulator length = 1"
        
        Args:
            probe_length: Probe length in inches
            
        Returns:
            Base insulator length in inches
        """
        if probe_length >= 8.0:
            return 4.0
        elif probe_length >= 5.0:
            return 2.0
        else:
            return 1.0

# Test the parser if run directly
if __name__ == "__main__":
    print("Testing Part Number Parser with Pricing...")
    print("=" * 50)
    
    parser = PartNumberParser()
    
    # Test cases
    test_cases = [
        "LS2000-115VAC-S-10\"",
        "LS2000-115VAC-S-10\"-XSP-VR-8\"TEFINS", 
        "LS2100-24VDC-H-12\"",
        "LS6000-115VAC-S-14\"-1\"NPT"
    ]
    
    for test_case in test_cases:
        print(f"\nParsing: {test_case}")
        print("-" * 30)
        
        result = parser.parse_part_number(test_case)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✓ Model: {result['model']}")
            print(f"✓ Voltage: {result['voltage']}")
            print(f"✓ Probe: {result['probe_material_name']} @ {result['probe_length']}\"")
            print(f"✓ Connection: {parser._format_connection_display(result)}")
            print(f"✓ Insulator: {parser._format_insulator_display(result)}")
            
            # Display pricing
            pricing = result.get('pricing', {})
            if pricing.get('total_price', 0) > 0:
                print(f"💰 Total Price: ${pricing['total_price']:.2f}")
                print(f"   - Base: ${pricing['base_price']:.2f}")
                if pricing.get('length_cost', 0) > 0:
                    print(f"   - Length: ${pricing['length_cost']:.2f}")
                if pricing.get('option_cost', 0) > 0:
                    print(f"   - Options: ${pricing['option_cost']:.2f}")
                if pricing.get('insulator_cost', 0) > 0:
                    print(f"   - Insulator: ${pricing['insulator_cost']:.2f}")
                if pricing.get('connection_cost', 0) > 0:
                    print(f"   - Connection: ${pricing['connection_cost']:.2f}")
            
            if result.get('options'):
                print(f"✓ Options: {', '.join([opt['code'] for opt in result['options']])}")
            
            if result.get('warnings'):
                print(f"⚠️  Warnings: {'; '.join(result['warnings'])}")
            
            if result.get('errors'):
                print(f"❌ Errors: {'; '.join(result['errors'])}")
    
    print(f"\n🎉 Testing complete!") 
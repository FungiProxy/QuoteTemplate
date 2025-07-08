"""
Spare Parts Manager for Babbitt Quote Generator
Handles spare parts business logic, pricing, and validation
"""

from typing import Dict, List, Optional, Any, Tuple
import json
from database.db_manager import DatabaseManager

class SparePartsManager:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """Initialize spare parts manager"""
        self.db_manager = db_manager if db_manager else DatabaseManager()
        
        # Category display names and ordering
        self.category_display = {
            'electronics': 'Electronics',
            'probe_assembly': 'Probe Assemblies',
            'housing': 'Housing',
            'card': 'Cards',
            'transmitter': 'Transmitters',
            'receiver': 'Receivers',
            'fuse': 'Fuses',
            'cable': 'Cables'
        }
        
        # Category priority for ordering
        self.category_priority = {
            'electronics': 1,
            'probe_assembly': 2,
            'housing': 3,
            'card': 4,
            'transmitter': 5,
            'receiver': 6,
            'fuse': 7,
            'cable': 8
        }
    
    def get_spare_parts_for_model(self, model_code: str, category: Optional[str] = None) -> Dict[str, Any]:
        """Get organized spare parts data for a specific model"""
        if not self.db_manager.connect():
            return {'error': 'Database connection failed'}
        
        try:
            # Get all spare parts for the model
            if category:
                spare_parts = self.db_manager.get_spare_parts_by_category(category, model_code)
            else:
                spare_parts = self.db_manager.get_spare_parts_by_model(model_code)
            
            # Organize by category
            organized_parts = {}
            for part in spare_parts:
                cat = part['category'] or 'other'
                if cat not in organized_parts:
                    organized_parts[cat] = []
                organized_parts[cat].append(part)
            
            # Get category summary
            categories = self.db_manager.get_spare_part_categories(model_code)
            
            return {
                'model_code': model_code,
                'spare_parts': organized_parts,
                'categories': categories,
                'total_parts': len(spare_parts),
                'category_display': self.category_display
            }
        
        finally:
            self.db_manager.disconnect()
    
    def search_spare_parts(self, search_term: str, model_code: Optional[str] = None) -> List[Dict]:
        """Search spare parts with enhanced results"""
        if not self.db_manager.connect():
            return []
        
        try:
            results = self.db_manager.search_spare_parts(search_term, model_code)
            
            # Enhance results with category display names
            for part in results:
                part['category_display'] = self.category_display.get(part['category'], part['category'])
                part['priority'] = self.category_priority.get(part['category'], 99)
            
            # Sort by priority then name
            results.sort(key=lambda x: (x['priority'], x['name']))
            
            return results
        
        finally:
            self.db_manager.disconnect()
    
    def get_spare_part_details(self, part_number: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific spare part"""
        if not self.db_manager.connect():
            return None
        
        try:
            part = self.db_manager.get_spare_part_by_part_number(part_number)
            if not part:
                return None
            
            # Enhance with display information
            part['category_display'] = self.category_display.get(part['category'], part['category'])
            
            # Parse compatible models
            try:
                part['compatible_models_list'] = json.loads(part['compatible_models'])
            except (json.JSONDecodeError, TypeError):
                part['compatible_models_list'] = [part['compatible_models']] if part['compatible_models'] else []
            
            # Add ordering requirements summary
            requirements = []
            if part['requires_voltage_spec']:
                requirements.append('Voltage specification required')
            if part['requires_length_spec']:
                requirements.append('Length specification required')
            if part['requires_sensitivity_spec']:
                requirements.append('Sensitivity specification required')
            
            part['ordering_requirements'] = requirements
            
            return part
        
        finally:
            self.db_manager.disconnect()
    
    def calculate_spare_part_quote(self, part_number: str, quantity: int = 1, 
                                 specifications: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate pricing for a spare part with all specifications"""
        if not self.db_manager.connect():
            return {'error': 'Database connection failed'}
        
        specifications = specifications or {}
        
        try:
            # Get detailed pricing calculation
            pricing = self.db_manager.calculate_spare_part_price(
                part_number=part_number,
                quantity=quantity,
                voltage=specifications.get('voltage'),
                length=specifications.get('length'),
                sensitivity=specifications.get('sensitivity')
            )
            
            if 'error' in pricing:
                return pricing
            
            # Enhance with additional information
            part_details = self.get_spare_part_details(part_number)
            if part_details:
                pricing.update({
                    'category_display': part_details['category_display'],
                    'compatible_models': part_details['compatible_models_list'],
                    'ordering_requirements': part_details['ordering_requirements']
                })
            
            # Add line item formatting for quotes
            pricing['line_item'] = self._format_line_item(pricing, specifications)
            
            return pricing
        
        finally:
            self.db_manager.disconnect()
    
    def get_recommended_spare_parts(self, model_code: str, limit: int = 5) -> List[Dict]:
        """Get recommended spare parts for a model (most critical/common)"""
        if not self.db_manager.connect():
            return []
        
        try:
            # Get popular parts for the model
            parts = self.db_manager.get_popular_spare_parts(model_code, limit)
            
            # Enhance with display information
            for part in parts:
                part['category_display'] = self.category_display.get(part['category'], part['category'])
                
                # Add basic pricing info
                part['formatted_price'] = f"${part['price']:,.2f}"
            
            return parts
        
        finally:
            self.db_manager.disconnect()
    
    def validate_spare_part_order(self, part_number: str, model_code: str, 
                                specifications: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate a spare part order with all requirements"""
        if not self.db_manager.connect():
            return {'valid': False, 'error': 'Database connection failed'}
        
        specifications = specifications or {}
        
        try:
            # Check compatibility
            compatibility = self.db_manager.validate_spare_part_compatibility(part_number, model_code)
            if not compatibility['compatible']:
                return {
                    'valid': False,
                    'errors': [compatibility['error']],
                    'warnings': []
                }
            
            # Get part details for requirement validation
            part = self.db_manager.get_spare_part_by_part_number(part_number)
            if not part:
                return {
                    'valid': False,
                    'errors': [f"Spare part '{part_number}' not found"],
                    'warnings': []
                }
            
            errors = []
            warnings = []
            
            # Validate required specifications
            if part['requires_voltage_spec'] and not specifications.get('voltage'):
                errors.append("Voltage specification is required for this part")
            
            if part['requires_length_spec'] and not specifications.get('length'):
                errors.append("Length specification is required for this part")
            
            if part['requires_sensitivity_spec'] and not specifications.get('sensitivity'):
                errors.append("Sensitivity specification is required for this part")
            
            # Add informational warnings
            if part['notes']:
                warnings.append(f"Note: {part['notes']}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'part_info': {
                    'name': part['name'],
                    'category': part['category'],
                    'category_display': self.category_display.get(part['category'], part['category'])
                }
            }
        
        finally:
            self.db_manager.disconnect()
    
    def create_spare_parts_quote_section(self, spare_parts_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a formatted spare parts section for quotes"""
        if not spare_parts_list:
            return {
                'has_spare_parts': False,
                'spare_parts': [],
                'subtotal': 0.0,
                'formatted_subtotal': '$0.00'
            }
        
        total = 0.0
        formatted_parts = []
        
        for part_item in spare_parts_list:
            # Calculate pricing if not already done
            if 'total_price' not in part_item:
                pricing = self.calculate_spare_part_quote(
                    part_item['part_number'],
                    part_item.get('quantity', 1),
                    part_item.get('specifications', {})
                )
                if 'error' not in pricing:
                    part_item.update(pricing)
            
            if 'total_price' in part_item:
                total += part_item['total_price']
                formatted_parts.append(part_item)
        
        return {
            'has_spare_parts': len(formatted_parts) > 0,
            'spare_parts': formatted_parts,
            'subtotal': total,
            'formatted_subtotal': f'${total:,.2f}',
            'count': len(formatted_parts)
        }
    
    def get_category_summary(self, model_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get summary of spare parts categories"""
        if not self.db_manager.connect():
            return []
        
        try:
            categories = self.db_manager.get_spare_part_categories(model_code)
            
            # Enhance with display names and ordering
            for cat in categories:
                cat['display_name'] = self.category_display.get(cat['category'], cat['category'])
                cat['priority'] = self.category_priority.get(cat['category'], 99)
            
            # Sort by priority
            categories.sort(key=lambda x: x['priority'])
            
            return categories
        
        finally:
            self.db_manager.disconnect()
    
    def _format_line_item(self, pricing: Dict[str, Any], specifications: Dict[str, Any]) -> str:
        """Format a spare part as a line item for quotes"""
        name = pricing.get('name', pricing.get('part_number', 'Unknown Part'))
        quantity = pricing.get('quantity', 1)
        unit_price = pricing.get('unit_price', 0.0)
        total_price = pricing.get('total_price', 0.0)
        
        line = f"{quantity}x {name}"
        
        # Add specifications if provided
        specs = []
        if specifications.get('voltage'):
            specs.append(f"Voltage: {specifications['voltage']}")
        if specifications.get('length'):
            specs.append(f"Length: {specifications['length']}\"")
        if specifications.get('sensitivity'):
            specs.append(f"Sensitivity: {specifications['sensitivity']}")
        
        if specs:
            line += f" ({', '.join(specs)})"
        
        line += f" @ ${unit_price:.2f} = ${total_price:.2f}"
        
        return line
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.db_manager:
            self.db_manager.disconnect() 
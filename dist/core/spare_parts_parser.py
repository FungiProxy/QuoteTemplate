"""
Spare Parts Parser for Babbitt Quote Generator
Handles parsing of dynamic spare part numbers with variable components
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from database.db_manager import DatabaseManager

class SparePartsParser:
    def __init__(self):
        """Initialize spare parts parser with pattern definitions"""
        self.db = DatabaseManager()
        
        # Define parsing patterns for different spare part types
        self.patterns = {
            'electronics': {
                'pattern': r'^([A-Z0-9/]+)-(115VAC|24VDC|230VAC|12VDC)-E$',
                'base_format': '{model}-ELECTRONICS',
                'variables': ['model', 'voltage']
            },
            'probe_assembly': {
                'pattern': r'^([A-Z0-9/]+)-([A-Z]+)-(\d+(?:\.\d+)?)"?$',
                'base_format': '{model}-{material}-PROBE-ASSEMBLY-{length}',
                'variables': ['model', 'material', 'length']
            },
            'power_supply': {
                'pattern': r'^([A-Z0-9/]+)-(115VAC|24VDC|230VAC|12VDC)-PS$',
                'base_format': '{model}-PS-POWER-SUPPLY',
                'variables': ['model', 'voltage']
            },
            'receiver_card': {
                'pattern': r'^([A-Z0-9/]+)-(115VAC|24VDC|230VAC|12VDC)-R$',
                'base_format': '{model}-R-RECEIVER-CARD',
                'variables': ['model', 'voltage']
            },
            'transmitter': {
                'pattern': r'^([A-Z0-9/]+)-(.+)-T$',
                'base_format': '{model}-T-TRANSMITTER',
                'variables': ['model', 'specs']  # specs can be size-sensitivity or just size
            },
            'sensing_card': {
                'pattern': r'^([A-Z0-9/]+)-SC$',
                'base_format': '{model}-SC-SENSING-CARD',
                'variables': ['model']
            },
            'dual_point_card': {
                'pattern': r'^([A-Z0-9/]+)-DP$',
                'base_format': '{model}-DP-DUAL-POINT-CARD',
                'variables': ['model']
            },
            'plugin_card': {
                'pattern': r'^([A-Z0-9/]+)-MA$',
                'base_format': '{model}-MA-PLUGIN-CARD',
                'variables': ['model']
            },
            'bb_power_supply': {
                'pattern': r'^([A-Z0-9/]+)-(115VAC|24VDC|230VAC|12VDC)-BB$',
                'base_format': '{model}-BB-POWER-SUPPLY',
                'variables': ['model', 'voltage']
            },
            'fuse': {
                'pattern': r'^([A-Z0-9/]+)-FUSE$',
                'base_format': 'FUSE-1/2-AMP',  # Special case - maps to generic fuse
                'variables': ['model']
            },
            'housing': {
                'pattern': r'^([A-Z0-9/]+)-HOUSING$',
                'base_format': '{model}-HOUSING',
                'variables': ['model']
            }
        }
        
        # Valid voltages
        self.valid_voltages = ['115VAC', '24VDC', '230VAC', '12VDC']
        
        # Valid materials for probe assemblies
        self.valid_materials = ['S', 'H', 'U', 'T', 'TS', 'CPVC', 'C']

    def parse_spare_part_number(self, part_number: str) -> Dict[str, Any]:
        """
        Parse a spare part number and return detailed information
        """
        part_number = part_number.strip().upper()
        
        result = {
            'original_part_number': part_number,
            'parsed_successfully': False,
            'base_part_number': None,
            'part_type': None,
            'variables': {},
            'database_match': None,
            'pricing_info': None,
            'errors': [],
            'warnings': []
        }
        
        # Try to match against each pattern
        for part_type, pattern_info in self.patterns.items():
            match = re.match(pattern_info['pattern'], part_number)
            if match:
                result['parsed_successfully'] = True
                result['part_type'] = part_type
                
                # Extract variables based on pattern
                if part_type == 'electronics':
                    result['variables'] = {
                        'model': match.group(1),
                        'voltage': match.group(2)
                    }
                    result['base_part_number'] = f"{match.group(1)}-ELECTRONICS"
                
                elif part_type == 'probe_assembly':
                    result['variables'] = {
                        'model': match.group(1),
                        'material': match.group(2),
                        'length': match.group(3)
                    }
                    result['base_part_number'] = f"{match.group(1)}-{match.group(2)}-PROBE-ASSEMBLY-{match.group(3)}"
                
                elif part_type in ['power_supply', 'receiver_card', 'bb_power_supply']:
                    result['variables'] = {
                        'model': match.group(1),
                        'voltage': match.group(2)
                    }
                    result['base_part_number'] = pattern_info['base_format'].format(**result['variables'])
                
                elif part_type == 'transmitter':
                    result['variables'] = {
                        'model': match.group(1),
                        'specs': match.group(2)
                    }
                    result['base_part_number'] = f"{match.group(1)}-T-TRANSMITTER"
                
                elif part_type == 'fuse':
                    result['variables'] = {'model': match.group(1)}
                    result['base_part_number'] = 'FUSE-1/2-AMP'  # Generic fuse entry
                
                else:  # Simple cases like sensing_card, dual_point_card, etc.
                    result['variables'] = {'model': match.group(1)}
                    result['base_part_number'] = pattern_info['base_format'].format(**result['variables'])
                
                break
        
        if not result['parsed_successfully']:
            result['errors'].append(f"Unable to parse spare part number: {part_number}")
            return result
        
        # Validate variables
        self._validate_variables(result)
        
        # Look up in database
        self._lookup_database_match(result)
        
        # Calculate pricing if database match found
        if result['database_match']:
            self._calculate_spare_part_pricing(result)
        
        return result

    def _validate_variables(self, result: Dict[str, Any]):
        """Validate extracted variables"""
        variables = result['variables']
        part_type = result['part_type']
        
        # Validate voltage if present
        if 'voltage' in variables:
            if variables['voltage'] not in self.valid_voltages:
                result['errors'].append(f"Invalid voltage: {variables['voltage']}")
        
        # Validate material if present (for probe assemblies)
        if 'material' in variables:
            if variables['material'] not in self.valid_materials:
                result['warnings'].append(f"Unusual material code: {variables['material']}")
        
        # Validate length if present
        if 'length' in variables:
            try:
                length_val = float(variables['length'])
                if length_val <= 0 or length_val > 999:
                    result['warnings'].append(f"Unusual length: {length_val}")
            except ValueError:
                result['errors'].append(f"Invalid length format: {variables['length']}")

    def _lookup_database_match(self, result: Dict[str, Any]):
        """Look up the base part number in the database"""
        if not self.db.connect():
            result['errors'].append("Database connection failed")
            return
        
        try:
            # For fuses, we need special handling
            if result['part_type'] == 'fuse':
                # Look up fuse pricing based on model
                model = result['variables']['model']
                if model == 'LT9000':
                    price = 20.00
                else:
                    price = 10.00
                
                result['database_match'] = {
                    'part_number': f"{model}-FUSE",
                    'name': f"{model} Fuse",
                    'description': f"Replacement fuse for {model}",
                    'price': price,
                    'category': 'fuse',
                    'compatible_models': [model]
                }
            else:
                # Look up the base part number
                spare_part = self.db.get_spare_part_by_part_number(result['base_part_number'])
                if spare_part:
                    result['database_match'] = spare_part
                else:
                    result['errors'].append(f"Part not found in database: {result['base_part_number']}")
        
        finally:
            self.db.disconnect()

    def _calculate_spare_part_pricing(self, result: Dict[str, Any]):
        """Calculate pricing for the spare part"""
        if not result['database_match']:
            return
        
        base_price = result['database_match']['price']
        variables = result['variables']
        
        # For probe assemblies, calculate length-based pricing
        if result['part_type'] == 'probe_assembly' and 'length' in variables:
            length = float(variables['length'])
            material = variables['material']
            
            # Add length surcharges based on material and length
            if material == 'S' and length > 10:  # Stainless steel
                additional_cost = (length - 10) * 45.0 / 12.0  # $45 per foot
            elif material == 'H' and length > 10:  # Halar
                additional_cost = (length - 10) * 110.0 / 12.0  # $110 per foot
            else:
                additional_cost = 0
            
            base_price += additional_cost
        
        result['pricing_info'] = {
            'base_price': result['database_match']['price'],
            'calculated_price': base_price,
            'variables_applied': variables
        }

    def get_valid_voltages(self) -> List[str]:
        """Get list of valid voltages"""
        return self.valid_voltages.copy()

    def get_valid_materials(self) -> List[str]:
        """Get list of valid probe materials"""
        return self.valid_materials.copy()

    def suggest_part_number_format(self, partial_number: str) -> List[str]:
        """Suggest proper format for a partial spare part number"""
        suggestions = []
        partial = partial_number.upper().strip()
        
        # Check if it looks like it could be any of our patterns
        for part_type, pattern_info in self.patterns.items():
            if any(partial.startswith(model) for model in ['LS2000', 'LS2100', 'LS6000', 'LS7000', 'LS8000', 'LT9000', 'FS10000']):
                if part_type == 'electronics':
                    suggestions.append(f"{partial}-115VAC-E (or 24VDC, 230VAC, 12VDC)")
                elif part_type == 'probe_assembly':
                    suggestions.append(f"{partial}-S-10\" (Model-Material-Length)")
                # Add more suggestions as needed
        
        return suggestions 
"""
Input Validation and Compatibility Checks for Babbitt Quote Generator
Provides comprehensive validation rules and compatibility checking
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from config.settings import (
    MAX_PART_NUMBER_LENGTH, MAX_CUSTOMER_NAME_LENGTH,
    MIN_PROBE_LENGTH, MAX_PROBE_LENGTH, HALAR_MAX_LENGTH
)

class ValidationError(Exception):
    """Custom validation error"""
    pass

class PartNumberValidator:
    """Validates part number format and components"""
    
    def __init__(self):
        # Valid model families
        self.valid_models = {
            'LS2000', 'LS2100', 'LS6000', 'LS7000', 'LS7000/2',
            'LS8000', 'LS8000/2', 'LT9000', 'FS10000', 'LS7500', 'LS8500'
        }
        
        # Valid voltage formats
        self.voltage_patterns = [
            r'^\d+VAC$',  # 115VAC, 240VAC
            r'^\d+VDC$',  # 24VDC, 12VDC
        ]
        
        # Valid material codes
        self.valid_materials = {'S', 'H', 'U', 'T', 'TS', 'C', 'CPVC'}
        
        # Valid option codes (BP removed - now handled as degree format)
        # TEF and PEEK removed - handled as insulators via XINS format
        self.valid_options = {
            'XSP', 'VR', 'CP', 'SSTAG', 'SSHSE', 'VRHSE', '3/4"OD'
        }
        
        # Valid insulator codes
        self.valid_insulators = {'TEF', 'UHMWPE', 'U', 'DEL', 'PEEK', 'CER'}
    
    def validate_format(self, part_number: str) -> List[str]:
        """Validate basic part number format"""
        errors = []
        
        if not part_number:
            errors.append("Part number cannot be empty")
            return errors
        
        if len(part_number) > MAX_PART_NUMBER_LENGTH:
            errors.append(f"Part number too long (max {MAX_PART_NUMBER_LENGTH} characters)")
        
        # Check for invalid characters
        if not re.match(r'^[A-Z0-9\-"/\.]+$', part_number.upper()):
            errors.append("Part number contains invalid characters")
        
        # Check basic structure
        parts = part_number.split('-')
        if len(parts) < 4:
            errors.append("Part number must have at least MODEL-VOLTAGE-MATERIAL-LENGTH")
        
        return errors
    
    def validate_model(self, model: str) -> List[str]:
        """Validate model number"""
        errors = []
        
        if not model:
            errors.append("Model number is required")
        elif model not in self.valid_models:
            errors.append(f"Unknown model: {model}. Valid models: {', '.join(sorted(self.valid_models))}")
        
        return errors
    
    def validate_voltage(self, voltage: str) -> List[str]:
        """Validate voltage specification"""
        errors = []
        
        if not voltage:
            errors.append("Voltage is required")
            return errors
        
        # Check voltage format
        valid_format = any(re.match(pattern, voltage) for pattern in self.voltage_patterns)
        if not valid_format:
            errors.append(f"Invalid voltage format: {voltage}. Expected format: 115VAC, 24VDC, etc.")
        
        return errors
    
    def validate_material(self, material: str) -> List[str]:
        """Validate material code"""
        errors = []
        
        if not material:
            errors.append("Material code is required")
        elif material not in self.valid_materials:
            errors.append(f"Unknown material: {material}. Valid materials: {', '.join(sorted(self.valid_materials))}")
        
        return errors
    
    def validate_length(self, length_str: str) -> Tuple[List[str], float]:
        """Validate probe length"""
        errors = []
        length = 0.0
        
        if not length_str:
            errors.append("Probe length is required")
            return errors, length
        
        # Extract numeric value from length string (remove quotes, etc.)
        clean_length = re.sub(r'[^0-9\.]', '', length_str)
        
        try:
            length = float(clean_length)
        except ValueError:
            errors.append(f"Invalid length format: {length_str}")
            return errors, length
        
        if length < MIN_PROBE_LENGTH:
            errors.append(f"Probe length too short (min {MIN_PROBE_LENGTH}\")")
        elif length > MAX_PROBE_LENGTH:
            errors.append(f"Probe length too long (max {MAX_PROBE_LENGTH}\")")
        
        return errors, length
    
    def validate_options(self, options: List[str]) -> List[str]:
        """Validate option codes"""
        errors = []
        
        for option in options:
            # Check for bent probe degree format
            if option.endswith('DEG'):
                try:
                    degree = int(option[:-3])
                    if not (0 <= degree <= 180):
                        errors.append(f"Invalid bent probe degree: {option}. Must be between 0 and 180 degrees.")
                except ValueError:
                    errors.append(f"Invalid bent probe format: {option}. Expected format: 90DEG")
            elif option not in self.valid_options:
                errors.append(f"Unknown option: {option}. Valid options: {', '.join(sorted(self.valid_options))} or XDEG format for bent probe")
        
        return errors
    
    def validate_insulator(self, insulator_code: str) -> List[str]:
        """Validate insulator code"""
        errors = []
        
        if insulator_code and insulator_code not in self.valid_insulators:
            errors.append(f"Unknown insulator: {insulator_code}. Valid insulators: {', '.join(sorted(self.valid_insulators))}")
        
        return errors

class CompatibilityChecker:
    """Checks compatibility between different part number components"""
    
    def __init__(self):
        # Model-specific material restrictions
        self.model_material_restrictions = {
            'LS2000': {'S', 'H', 'U', 'T', 'TS'},
            'LS2100': {'S', 'H', 'TS'},
            'LS6000': {'S', 'H', 'TS', 'CPVC'},
            'LS7000': {'S', 'H', 'TS', 'CPVC'},
            'LS7000/2': {'H', 'TS'},  # Must use Halar in conductive liquids
            'LS8000': {'S', 'H', 'TS'},
            'LS8000/2': {'H', 'S', 'TS'},
            'LT9000': {'H', 'TS'},
            'FS10000': {'S'},
        }
        
        # Model-specific voltage restrictions
        self.model_voltage_restrictions = {
            'LS2000': {'115VAC', '24VDC'},  # 12VDC and 240VAC not available
            'LS2100': {'24VDC'},  # Only 24VDC (16-32V range)
            'LS6000': {'115VAC', '12VDC', '24VDC', '240VAC'},
            'LS7000': {'115VAC', '12VDC', '24VDC', '240VAC'},
            'LS7000/2': {'115VAC', '12VDC', '24VDC', '240VAC'},
            'LS8000': {'115VAC', '12VDC', '24VDC', '240VAC'},
            'LS8000/2': {'115VAC', '12VDC', '24VDC', '240VAC'},
            'LT9000': {'115VAC', '24VDC', '230VAC'},
            'FS10000': {'115VAC', '12VDC', '24VDC', '240VAC'},
        }
        
        # Incompatible option combinations
        self.incompatible_options = {
            'CP': ['BENT_PROBE'],  # Cable probe can't be bent (handled specially)
        }
        
        # Model-specific option restrictions
        self.model_option_restrictions = {
            'XSP': ['LS2000'],  # Extra static protection only for LS2000
            'SSHSE': ['LS7000'],  # Stainless steel housing only for LS7000
            '3/4"OD': ['ALL'],  # 3/4" diameter probe available for all models
        }
    
    def check_model_material_compatibility(self, model: str, material: str) -> List[str]:
        """Check if material is compatible with model"""
        errors = []
        
        if model in self.model_material_restrictions:
            allowed_materials = self.model_material_restrictions[model]
            if material not in allowed_materials:
                errors.append(f"Material {material} not compatible with {model}. Allowed: {', '.join(sorted(allowed_materials))}")
        
        return errors
    
    def check_model_voltage_compatibility(self, model: str, voltage: str) -> List[str]:
        """Check if voltage is compatible with model"""
        errors = []
        
        if model in self.model_voltage_restrictions:
            allowed_voltages = self.model_voltage_restrictions[model]
            if voltage not in allowed_voltages:
                errors.append(f"Voltage {voltage} not compatible with {model}. Allowed: {', '.join(sorted(allowed_voltages))}")
        
        return errors
    
    def check_option_compatibility(self, options: List[str]) -> List[str]:
        """Check for incompatible option combinations"""
        errors = []
        
        # Check for cable probe + bent probe incompatibility
        has_cable_probe = 'CP' in options
        has_bent_probe = any(opt.endswith('DEG') for opt in options)
        
        if has_cable_probe and has_bent_probe:
            bent_probe_options = [opt for opt in options if opt.endswith('DEG')]
            for bent_opt in bent_probe_options:
                errors.append(f"Options CP and {bent_opt} are incompatible (cable probe cannot be bent)")
        
        # Check other incompatible combinations
        for option in options:
            if option in self.incompatible_options:
                incompatible = self.incompatible_options[option]
                for other_option in options:
                    if other_option in incompatible:
                        errors.append(f"Options {option} and {other_option} are incompatible")
        
        return errors
    
    def check_model_option_compatibility(self, model: str, options: List[str]) -> List[str]:
        """Check if options are compatible with model"""
        errors = []
        
        for option in options:
            if option in self.model_option_restrictions:
                allowed_models = self.model_option_restrictions[option]
                if model not in allowed_models:
                    errors.append(f"Option {option} not available for {model}. Available for: {', '.join(allowed_models)}")
        
        return errors
    
    def check_length_material_compatibility(self, material: str, length: float) -> List[str]:
        """Check length limitations for specific materials"""
        warnings = []
        
        if material == 'H' and length > HALAR_MAX_LENGTH:
            warnings.append(f"Halar coating limited to {HALAR_MAX_LENGTH}\" - consider Teflon Sleeve for longer probes")
        
        return warnings

class CustomerDataValidator:
    """Validates customer information"""
    
    @staticmethod
    def validate_customer_name(name: str) -> List[str]:
        """Validate customer name"""
        errors = []
        
        if not name or not name.strip():
            errors.append("Customer name is required")
        elif len(name) > MAX_CUSTOMER_NAME_LENGTH:
            errors.append(f"Customer name too long (max {MAX_CUSTOMER_NAME_LENGTH} characters)")
        
        return errors
    
    @staticmethod
    def validate_email(email: str) -> List[str]:
        """Validate email address"""
        errors = []
        
        if email:  # Email is optional
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors.append("Invalid email format")
        
        return errors
    
    @staticmethod
    def validate_phone(phone: str) -> List[str]:
        """Validate phone number"""
        errors = []
        
        if phone:  # Phone is optional
            # Remove formatting characters
            clean_phone = re.sub(r'[^\d]', '', phone)
            if len(clean_phone) < 10:
                errors.append("Phone number too short")
            elif len(clean_phone) > 15:
                errors.append("Phone number too long")
        
        return errors

class QuoteValidator:
    """Validates complete quote data"""
    
    @staticmethod
    def validate_quantity(quantity: int) -> List[str]:
        """Validate quantity"""
        errors = []
        
        if quantity <= 0:
            errors.append("Quantity must be positive")
        elif quantity > 10000:
            errors.append("Quantity too large (max 10,000)")
        
        return errors
    
    @staticmethod
    def validate_pricing(pricing: Dict[str, Any]) -> List[str]:
        """Validate pricing data"""
        errors = []
        
        if not pricing:
            errors.append("Pricing data is missing")
            return errors
        
        total_price = pricing.get('total_price', 0)
        if total_price < 0:
            errors.append("Total price cannot be negative")
        elif total_price > 1000000:
            errors.append("Total price seems unreasonably high")
        
        return errors

# Main validation function
def validate_complete_part_number(part_number: str, parsed_data: Optional[Dict[str, Any]] = None) -> Tuple[List[str], List[str]]:
    """
    Comprehensive validation of a complete part number
    Returns: (errors, warnings)
    """
    errors = []
    warnings = []
    
    # Initialize validators
    pn_validator = PartNumberValidator()
    compat_checker = CompatibilityChecker()
    
    # Basic format validation
    format_errors = pn_validator.validate_format(part_number)
    errors.extend(format_errors)
    
    if errors:  # Don't continue if basic format is invalid
        return errors, warnings
    
    # Parse basic components if not provided
    if not parsed_data:
        parts = part_number.split('-')
        if len(parts) >= 4:
            parsed_data = {
                'model': parts[0],
                'voltage': parts[1],
                'probe_material': parts[2],
                'probe_length': parts[3],
                'options': parts[4:] if len(parts) > 4 else []
            }
        else:
            return errors + ["Invalid part number format"], warnings
    
    # Validate individual components
    errors.extend(pn_validator.validate_model(parsed_data.get('model', '')))
    errors.extend(pn_validator.validate_voltage(parsed_data.get('voltage', '')))
    errors.extend(pn_validator.validate_material(parsed_data.get('probe_material', '')))
    
    length_errors, length_value = pn_validator.validate_length(parsed_data.get('probe_length', ''))
    errors.extend(length_errors)
    
    # Compatibility checks
    model = parsed_data.get('model', '')
    voltage = parsed_data.get('voltage', '')
    material = parsed_data.get('probe_material', '')
    options = parsed_data.get('options', [])
    
    errors.extend(compat_checker.check_model_material_compatibility(model, material))
    errors.extend(compat_checker.check_model_voltage_compatibility(model, voltage))
    errors.extend(compat_checker.check_option_compatibility(options))
    errors.extend(compat_checker.check_model_option_compatibility(model, options))
    
    # Length warnings
    warnings.extend(compat_checker.check_length_material_compatibility(material, length_value))
    
    return errors, warnings
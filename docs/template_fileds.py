"""
Template Field Mappings for RTF Quote Templates

This module defines all the template variables that need to be replaced
when generating quotes from RTF templates.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class QuoteTemplateFields:
    """
    Template fields for quote generation.
    Each field corresponds to a placeholder in the RTF templates.
    """
    
    # Quote Header Information
    date: str
    customer_name: str  # Maps to CUSTOMER/CUSTOMER NAME/COMPANY
    attention_name: str  # Maps to ATTN field
    quote_number: str    # Maps to Quote #/Quote#
    
    # Product Information
    part_number: str     # Full part number (e.g., "LS2000-115VAC-H-12")
    quantity: str        # Quantity (e.g., "1", "5", "10")
    unit_price: str      # Price without $ symbol
    supply_voltage: str  # Operating voltage (e.g., "115VAC", "24VDC")
    
    # Technical Specifications
    probe_length: str           # In inches (e.g., "12")
    process_connection_size: str # Connection size (e.g., "¾", "1")
    insulator_material: str     # Material (e.g., "Teflon", "DELRIN", "UHMPE")
    insulator_length: str       # Length spec (e.g., "4")
    probe_material: str         # Material (e.g., "316SS", "HALAR")
    probe_diameter: str         # Diameter (e.g., "½")
    max_temperature: str        # Temperature rating (e.g., "450 F", "180 F")
    max_pressure: str          # Pressure rating (e.g., "300 PSI", "1500 PSI")
    
    # Model-Specific Fields (Optional)
    cable_length: Optional[str] = None      # For models with cable
    flange_size: Optional[str] = None       # For flanged models
    sensor_type: Optional[str] = None       # Full Ring/Partial Ring
    output_type: Optional[str] = None       # Relay/current output specs
    enclosure_option: Optional[str] = None  # Optional enclosure details
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for template replacement."""
        return {
            # Header fields
            'DATE': self.date,
            'CUSTOMER': self.customer_name,
            'CUSTOMER NAME': self.customer_name,
            'COMPANY': self.customer_name,
            'ATTN': self.attention_name,
            'QUOTE_NUMBER': self.quote_number,
            'Quote #': self.quote_number,
            'Quote#': self.quote_number,
            
            # Product fields
            'PART_NUMBER': self.part_number,
            'QUANTITY': self.quantity,
            'PRICE': self.unit_price,
            'SUPPLY_VOLTAGE': self.supply_voltage,
            
            # Technical specs
            'PROBE_LENGTH': self.probe_length,
            'PROCESS_CONNECTION_SIZE': self.process_connection_size,
            'INSULATOR_MATERIAL': self.insulator_material,
            'INSULATOR_LENGTH': self.insulator_length,
            'PROBE_MATERIAL': self.probe_material,
            'PROBE_DIAMETER': self.probe_diameter,
            'MAX_TEMPERATURE': self.max_temperature,
            'MAX_PRESSURE': self.max_pressure,
            
            # Optional fields
            'CABLE_LENGTH': self.cable_length,
            'FLANGE_SIZE': self.flange_size,
            'SENSOR_TYPE': self.sensor_type,
            'OUTPUT_TYPE': self.output_type,
            'ENCLOSURE_OPTION': self.enclosure_option,
        }

# Template placeholder patterns that need replacement
TEMPLATE_PATTERNS = {
    # Basic text replacements
    'DATE': r'\bDATE\b',
    'CUSTOMER': r'\b(?:CUSTOMER|CUSTOMER NAME|COMPANY)\b',
    'ATTN': r'\bATTN:\s*',
    'QUOTE_NUMBER': r'\b(?:Quote #|Quote#)\s*',
    
    # Part number patterns (various XXXX patterns)
    'PART_NUMBER_PATTERNS': [
        r'FS10000-115VAC-S-xx',
        r'LS2000-XXXX-[HS]-XX',
        r'LS2100-24VDC-[HS]-XX',
        r'LS6000-XXXXX-[HS]-XX',
        r'LS7000(?:/2)?-XXXXXX-[HS]-XX',
        r'LS7500-XXXXXXXX-(?:FP|PR)-XX-150#-(?:FR|PR)',
        r'LS8000(?:/2)?-(?:XXXXXX|xxx)-[HS]-(?:XX|xx)',
        r'LS8500-XXXXXXXX-(?:FP|PR)-XX-150#',
        r'LT9000-XXXX-(?:H|TS)-XX',
    ],
    
    # Supply voltage patterns
    'SUPPLY_VOLTAGE_PATTERN': r'Supply Voltage:\s*(?:XXXX|xxx|\s*$)',
    
    # Probe length patterns
    'PROBE_LENGTH_PATTERNS': [
        r'x XX"',  # Standard XX" pattern
        r'xx"',    # lowercase xx" pattern
    ],
    
    # Price patterns
    'PRICE_PATTERN': r'\$\s*(?:EACH|xxx|\s+EACH)',
}

# Model-specific template field requirements
MODEL_TEMPLATE_FIELDS = {
    'FS10000S': {
        'required': ['date', 'customer_name', 'attention_name', 'quote_number', 
                    'part_number', 'unit_price', 'supply_voltage', 'probe_length'],
        'optional': ['cable_length']
    },
    'LS2000H': {
        'required': ['date', 'customer_name', 'attention_name', 'quote_number',
                    'part_number', 'unit_price', 'supply_voltage', 'probe_length',
                    'insulator_material', 'probe_material', 'max_temperature'],
        'optional': []
    },
    'LS2000S': {
        'required': ['date', 'customer_name', 'attention_name', 'quote_number',
                    'part_number', 'unit_price', 'supply_voltage', 'probe_length',
                    'insulator_material', 'probe_material', 'max_temperature'],
        'optional': []
    },
    # Add other models as needed...
}

def get_template_fields_for_model(model: str) -> Dict[str, list]:
    """Get required and optional fields for a specific model."""
    return MODEL_TEMPLATE_FIELDS.get(model, {
        'required': ['date', 'customer_name', 'attention_name', 'quote_number',
                    'part_number', 'unit_price', 'supply_voltage'],
        'optional': []
    })
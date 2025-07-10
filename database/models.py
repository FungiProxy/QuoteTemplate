"""
Database Models for Babbitt Quote Generator
Defines data structures and validation for database tables
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

@dataclass
class ProductModel:
    """Product model data structure"""
    id: Optional[int] = None
    model_number: str = ""
    description: str = ""
    base_price: float = 0.0
    base_length: float = 10.0
    default_voltage: str = ""
    default_material: str = ""
    default_insulator: str = ""
    max_temp_rating: Optional[str] = None
    max_pressure: Optional[str] = None
    housing_type: Optional[str] = None
    output_type: Optional[str] = None
    application_notes: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Material:
    """Material data structure"""
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    description: Optional[str] = None
    base_price_adder: float = 0.0
    length_adder_per_foot: float = 0.0
    length_adder_per_inch: float = 0.0
    nonstandard_length_surcharge: float = 0.0
    max_length_with_coating: Optional[float] = None
    compatible_models: Optional[str] = None  # JSON array
    created_at: Optional[datetime] = None

@dataclass
class Option:
    """Option data structure"""
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    description: Optional[str] = None
    price: float = 0.0
    price_type: str = "fixed"
    category: Optional[str] = None
    compatible_models: Optional[str] = None  # JSON array
    exclusions: Optional[str] = None  # JSON array
    created_at: Optional[datetime] = None

@dataclass
class Insulator:
    """Insulator data structure"""
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    description: Optional[str] = None
    price_adder: float = 0.0
    max_temp_rating: Optional[str] = None
    standard_length: float = 4.0
    compatible_models: Optional[str] = None  # JSON array
    created_at: Optional[datetime] = None

@dataclass
class Voltage:
    """Voltage option data structure"""
    id: Optional[int] = None
    model_family: str = ""
    voltage: str = ""
    price_adder: float = 0.0
    is_default: bool = False
    created_at: Optional[datetime] = None

@dataclass
class LengthPricing:
    """Length pricing rule data structure"""
    id: Optional[int] = None
    material_code: str = ""
    model_family: str = ""
    base_length: float = 10.0
    adder_per_foot: float = 0.0
    adder_per_inch: float = 0.0
    nonstandard_surcharge: float = 0.0
    nonstandard_threshold: float = 0.0
    created_at: Optional[datetime] = None

@dataclass
class Quote:
    """Quote data structure"""
    id: Optional[int] = None
    quote_number: str = ""
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    status: str = "draft"
    total_price: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class QuoteItem:
    """Quote item data structure"""
    id: Optional[int] = None
    quote_id: int = 0
    part_number: str = ""
    description: Optional[str] = None
    quantity: int = 1
    unit_price: float = 0.0
    total_price: float = 0.0
    created_at: Optional[datetime] = None

@dataclass
class ParsedPartNumber:
    """Parsed part number data structure"""
    original_part_number: str = ""
    model: str = ""
    voltage: str = ""
    probe_material: str = ""
    probe_length: float = 10.0
    options: List[Dict[str, str]] = field(default_factory=list)
    insulator: Optional[Dict[str, Any]] = None
    process_connection: Optional[Dict[str, str]] = None
    calculated_specs: Dict[str, Any] = field(default_factory=dict)
    pricing: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

@dataclass 
class QuoteData:
    """Complete quote data structure"""
    part_number: str = ""
    model: str = ""
    voltage: str = ""
    probe_material: str = ""
    probe_length: float = 10.0
    process_connection: str = ""
    insulator: str = ""
    housing: str = ""
    output: str = ""
    max_temperature: str = ""
    max_pressure: str = ""
    options: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    total_price: float = 0.0
    base_price: float = 0.0
    length_cost: float = 0.0
    length_surcharge: float = 0.0
    option_cost: float = 0.0
    insulator_cost: float = 0.0
    price_breakdown: List[str] = field(default_factory=list)

@dataclass
class Employee:
    """Employee data structure"""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    work_email: str = ""
    work_phone: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Helper functions for model operations
def dict_to_product_model(data: Dict[str, Any]) -> ProductModel:
    """Convert dictionary to ProductModel"""
    return ProductModel(
        id=data.get('id'),
        model_number=data.get('model_number', ''),
        description=data.get('description', ''),
        base_price=data.get('base_price', 0.0),
        base_length=data.get('base_length', 10.0),
        default_voltage=data.get('default_voltage', ''),
        default_material=data.get('default_material', ''),
        default_insulator=data.get('default_insulator', ''),
        max_temp_rating=data.get('max_temp_rating'),
        max_pressure=data.get('max_pressure'),
        housing_type=data.get('housing_type'),
        output_type=data.get('output_type'),
        application_notes=data.get('application_notes'),
        created_at=data.get('created_at')
    )

def dict_to_material(data: Dict[str, Any]) -> Material:
    """Convert dictionary to Material"""
    return Material(
        id=data.get('id'),
        code=data.get('code', ''),
        name=data.get('name', ''),
        description=data.get('description'),
        base_price_adder=data.get('base_price_adder', 0.0),
        length_adder_per_foot=data.get('length_adder_per_foot', 0.0),
        length_adder_per_inch=data.get('length_adder_per_inch', 0.0),
        nonstandard_length_surcharge=data.get('nonstandard_length_surcharge', 0.0),
        max_length_with_coating=data.get('max_length_with_coating'),
        compatible_models=data.get('compatible_models'),
        created_at=data.get('created_at')
    )

def dict_to_option(data: Dict[str, Any]) -> Option:
    """Convert dictionary to Option"""
    return Option(
        id=data.get('id'),
        code=data.get('code', ''),
        name=data.get('name', ''),
        description=data.get('description'),
        price=data.get('price', 0.0),
        price_type=data.get('price_type', 'fixed'),
        category=data.get('category'),
        compatible_models=data.get('compatible_models'),
        exclusions=data.get('exclusions'),
        created_at=data.get('created_at')
    )

def dict_to_employee(data: Dict[str, Any]) -> Employee:
    """Convert dictionary to Employee"""
    return Employee(
        id=data.get('id'),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        work_email=data.get('work_email', ''),
        work_phone=data.get('work_phone'),
        is_active=data.get('is_active', True),
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )

# Validation functions
def validate_part_number(part_number: str) -> List[str]:
    """Validate part number format"""
    errors = []
    
    if not part_number:
        errors.append("Part number cannot be empty")
        return errors
    
    if len(part_number) > 100:
        errors.append("Part number too long (max 100 characters)")
    
    # Check basic format: MODEL-VOLTAGE-MATERIAL-LENGTH
    parts = part_number.split('-')
    if len(parts) < 4:
        errors.append("Part number must have at least 4 components (MODEL-VOLTAGE-MATERIAL-LENGTH)")
    
    return errors

def validate_customer_name(name: str) -> List[str]:
    """Validate customer name"""
    errors = []
    
    if not name or not name.strip():
        errors.append("Customer name cannot be empty")
    
    if len(name) > 100:
        errors.append("Customer name too long (max 100 characters)")
    
    return errors

def validate_pricing_data(pricing: Dict[str, Any]) -> List[str]:
    """Validate pricing calculation results"""
    errors = []
    
    if not pricing:
        errors.append("Pricing data is missing")
        return errors
    
    total_price = pricing.get('total_price', 0)
    if total_price < 0:
        errors.append("Total price cannot be negative")
    
    base_price = pricing.get('base_price', 0)
    if base_price < 0:
        errors.append("Base price cannot be negative")
    
    return errors 
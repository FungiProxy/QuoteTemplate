"""
Helper Utility Functions for Babbitt Quote Generator
Provides common utility functions used throughout the application
"""

import re
from typing import Optional, Union, Any
from decimal import Decimal, InvalidOperation
import unicodedata

def format_currency(amount: Union[float, int, Decimal], 
                   currency_symbol: str = "$", 
                   decimal_places: int = 2) -> str:
    """
    Format a numeric amount as currency
    
    Args:
        amount: The numeric amount to format
        currency_symbol: Currency symbol to use (default: "$")
        decimal_places: Number of decimal places (default: 2)
    
    Returns:
        Formatted currency string
    """
    try:
        if isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        elif not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        # Format with specified decimal places
        format_str = f"{{:.{decimal_places}f}}"
        formatted = format_str.format(float(amount))
        
        return f"{currency_symbol}{formatted}"
    except (InvalidOperation, ValueError, TypeError):
        return f"{currency_symbol}0.00"

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits_only) <= 15

def clean_part_number(part_number: str) -> str:
    """
    Clean and normalize part number format
    
    Args:
        part_number: Raw part number string
    
    Returns:
        Cleaned part number
    """
    if not part_number:
        return ""
    
    # Remove leading/trailing whitespace
    cleaned = part_number.strip()
    
    # Convert to uppercase
    cleaned = cleaned.upper()
    
    # Remove multiple spaces and replace with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Normalize unicode characters
    cleaned = unicodedata.normalize('NFKD', cleaned)
    
    return cleaned

def extract_numeric_value(value_str: str) -> Optional[float]:
    """
    Extract numeric value from a string
    
    Args:
        value_str: String containing numeric value
    
    Returns:
        Extracted numeric value or None if not found
    """
    if not value_str:
        return None
    
    # Remove common non-numeric characters but keep decimal point
    cleaned = re.sub(r'[^\d\.]', '', str(value_str))
    
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None

def safe_float_convert(value: Any, default: float = 0.0) -> float:
    """
    Safely convert value to float with default fallback
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Float value or default
    """
    try:
        if value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int_convert(value: Any, default: int = 0) -> int:
    """
    Safely convert value to int with default fallback
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Integer value or default
    """
    try:
        if value is None:
            return default
        return int(float(value))  # Convert through float to handle decimal strings
    except (ValueError, TypeError):
        return default

def normalize_voltage(voltage: str) -> str:
    """
    Normalize voltage string format
    
    Args:
        voltage: Raw voltage string
    
    Returns:
        Normalized voltage string
    """
    if not voltage:
        return ""
    
    # Clean the input
    cleaned = voltage.strip().upper()
    
    # Extract numeric part and voltage type
    match = re.match(r'(\d+)\s*(V?A?C?D?C?)', cleaned)
    if match:
        number, suffix = match.groups()
        
        # Normalize suffix
        if suffix in ['V', 'VAC', 'AC']:
            suffix = 'VAC'
        elif suffix in ['VDC', 'DC']:
            suffix = 'VDC'
        elif not suffix:
            # Default to VAC if no suffix
            suffix = 'VAC'
        
        return f"{number}{suffix}"
    
    return cleaned

def normalize_length(length: str) -> str:
    """
    Normalize length string format
    
    Args:
        length: Raw length string
    
    Returns:
        Normalized length string
    """
    if not length:
        return ""
    
    # Remove quotes and normalize
    cleaned = length.strip().replace('"', '').replace("'", "")
    
    # If it's just a number, add inch symbol
    if re.match(r'^\d+(\.\d+)?$', cleaned):
        return f'{cleaned}"'
    
    return cleaned

def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to maximum length with optional suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if not text or len(text) <= max_length:
        return text
    
    if len(suffix) >= max_length:
        return text[:max_length]
    
    return text[:max_length - len(suffix)] + suffix

def camel_to_snake(name: str) -> str:
    """
    Convert CamelCase to snake_case
    
    Args:
        name: CamelCase string
    
    Returns:
        snake_case string
    """
    # Insert underscores before uppercase letters
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Insert underscores before uppercase letters preceded by lowercase
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(name: str) -> str:
    """
    Convert snake_case to CamelCase
    
    Args:
        name: snake_case string
    
    Returns:
        CamelCase string
    """
    components = name.split('_')
    return ''.join(word.capitalize() for word in components)

def is_numeric(value: str) -> bool:
    """
    Check if string represents a numeric value
    
    Args:
        value: String to check
    
    Returns:
        True if numeric, False otherwise
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def clean_filename(filename: str) -> str:
    """
    Clean filename by removing/replacing invalid characters
    
    Args:
        filename: Raw filename
    
    Returns:
        Clean filename safe for filesystem
    """
    if not filename:
        return "unnamed"
    
    # Replace problematic characters
    cleaned = filename.replace('/', '_')
    cleaned = cleaned.replace('\\', '_')
    cleaned = cleaned.replace(':', '_')
    cleaned = cleaned.replace('*', '_')
    cleaned = cleaned.replace('?', '_')
    cleaned = cleaned.replace('"', '_')
    cleaned = cleaned.replace('<', '_')
    cleaned = cleaned.replace('>', '_')
    cleaned = cleaned.replace('|', '_')
    
    # Remove multiple underscores
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Remove leading/trailing underscores and whitespace
    cleaned = cleaned.strip('_').strip()
    
    return cleaned if cleaned else "unnamed"

def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Filename
    
    Returns:
        File extension (with dot) or empty string
    """
    if not filename or '.' not in filename:
        return ""
    
    return filename.rsplit('.', 1)[-1].lower()

def ensure_file_extension(filename: str, extension: str) -> str:
    """
    Ensure filename has the specified extension
    
    Args:
        filename: Original filename
        extension: Required extension (with or without dot)
    
    Returns:
        Filename with correct extension
    """
    if not filename:
        return f"unnamed.{extension.lstrip('.')}"
    
    # Normalize extension
    if not extension.startswith('.'):
        extension = f".{extension}"
    
    # Check if already has correct extension
    if filename.lower().endswith(extension.lower()):
        return filename
    
    # Add extension
    return f"{filename}{extension}"

def pluralize(word: str, count: int) -> str:
    """
    Simple pluralization helper
    
    Args:
        word: Base word
        count: Count to determine plural
    
    Returns:
        Pluralized word if count != 1
    """
    if count == 1:
        return word
    
    # Simple pluralization rules
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    else:
        return word + 's'

def batch_process(items: list, batch_size: int = 100):
    """
    Process items in batches
    
    Args:
        items: List of items to process
        batch_size: Size of each batch
    
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def deep_get(dictionary: dict, keys: str, default: Any = None) -> Any:
    """
    Get nested dictionary value using dot notation
    
    Args:
        dictionary: Dictionary to search
        keys: Dot-separated keys (e.g., "user.profile.name")
        default: Default value if key not found
    
    Returns:
        Value at nested key or default
    """
    try:
        for key in keys.split('.'):
            dictionary = dictionary[key]
        return dictionary
    except (KeyError, TypeError):
        return default

def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flatten nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for nested keys
    
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items) 

def format_phone_number(phone: str) -> str:
    """
    Format phone number to (xxx) xxx-xxxx format
    
    Args:
        phone: Phone number string (can be digits only or already formatted)
    
    Returns:
        Formatted phone number string
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # If we have exactly 10 digits, format as (xxx) xxx-xxxx
    if len(digits_only) == 10:
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    
    # If we have 11 digits starting with 1, format as 1 (xxx) xxx-xxxx
    elif len(digits_only) == 11 and digits_only.startswith('1'):
        return f"1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
    
    # For other lengths, return the original input
    return phone

def unformat_phone_number(phone: str) -> str:
    """
    Remove formatting from phone number to get digits only
    
    Args:
        phone: Formatted phone number string
    
    Returns:
        Digits only phone number string
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    return re.sub(r'\D', '', phone) 
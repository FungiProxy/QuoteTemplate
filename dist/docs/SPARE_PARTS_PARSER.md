# Spare Parts Parser Documentation

## Overview

The spare parts parser system handles dynamic parsing of spare part numbers with variable components (voltage, length, material, etc.). It translates user-friendly part numbers into database lookups and pricing calculations.

## Architecture

### Core Components

1. **`SparePartsParser`** (`core/spare_parts_parser.py`)
   - Parses user input part numbers
   - Validates components (voltage, material, length)
   - Maps to database entries
   - Calculates dynamic pricing

2. **`SparePartsManager`** (`core/spare_parts_manager.py`)
   - Integrates with the parser
   - Manages database operations
   - Handles quote generation
   - Formats output for display

## Part Number Formats

### Electronics
- **Input Format**: `{MODEL}-{VOLTAGE}-E`
- **Example**: `LS2000-115VAC-E`
- **Maps to**: `LS2000-ELECTRONICS`
- **Valid Voltages**: 115VAC, 24VDC, 230VAC, 12VDC

### Probe Assemblies
- **Input Format**: `{MODEL}-{MATERIAL}-{LENGTH}"`
- **Example**: `LS7000-S-12"`
- **Maps to**: `LS7000-S-PROBE-ASSEMBLY-12`
- **Valid Materials**: S, H, U, T, TS, CPVC, C
- **Length Pricing**: Automatic calculation for > base length

### Power Supplies
- **Input Format**: `{MODEL}-{VOLTAGE}-PS`
- **Example**: `LS7000-115VAC-PS`
- **Maps to**: `LS7000-PS-POWER-SUPPLY`

### Receiver Cards
- **Input Format**: `{MODEL}-{VOLTAGE}-R`
- **Example**: `LS8000-24VDC-R`
- **Maps to**: `LS8000-R-RECEIVER-CARD`

### Transmitters
- **Input Format**: `{MODEL}-{SPECS}-T`
- **Example**: `LS8000-SIZE-SENSITIVITY-T`
- **Maps to**: `LS8000-T-TRANSMITTER`
- **Note**: Specs can be flexible (size, sensitivity, or both)

### Cards
- **Sensing Card**: `{MODEL}-SC` → `{MODEL}-SC-SENSING-CARD`
- **Dual Point**: `{MODEL}-DP` → `{MODEL}-DP-DUAL-POINT-CARD`
- **Plugin Card**: `{MODEL}-MA` → `{MODEL}-MA-PLUGIN-CARD`

### BB Power Supplies
- **Input Format**: `{MODEL}-{VOLTAGE}-BB`
- **Example**: `LT9000-24VDC-BB`
- **Maps to**: `LT9000-BB-POWER-SUPPLY`

### Fuses
- **Input Format**: `{MODEL}-FUSE`
- **Example**: `LS7000-FUSE` or `LT9000-FUSE`
- **Pricing**: $10.00 for most models, $20.00 for LT9000
- **Maps to**: Generic fuse entry with model-specific pricing

### Housing
- **Input Format**: `{MODEL}-HOUSING`
- **Example**: `LS2000-HOUSING`
- **Maps to**: `{MODEL}-HOUSING`

## Usage Examples

### Basic Parsing
```python
from core.spare_parts_parser import SparePartsParser

parser = SparePartsParser()
result = parser.parse_spare_part_number("LS2000-115VAC-E")

if result['parsed_successfully']:
    print(f"Part type: {result['part_type']}")
    print(f"Variables: {result['variables']}")
    print(f"Database match: {result['database_match']['name']}")
    print(f"Price: ${result['pricing_info']['calculated_price']:.2f}")
```

### Quote Generation
```python
from core.spare_parts_manager import SparePartsManager

manager = SparePartsManager()
quote = manager.parse_and_quote_spare_part("LS7000-S-12\"", quantity=2)

if quote['success']:
    print(f"Unit price: ${quote['unit_price']:.2f}")
    print(f"Total price: ${quote['total_price']:.2f}")
    print(f"Description: {quote['line_item_description']}")
```

## Dynamic Pricing

### Probe Assembly Length Pricing
- **Stainless Steel (S)**: $45/foot for length > 10"
- **Halar (H)**: $110/foot for length > 10"
- **Other materials**: Base price only

### Calculation Example
```python
# LS7000-S-12" (12-inch stainless steel probe)
base_price = 280.00  # From database
additional_length = 12 - 10 = 2 inches
additional_cost = 2 * (45.00 / 12) = $7.50
total_price = 280.00 + 7.50 = $287.50
```

## Error Handling

### Validation Errors
- Invalid voltage specifications
- Unrecognized material codes
- Invalid length formats
- Unusual length values (warnings)

### Database Errors
- Connection failures
- Missing part entries
- Invalid part numbers

### Example Error Response
```python
{
    'parsed_successfully': False,
    'errors': ['Invalid voltage: 999VAC'],
    'warnings': ['Unusual material code: XYZ'],
    'suggestions': ['LS7000-115VAC-PS (or 24VDC, 230VAC, 12VDC)']
}
```

## Integration Points

### With Main Quote System
```python
# In main quote processing
spare_parts_manager = SparePartsManager()
spare_result = spare_parts_manager.parse_and_quote_spare_part(part_number)

if spare_result['success']:
    quote_items.append({
        'description': spare_result['line_item_description'],
        'unit_price': spare_result['unit_price'],
        'quantity': spare_result['quantity'],
        'total_price': spare_result['total_price']
    })
```

### With GUI
```python
# In GUI part number entry
def on_part_number_entered(part_number):
    result = manager.parse_and_quote_spare_part(part_number)
    
    if result['success']:
        display_part_info(result)
    else:
        show_error(result['error'])
        if result.get('suggestions'):
            show_suggestions(result['suggestions'])
```

## Database Schema

### Spare Parts Table
```sql
CREATE TABLE spare_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_number TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT,
    compatible_models TEXT, -- JSON array
    notes TEXT,
    requires_voltage_spec BOOLEAN DEFAULT 0,
    requires_length_spec BOOLEAN DEFAULT 0,
    requires_sensitivity_spec BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Categories
- `electronics`: Electronic assemblies
- `probe_assembly`: Probe assemblies  
- `housing`: Housing components
- `card`: Various cards (sensing, dual point, plugin)
- `transmitter`: Transmitter components
- `receiver`: Receiver components
- `fuse`: Fuses
- `cable`: Cable assemblies

## Maintenance

### Adding New Part Types
1. Update `patterns` dictionary in `SparePartsParser`
2. Add parsing logic in `parse_spare_part_number()`
3. Update validation in `_validate_variables()`
4. Add database entries
5. Update documentation

### Updating Pricing Logic
1. Modify `_calculate_spare_part_pricing()` method
2. Update length-based pricing formulas
3. Add new material types if needed
4. Test with various scenarios

## Testing

### Validation Tests
- Valid part number formats
- Invalid part number rejection
- Database connectivity
- Price calculations
- Error handling

### Example Test Cases
```python
test_cases = [
    ("LS2000-115VAC-E", "electronics", True),
    ("LS7000-S-12", "probe_assembly", True),
    ("INVALID-FORMAT", None, False),
    ("LS2000-999VAC-E", "electronics", False),  # Invalid voltage
]
```

## Performance Considerations

- Database connections are managed efficiently
- Parser patterns are pre-compiled
- Validation is performed before database lookups
- Results can be cached for repeated requests

## Future Enhancements

1. **Batch Processing**: Handle multiple part numbers at once
2. **Caching**: Cache frequently accessed parts
3. **Fuzzy Matching**: Suggest similar parts for typos
4. **Validation Rules**: More sophisticated validation
5. **Reporting**: Usage statistics and popular parts 
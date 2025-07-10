# Max Pressure Template Variable Setup

## Overview

The `max_pressure` template variable is **already fully integrated** into your quote template system. It automatically calculates and provides the maximum pressure rating for each part number based on the process connection size and model specifications.

## ✅ Current Status: FULLY WORKING

The `max_pressure` variable is:
- ✅ **Automatically calculated** from part number data
- ✅ **Passed to templates** in all export functions
- ✅ **Available in Word templates** as `{{max_pressure}}`
- ✅ **Available in RTF templates** as `MAX_PRESSURE`
- ✅ **Properly formatted** with units (e.g., "300 PSI", "1500 PSI")

## How It Works

### 1. Automatic Calculation
The system automatically calculates max pressure based on:
- **Process connection size**: 3/4" = 300 PSI, 1" = 300 PSI, 2" = 150 PSI
- **Model specifications**: Different models have different pressure ratings
- **Connection type**: NPT, Flange, Tri-Clamp have different ratings

### 2. Data Flow
```
Part Number → Parser → max_pressure calculated → Template System → {{max_pressure}}
```

### 3. Template Integration
The variable is available in both Word and RTF templates:

**Word Templates (.docx):**
```docx
Maximum Pressure: {{max_pressure}}
Operating Limits: {{max_pressure}}
```

**RTF Templates (.rtf):**
```rtf
Maximum Pressure: MAX_PRESSURE
Operating Limits: MAX_PRESSURE
```

## Template Variable Details

### Variable Name
- **Word Templates**: `{{max_pressure}}`
- **RTF Templates**: `MAX_PRESSURE`

### Example Values
- `300 PSI` - Standard pressure for most models
- `1500 PSI` - High pressure for LS6000/LS7000 series
- `150 PSI` - Lower pressure for some connection sizes

### Default Value
- **Fallback**: `300 PSI` (if calculation fails)

## Usage in Templates

### Word Template Example
```docx
Technical Specifications:
• Maximum Temperature: {{max_temperature}}
• Maximum Pressure: {{max_pressure}}
• Process Connection: {{pc_type}} {{pc_size}}
```

### RTF Template Example
```rtf
Technical Specifications:
• Maximum Temperature: MAX_TEMPERATURE
• Maximum Pressure: MAX_PRESSURE
• Process Connection: PC_TYPE PC_SIZE
```

## Integration Points

### 1. Part Parser (`core/part_parser.py`)
- Calculates max pressure based on connection size
- Stores in parsed data as `max_pressure`

### 2. Quote Generator (`core/quote_generator.py`)
- Includes max pressure in specifications section
- Formats as "Max Pressure: 300 PSI"

### 3. Word Template Processor (`export/word_template_processor.py`)
- Passes `max_pressure` to template variables
- Available as `{{max_pressure}}`

### 4. RTF Template Processor (`export/word_exporter.py`)
- Passes `max_pressure` to RTF templates
- Available as `MAX_PRESSURE`

### 5. Main Window (`gui/main_window.py`)
- Extracts max pressure from quote data
- Passes to template export functions

## Pressure Ratings by Model

| Model Series | Default Pressure | Notes |
|--------------|------------------|-------|
| LS2000 | 300 PSI | Standard pressure |
| LS2100 | 300 PSI | Standard pressure |
| LS6000 | 1500 PSI | High pressure |
| LS7000 | 1500 PSI | High pressure |
| LS7500 | 1500 PSI | High pressure |
| LS8000 | 300 PSI | Standard pressure |
| LS8500 | 1500 PSI | High pressure |
| LT9000 | 300 PSI | Standard pressure |
| FS10000 | 300 PSI | Standard pressure |

## Pressure Ratings by Connection Size

| Connection Size | Pressure Rating | Notes |
|-----------------|-----------------|-------|
| 3/4" | 300 PSI | Standard NPT |
| 1" | 300 PSI | Standard NPT |
| 2" | 150 PSI | Larger connection |
| Flange | 150# | Flange rating |
| Tri-Clamp | 150 PSI | Sanitary connection |

## Testing

You can test the max_pressure functionality with:

```bash
python test_max_pressure_template.py
```

This will generate test documents with different pressure values to verify the system is working correctly.

## Next Steps

1. **Create Template Files**: Add your Word templates to `export/templates/` directory
2. **Add Variables**: Include `{{max_pressure}}` in your templates where needed
3. **Test**: Generate quotes to verify pressure values appear correctly

## Example Template Usage

Here's how to use max_pressure in a typical quote template:

```docx
BABBITT INTERNATIONAL
Point Level Switch Quote

Part Number: {{part_number}}
Customer: {{customer_name}}
Date: {{date}}

Technical Specifications:
• Model: {{model}}
• Supply Voltage: {{supply_voltage}}
• Probe Length: {{probe_length}}"
• Maximum Temperature: {{max_temperature}}
• Maximum Pressure: {{max_pressure}}
• Process Connection: {{pc_type}} {{pc_size}}

Price: ${{unit_price}} EACH
```

The `{{max_pressure}}` will automatically be replaced with the correct pressure rating for each part number. 
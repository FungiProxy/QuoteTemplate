# RTF Template Variables Summary

## Overview

This document provides a comprehensive summary of all template variables identified in your RTF templates and how the new template processing system works.

## Identified Template Variables

### **Core Quote Information**
These variables appear in all templates and are required for basic quote generation:

| Variable | Description | Example Values | Templates |
|----------|-------------|----------------|-----------|
| `DATE` | Quote date | "December 15, 2024" | All templates |
| `CUSTOMER`/`CUSTOMER NAME`/`COMPANY` | Customer company name | "ACME Industrial Solutions" | All templates |
| `ATTN` | Contact person name | "John Smith, P.E." | All templates |
| `QUOTE_NUMBER` | Quote number/ID | "Q-2024-12345" | All templates |

### **Product Information**
Variables related to the specific product being quoted:

| Variable | Description | Example Values | Templates |
|----------|-------------|----------------|-----------|
| `PART_NUMBER` | Complete part number | "LS2000-115VAC-H-12\"" | All templates |
| `QUANTITY` | Number of units | "1" | All templates |
| `UNIT_PRICE` | Price per unit | "1,250.00" | All templates |
| `SUPPLY_VOLTAGE` | Operating voltage | "115VAC", "24VDC", "230VAC" | All templates |

### **Technical Specifications**
Variables for technical details that vary by model:

| Variable | Description | Example Values | Templates |
|----------|-------------|----------------|-----------|
| `PROBE_LENGTH` | Probe length in inches | "12", "18", "24" | All templates |
| `PROCESS_CONNECTION_SIZE` | Connection size | "¾\"", "1\"" | Most templates |
| `INSULATOR_MATERIAL` | Insulator material | "Teflon", "DELRIN", "UHMPE" | All templates |
| `INSULATOR_LENGTH` | Insulator length | "4" | Most templates |
| `PROBE_MATERIAL` | Probe material | "316SS", "HALAR" | All templates |
| `PROBE_DIAMETER` | Probe diameter | "½\"", "¾\"" | All templates |
| `MAX_TEMPERATURE` | Temperature rating | "450 F", "180 F", "250 F" | All templates |
| `MAX_PRESSURE` | Pressure rating | "300 PSI", "1500 PSI" | Most templates |

### **Model-Specific Variables**
Variables that only apply to certain product models:

| Variable | Description | Example Values | Models |
|----------|-------------|----------------|--------|
| `CABLE_LENGTH` | Cable length specification | "15 feet" | FS10000S |
| `FLANGE_SIZE` | Flange specification | "150#" | LS7500*, LS8500* |
| `SENSOR_TYPE` | Sensor element type | "Full Ring", "Partial Ring" | LS7500*, LS8500* |
| `OUTPUT_TYPE` | Output specifications | "5 Amp DPDT Relay" | Various |
| `ENCLOSURE_OPTION` | Optional enclosure | "NEMA 4 Metal Enclosure" | LS8000*, LS8500* |

## Template Processing Patterns

### **Replacement Patterns in RTF Files**

The system identifies and replaces these patterns in the RTF templates:

#### **Basic Text Patterns:**
- `DATE` → Actual date
- `CUSTOMER`/`CUSTOMER NAME`/`COMPANY` → Customer name
- `ATTN:` → Contact person name
- `Quote #`/`Quote#` → Quote number

#### **Part Number Patterns:**
- `LS2000-XXXX-H-XX"` → `LS2000-115VAC-H-12"`
- `LS6000-XXXXX-H-XX"` → `LS6000-24VDC-H-18"`
- `FS10000-115VAC-S-xx` → `FS10000-115VAC-S-24"`
- And similar patterns for all models...

#### **Technical Specification Patterns:**
- `Supply Voltage:` (blank) → `Supply Voltage: 115VAC`
- `x XX"` → `x 12"`
- `$ EACH` → `$ 1,250.00 EACH`

### **Template Files and Models**

| Template File | Model | Key Features |
|---------------|-------|--------------|
| `FS10000S_template.rtf` | FS10000S | Flow switch with cable |
| `LS2000H_template.rtf` | LS2000H | High-temp insulator |
| `LS2000S_template.rtf` | LS2000S | Standard insulator |
| `LS2100H_template.rtf` | LS2100H | Loop power, high-temp |
| `LS2100S_template.rtf` | LS2100S | Loop power, standard |
| `LS6000H_template.rtf` | LS6000H | High pressure, high-temp |
| `LS6000S_template.rtf` | LS6000S | High pressure, standard |
| `LS7000H_template.rtf` | LS7000H | Standard single point |
| `LS7000S_template.rtf` | LS7000S | Standard single point |
| `LS7000-2H_template.rtf` | LS7000-2H | Dual point level switch |
| `LS7500FR_template.rtf` | LS7500FR | Full ring presence/absence |
| `LS7500PR_template.rtf` | LS7500PR | Partial ring presence/absence |
| `LS8000H_template.rtf` | LS8000H | Remote electronics |
| `LS8000S_template.rtf` | LS8000S | Remote electronics |
| `LS8000-2H_template.rtf` | LS8000-2H | Dual point remote |
| `LS8500FR_template.rtf` | LS8500FR | Full ring remote |
| `LS8500PR_template.rtf` | LS8500PR | Partial ring remote |
| `LT9000H_template.rtf` | LT9000H | Level transmitter |
| `LT9000TS_template.rtf` | LT9000TS | Teflon sleeve transmitter |

## How to Use the System

### **Basic Usage:**

```python
from export.word_exporter import generate_quote

# Generate a quote
success = generate_quote(
    model="LS2000H",
    customer_name="ACME Industrial Solutions",
    attention_name="John Smith, P.E.",
    quote_number="Q-2024-12345",
    part_number="LS2000-115VAC-H-12",
    unit_price="1,250.00",
    supply_voltage="115VAC",
    probe_length="12",
    output_path="quotes/acme_quote.rtf"
)
```

### **Advanced Usage with Custom Specifications:**

```python
from docs.template_fileds import QuoteTemplateFields
from export.word_exporter import RTFTemplateProcessor

# Create detailed field specifications
fields = QuoteTemplateFields(
    date="December 15, 2024",
    customer_name="ACME Industrial Solutions",
    attention_name="John Smith, P.E.",
    quote_number="Q-2024-12345",
    part_number="LS2000-115VAC-H-12",
    quantity="1",
    unit_price="1,250.00",
    supply_voltage="115VAC",
    probe_length="12",
    process_connection_size="¾",
    insulator_material="Teflon",
    insulator_length="4",
    probe_material="HALAR",
    probe_diameter="½",
    max_temperature="450 F",
    max_pressure="300 PSI"
)

# Process template
processor = RTFTemplateProcessor()
processed_content = processor.process_template("LS2000H", fields)
```

## Integration with Existing System

The template system is designed to integrate with your existing quote generation components:

1. **Part Number Parsing** → Extract model and specifications
2. **Pricing Engine** → Calculate unit price
3. **Template Processing** → Replace variables in RTF template
4. **Document Export** → Save as RTF or convert to DOCX

### **Integration Points:**

```python
# Parse part number
parsed_part = part_parser.parse_part_number("LS2000-115VAC-H-12")

# Calculate pricing  
pricing = pricing_engine.calculate_pricing(parsed_part)

# Generate template fields
fields = QuoteTemplateFields(
    # ... populate from parsed_part and pricing
)

# Generate quote document
success = generate_quote_document(model, fields, output_path)
```

## Next Steps

1. **Test the system** with your existing part numbers and pricing data
2. **Integrate** with your GUI application for quote generation
3. **Convert back to DOCX** when ready for production use
4. **Customize** additional template variables as needed

## File Structure

```
export/
├── templates/              # RTF template files
│   ├── FS10000S_template.rtf
│   ├── LS2000H_template.rtf
│   └── ... (all template files)
├── word_exporter.py       # Main template processor
└── integration_example.py # Integration examples

docs/
├── template_fileds.py     # Template field definitions
└── TEMPLATE_VARIABLES_SUMMARY.md  # This document

tests/
└── test_template_processing.py    # Test suite
```

This system provides a complete solution for generating professional quote documents from your RTF templates with dynamic data replacement. 
# Composed Multi-Item Quote Export Guide

## Overview

This guide explains the new **Composed Multi-Item Quote Export** system that solves the limitations of trying to force multiple items into a single template.

## The Problem with Single-Template Approach

The previous approach of adding conditional variables to templates had these limitations:

1. **Model-Specific Content**: Templates contain model-specific text, specifications, and formatting that can't be handled by simple variables
2. **Template Selection**: Using only the first item's model template doesn't work when you have multiple different models
3. **Content Structure**: Each model has unique sections, specifications, and formatting that need to be preserved
4. **Professional Layout**: The approach couldn't maintain professional appearance when combining different models

## The Solution: Composed Multi-Template Approach

Instead of forcing everything into one template, the new system:

1. **Generates individual sections** for each item using its specific model template
2. **Combines them** into one professional document
3. **Maintains model-specific formatting** and content
4. **Adds a summary section** with totals

## How It Works

### 1. Document Structure

The composed quote creates a document with this structure:

```
BABBITT INTERNATIONAL
Point Level Switch Quote

[Header Information - Customer, Date, Quote Number]

Item 1: MAIN PART
Part Number: LS2000-115VAC-S-10"
Quantity: 1
[Technical Specifications from LS2000 template]

Item 2: MAIN PART  
Part Number: LS2100-24VDC-H-12"
Quantity: 2
[Technical Specifications from LS2100 template]

Item 3: SPARE PART
Part Number: SPARE-001
[Spare part specifications]

[Summary Table with all items and totals]

[Footer with company information]
```

### 2. Template Processing

For each main item:
- **Extracts the model** from the part number
- **Finds the appropriate template** for that model
- **Processes the template** with the item's specific data
- **Extracts technical specifications** and product details
- **Adds them to the composed document**

### 3. Content Extraction

The system intelligently extracts content from each template:
- **Skips header information** (customer, date, quote number)
- **Includes technical specifications** (voltage, probe length, materials, etc.)
- **Preserves formatting** (bold, italic, etc.)
- **Maintains professional appearance**

## Benefits

### ✅ Model-Specific Content
Each item gets the exact specifications and formatting appropriate for its model.

### ✅ Multiple Model Support
You can have LS2000, LS2100, LS6000, FS10000, and spare parts all in one quote.

### ✅ Professional Appearance
Each section maintains the professional formatting from its original template.

### ✅ Complete Information
All technical specifications, options, and details are preserved for each item.

### ✅ Summary Section
Multi-item quotes include a professional summary table with totals.

### ✅ Backward Compatibility
Single-item quotes work exactly as before.

## Usage

### Automatic Detection

The system automatically detects whether you have single or multiple items:

- **Single Item**: Uses the original template approach
- **Multiple Items**: Uses the new composed approach

### No Template Changes Required

Your existing templates work exactly as they are. No need to add conditional variables or modify templates.

### Automatic Model Selection

Each item automatically uses the correct template based on its model:
- `LS2000-115VAC-S-10"` → Uses `LS2000S_template.docx`
- `LS2100-24VDC-H-12"` → Uses `LS2100H_template.docx`
- `FS10000-115VAC-S-6"` → Uses `FS10000S_template.docx`

## Example Output

### Single Item Quote
```
BABBITT INTERNATIONAL
Point Level Switch Quote

Date: December 15, 2024
Customer: ACME Industrial Solutions
Attention: John Smith, P.E.
Quote Number: Q-2024-12345

Item 1: MAIN PART
Part Number: LS2000-115VAC-S-10"
Quantity: 1

Technical Specifications:
• Model: LS2000
• Supply Voltage: 115VAC
• Probe Length: 10"
• Probe Material: 316SS
• Insulator Material: UHMWPE
• Maximum Temperature: 450°F
• Maximum Pressure: 300 PSI
• Process Connection: NPT ¾"
• Output Type: 10 Amp SPDT Relay

[Footer with company information]
```

### Multi-Item Quote
```
BABBITT INTERNATIONAL
Point Level Switch Quote

Date: December 15, 2024
Customer: ACME Industrial Solutions
Attention: John Smith, P.E.
Quote Number: Q-2024-12345
Total Items: 3

Item 1: MAIN PART
Part Number: LS2000-115VAC-S-10"
Quantity: 1

Technical Specifications:
• Model: LS2000
• Supply Voltage: 115VAC
• Probe Length: 10"
• Probe Material: 316SS
• Insulator Material: UHMWPE
• Maximum Temperature: 450°F
• Maximum Pressure: 300 PSI
• Process Connection: NPT ¾"
• Output Type: 10 Amp SPDT Relay

------------------------------------------------------------

Item 2: MAIN PART
Part Number: LS2100-24VDC-H-12"
Quantity: 2

Technical Specifications:
• Model: LS2100
• Supply Voltage: 24VDC
• Probe Length: 12"
• Probe Material: Halar Coated
• Insulator Material: Teflon
• Maximum Temperature: 450°F
• Maximum Pressure: 300 PSI
• Process Connection: NPT ¾"
• Output Type: 10 Amp SPDT Relay

------------------------------------------------------------

Item 3: SPARE PART
Part Number: SPARE-001
Quantity: 1

Description: Replacement Probe Assembly
Category: probe_assembly
Unit Price: $125.00
Total Price: $125.00

================================================================================

QUOTE SUMMARY

┌─────┬─────────────────────┬──────────┬──────────┬─────────────┐
│Item │ Part Number         │ Type     │ Quantity │ Total Price │
├─────┼─────────────────────┼──────────┼──────────┼─────────────┤
│  1  │ LS2000-115VAC-S-10" │ MAIN     │    1     │   $425.00   │
│  2  │ LS2100-24VDC-H-12"  │ MAIN     │    2     │  $1,360.00  │
│  3  │ SPARE-001           │ SPARE    │    1     │   $125.00   │
├─────┼─────────────────────┼──────────┼──────────┼─────────────┤
│     │                     │          │  TOTAL:  │  $1,910.00  │
└─────┴─────────────────────┴──────────┴──────────┴─────────────┘

[Footer with company information]
```

## Implementation Details

### Function: `generate_composed_multi_item_quote()`

This is the main function that handles the composed export:

```python
def generate_composed_multi_item_quote(
    quote_items: List[Dict[str, Any]],
    customer_name: str,
    attention_name: str,
    quote_number: str,
    output_path: str,
    employee_info: Optional[Dict[str, str]] = None,
    **kwargs
) -> bool:
```

### Helper Functions

- `_add_main_item_section()`: Processes each main item using its specific template
- `_add_spare_part_section()`: Adds spare part information
- `_add_basic_specifications()`: Fallback for when template processing fails

### Content Extraction Logic

The system extracts content by:
1. Processing each item's template with its specific data
2. Identifying technical specification paragraphs
3. Copying them to the composed document
4. Preserving formatting and structure

## Testing

Use the test script to verify the functionality:

```bash
python test_composed_multi_item_export.py
```

This will test:
- Multi-item quotes with different models
- Single item quotes (backward compatibility)
- Mixed model combinations
- Spare parts integration

## Next Steps

1. **Test with your actual quote data**
2. **Review the generated documents**
3. **Customize the summary section** if needed
4. **Adjust formatting** if required
5. **Add any additional sections** specific to your business needs

## Advantages Over Previous Approach

| Aspect | Previous Approach | New Composed Approach |
|--------|------------------|----------------------|
| **Model Support** | Limited to one model | Multiple models in one quote |
| **Template Changes** | Required conditional variables | No template changes needed |
| **Content Accuracy** | Generic variables | Model-specific content |
| **Professional Appearance** | Compromised | Maintained for each model |
| **Flexibility** | Limited | Highly flexible |
| **Maintenance** | Complex template management | Simple template management |

This new approach solves all the limitations you identified while maintaining the professional quality and accuracy of your quote documents. 
# Word Template Setup Guide

## Overview

This guide shows how to set up your original Word templates with template variables like `{{customer_name}}` to work with the new Word template processor. This approach maintains your professional formatting while enabling reliable data population.

## Template Variables Format

Use the format `{{variable_name}}` for all data that should be replaced. The system recognizes these variables:

### Header Information
- `{{date}}` - Current date (automatically formatted as "December 15, 2024")
- `{{customer_name}}` or `{{company_name}}` - Customer company name
- `{{attention_name}}` or `{{contact_name}}` - Contact person name
- `{{quote_number}}` - Quote number

### Product Information
- `{{part_number}}` - Full part number (e.g., "LS2000-115VAC-S-12")
- `{{quantity}}` - Quantity (usually "1")
- `{{unit_price}}` or `{{price}}` - Unit price (e.g., "1,250.00")
- `{{supply_voltage}}` or `{{voltage}}` - Supply voltage (e.g., "115VAC")
- `{{probe_length}}` or `{{length}}` - Probe length (e.g., "12")

### Technical Specifications
- `{{process_connection_size}}` - Connection size (e.g., "¾"")
- `{{insulator_material}}` - Insulator material (e.g., "UHMPE", "Teflon")
- `{{insulator_length}}` - Insulator length (e.g., "4"")
- `{{probe_material}}` - Probe material (e.g., "316SS", "HALAR")
- `{{probe_diameter}}` - Probe diameter (e.g., "½"")
- `{{max_temperature}}` - Maximum temperature (e.g., "450°F")
- `{{max_pressure}}` - Maximum pressure (e.g., "300 PSI")
- `{{output_type}}` - Output type (e.g., "10 Amp SPDT Relay")

### Company Information (Pre-filled)
- `{{company_contact}}` - "John Nicholosi"
- `{{company_phone}}` - "(713) 467-4438"
- `{{company_email}}` - "John@babbitt.us"
- `{{company_website}}` - "www.babbittinternational.com"

### Terms (Pre-filled)
- `{{delivery_terms}}` - "NET 30 W.A.C."
- `{{fob_terms}}` - "FOB, Houston, TX"
- `{{quote_validity}}` - "30 days"

## Example Template Conversion

### Before (Original):
```
DATE: _______________

CUSTOMER NAME: _________________________

ATTN: _________________________     Quote #: _____________

Subject: LS2000 Level Switch Quote

1 QTY    LS2000-XXXX-S-XX" LEVEL SWITCH         $_______ EACH

• Supply Voltage: ___________
• Probe: ½" Diameter 316SS x XX" (Including Insulator)
```

### After (With Template Variables):
```
DATE: {{date}}

CUSTOMER NAME: {{customer_name}}

ATTN: {{attention_name}}               Quote #: {{quote_number}}

Subject: LS2000 Level Switch Quote

1 QTY    {{part_number}} LEVEL SWITCH         ${{unit_price}} EACH

• Supply Voltage: {{supply_voltage}}
• Probe: {{probe_diameter}} Diameter {{probe_material}} x {{probe_length}}" (Including Insulator)
```

## Step-by-Step Template Setup

### Step 1: Open Your Original Word Template
1. Open your existing professional Word template (e.g., `LS2000_Quote_Template.docx`)
2. Save a copy as `LS2000S_template.docx` in the `export/templates/` folder

### Step 2: Replace Data Fields with Variables
Replace any field that should be filled with data:

**Header Section:**
- Replace "DATE" with `{{date}}`
- Replace "CUSTOMER NAME" with `{{customer_name}}`
- Replace "ATTN:" field with `ATTN: {{attention_name}}`
- Replace "Quote #" field with `Quote #: {{quote_number}}`

**Product Section:**
- Replace part number pattern with `{{part_number}}`
- Replace price with `${{unit_price}} EACH`
- Replace voltage field with `{{supply_voltage}}`
- Replace length measurements with `{{probe_length}}"`

**Technical Specifications:**
- Replace material specifications with appropriate variables
- Replace temperature/pressure ratings with variables

### Step 3: Test the Template
The system will automatically detect missing variables and show them as `{{MISSING: variable_name}}` so you can easily find what needs to be added.

## File Naming Convention

Save your Word templates in `export/templates/` with this naming pattern:
- `LS2000S_template.docx`
- `LS2000H_template.docx`
- `FS10000S_template.docx`
- etc.

The system extracts the model name from your part number and looks for the corresponding template.

## Benefits of This Approach

✅ **Maintains Professional Formatting** - Your original design, fonts, layout, and logos are preserved
✅ **Reliable Data Population** - Template variables are replaced accurately every time
✅ **Easy to Update** - Just edit the Word template and the changes apply to all future quotes
✅ **No Conversion Issues** - Direct Word processing means no formatting loss
✅ **Easy to Debug** - Missing variables are clearly marked in the output

## Integration with Current System

The new Word template processor integrates seamlessly with your existing export system. When you export a quote, the system will:

1. Extract the model from the part number (e.g., "LS2000S")
2. Load the corresponding template (`LS2000S_template.docx`)
3. Replace all `{{variables}}` with actual data
4. Save the result as a professional Word document

## Next Steps

1. **Convert one template first** - Start with LS2000S as a test
2. **Test with real data** - Generate a quote to verify formatting
3. **Convert remaining templates** - Once satisfied, convert other models
4. **Update export system** - Integrate the new processor with your GUI

Would you like me to help you convert your first template? 
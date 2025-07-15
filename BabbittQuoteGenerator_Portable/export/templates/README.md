# Word Templates Directory

This directory contains Word (.docx) templates for the Babbitt Quote Generator.

## Template Naming Convention

Templates should be named according to the model they represent:
- LS2000S_template.docx - LS2000 Standard version
- LS2000H_template.docx - LS2000 High-Temp version
- LS2100S_template.docx - LS2100 Standard version
- etc.

## Template Variables

Templates should use the following variable placeholders:

### Header Information
- {{customer_name}} - Customer company name
- {{attention_name}} - Contact person name
- {{quote_number}} - Quote number
- {{date}} - Current date

### Product Information
- {{part_number}} - Full part number
- {{unit_price}} - Unit price
- {{supply_voltage}} - Supply voltage
- {{probe_length}} - Probe length
- {{probe_material}} - Probe material
- {{insulator_material}} - Insulator material
- {{max_temperature}} - Maximum temperature
- {{max_pressure}} - Maximum pressure (e.g., "300 PSI", "1500 PSI")

### Process Connection
- {{pc_type}} - Process connection type
- {{pc_size}} - Process connection size
- {{pc_matt}} - Process connection material
- {{pc_rate}} - Process connection rating

### Employee/Company Information
- {{employee_name}} - Employee name (from selected employee)
- {{employee_phone}} - Employee phone number
- {{employee_email}} - Employee email address
- {{company_contact}} - Company contact (same as employee_name)
- {{company_phone}} - Company phone (same as employee_phone)
- {{company_email}} - Company email (same as employee_email)
- {{company_website}} - Company website

## Setup Instructions

1. Copy your existing Word templates to this directory
2. Rename them according to the naming convention above
3. Replace placeholder text with template variables (e.g., {{customer_name}})
4. Test the templates using the quote generator

## Fallback Templates

If a specific model template is not found, the system will:
1. Try a generic template (e.g., LS2000_template.docx)
2. Fall back to default_template.docx
3. Use the old quote generator as a last resort

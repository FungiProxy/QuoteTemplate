# Multi-Item Template Variables Guide

This guide explains how to use the new conditional variables in your Word templates to handle multiple quote items.

## Overview

The new system allows your existing templates to work with both single and multiple items by adding conditional variables. When there's only one item, the template works exactly as before. When there are multiple items, additional sections can be displayed.

## Conditional Variables

### Multi-Item Detection

- `{{has_multiple_items}}` - Returns "true" if multiple items, "false" if single item
- `{{is_single_item}}` - Returns "true" if single item, "false" if multiple items
- `{{item_count}}` - Number of items in the quote (e.g., "2", "3", "5")

### Quote Summary Variables

- `{{total_quote_value}}` - Total value of all items combined

### Additional Item Variables

For each additional item (items 2-10), the following variables are available:

#### Basic Item Info
- `{{item_2_part_number}}` - Part number for item 2
- `{{item_2_type}}` - Type of item (MAIN or SPARE)
- `{{item_2_quantity}}` - Quantity for item 2

#### Main Item Specifications (for main items only)
- `{{item_2_model}}` - Model (e.g., LS2000, LS2100)
- `{{item_2_voltage}}` - Voltage (e.g., 115VAC, 24VDC)
- `{{item_2_probe_length}}` - Probe length in inches
- `{{item_2_probe_material}}` - Probe material (e.g., 316SS, Halar)
- `{{item_2_insulator_material}}` - Insulator material (e.g., Teflon, UHMWPE)
- `{{item_2_insulator_length}}` - Insulator length (e.g., 4")
- `{{item_2_max_temperature}}` - Max temperature (e.g., 450°F)
- `{{item_2_max_pressure}}` - Max pressure (e.g., 300 PSI)
- `{{item_2_pc_type}}` - Process connection type (e.g., NPT)
- `{{item_2_pc_size}}` - Process connection size (e.g., ¾")
- `{{item_2_output_type}}` - Output type (e.g., 10 Amp SPDT Relay)
- `{{item_2_options}}` - Comma-separated list of options
- `{{item_2_unit_price}}` - Unit price for item 2
- `{{item_2_total_price}}` - Total price (unit price × quantity)

#### Spare Part Specifications (for spare parts only)
- `{{item_2_description}}` - Description of the spare part
- `{{item_2_category}}` - Category of spare part
- `{{item_2_unit_price}}` - Unit price for spare part
- `{{item_2_total_price}}` - Total price (unit price × quantity)

## Conditional Content Syntax

### Multi-Item Conditionals

Use `{{if_multiple_items:content}}` to show content only when there are multiple items:

```
{{if_multiple_items:
Additional Items:
- Item 2: {{item_2_part_number}} - {{item_2_unit_price}}
- Item 3: {{item_3_part_number}} - {{item_3_unit_price}}

Total Quote Value: {{total_quote_value}}
}}
```

### Item-Specific Conditionals

Use `{{if_item_2:content}}` to show content only when item 2 exists:

```
{{if_item_2:
Item 2 Specifications:
Model: {{item_2_model}}
Voltage: {{item_2_voltage}}
Probe Length: {{item_2_probe_length}}"
Max Temperature: {{item_2_max_temperature}}
Unit Price: {{item_2_unit_price}}
}}
```

### Combining Conditionals

You can combine multiple conditionals:

```
{{if_multiple_items:
{{if_item_2:
Item 2: {{item_2_part_number}} - {{item_2_unit_price}}
}}
{{if_item_3:
Item 3: {{item_3_part_number}} - {{item_3_unit_price}}
}}
Total: {{total_quote_value}}
}}
```

## Template Examples

### Example 1: Simple Additional Items Section

Add this to your template to show additional items:

```
{{if_multiple_items:

ADDITIONAL ITEMS
================

{{if_item_2:• {{item_2_part_number}} - Qty: {{item_2_quantity}} - {{item_2_unit_price}} each}}
{{if_item_3:• {{item_3_part_number}} - Qty: {{item_3_quantity}} - {{item_3_unit_price}} each}}
{{if_item_4:• {{item_4_part_number}} - Qty: {{item_4_quantity}} - {{item_4_unit_price}} each}}

TOTAL QUOTE VALUE: {{total_quote_value}}
}}
```

### Example 2: Detailed Specifications for Each Item

Add this for detailed specifications:

```
{{if_multiple_items:

DETAILED SPECIFICATIONS
=======================

{{if_item_2:
Item 2: {{item_2_part_number}}
Model: {{item_2_model}}
Voltage: {{item_2_voltage}}
Probe Length: {{item_2_probe_length}}"
Probe Material: {{item_2_probe_material}}
Insulator: {{item_2_insulator_material}} {{item_2_insulator_length}}
Max Temperature: {{item_2_max_temperature}}
Max Pressure: {{item_2_max_pressure}}
Process Connection: {{item_2_pc_type}} {{item_2_pc_size}}
Options: {{item_2_options}}
Unit Price: {{item_2_unit_price}}
Quantity: {{item_2_quantity}}
Total: {{item_2_total_price}}

}}

{{if_item_3:
Item 3: {{item_3_part_number}}
Model: {{item_3_model}}
Voltage: {{item_3_voltage}}
Probe Length: {{item_3_probe_length}}"
Probe Material: {{item_3_probe_material}}
Insulator: {{item_3_insulator_material}} {{item_3_insulator_length}}
Max Temperature: {{item_3_max_temperature}}
Max Pressure: {{item_3_max_pressure}}
Process Connection: {{item_3_pc_type}} {{item_3_pc_size}}
Options: {{item_3_options}}
Unit Price: {{item_3_unit_price}}
Quantity: {{item_3_quantity}}
Total: {{item_3_total_price}}

}}
}}
```

### Example 3: Summary Table

Add this for a professional summary table:

```
{{if_multiple_items:

QUOTE SUMMARY
=============

Item Count: {{item_count}} items

| Item | Part Number | Type | Quantity | Unit Price | Total |
|------|-------------|------|----------|------------|-------|
| 1 | {{part_number}} | MAIN | {{quantity}} | {{unit_price}} | {{price}} |
{{if_item_2:| 2 | {{item_2_part_number}} | {{item_2_type}} | {{item_2_quantity}} | {{item_2_unit_price}} | {{item_2_total_price}} |}}
{{if_item_3:| 3 | {{item_3_part_number}} | {{item_3_type}} | {{item_3_quantity}} | {{item_3_unit_price}} | {{item_3_total_price}} |}}
{{if_item_4:| 4 | {{item_4_part_number}} | {{item_4_type}} | {{item_4_quantity}} | {{item_4_unit_price}} | {{item_4_total_price}} |}}

**TOTAL QUOTE VALUE: {{total_quote_value}}**
}}
```

## Backward Compatibility

- **Single Item Quotes**: Work exactly as before - no changes needed
- **Existing Templates**: Continue to work without modification
- **New Variables**: Only appear when multiple items are present

## Best Practices

1. **Test Both Scenarios**: Always test your template with both single and multiple items
2. **Use Clear Formatting**: Make additional items sections visually distinct
3. **Include Totals**: Always show the total quote value for multi-item quotes
4. **Consistent Styling**: Match the formatting of your existing template
5. **Limit Items**: The system supports up to 10 items (item_2 through item_11)

## Troubleshooting

### Variables Not Showing
- Check that the variable name is exactly correct (case-sensitive)
- Ensure the item exists in the quote
- Verify the conditional syntax is correct

### Content Not Appearing
- Check that `{{if_multiple_items:` and `}}` are properly paired
- Ensure there are no extra spaces in the conditional syntax
- Verify that the item number in `{{if_item_X:` matches an existing item

### Template Not Working
- Test with a single item first to ensure basic functionality
- Check the console output for error messages
- Verify that the template file is saved in the correct format (.docx)

## Migration Guide

To add multi-item support to existing templates:

1. **Backup your template** before making changes
2. **Add conditional sections** using the examples above
3. **Test with single items** to ensure nothing breaks
4. **Test with multiple items** to verify new functionality
5. **Update documentation** for your team

## Support

If you encounter issues with multi-item templates:

1. Check the console output for detailed error messages
2. Verify that all required variables are present
3. Test with simpler conditionals first
4. Contact the development team with specific error details 
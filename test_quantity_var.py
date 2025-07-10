#!/usr/bin/env python3
"""
Test script to verify quantity variable in templates
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser

def test_quantity_variable():
    """Test that quantity variable is available in quote data"""
    parser = PartNumberParser()
    
    # Test part number
    part_number = 'LS2000-115VAC-S-10"'
    
    print(f"Testing quantity variable for: {part_number}")
    print("=" * 50)
    
    try:
        # Parse the part number
        parsed = parser.parse_part_number(part_number)
        
        if parsed.get('errors'):
            print(f"❌ Parse errors: {parsed['errors']}")
            return
        
        # Get quote data
        quote_data = parser.get_quote_data(parsed)
        
        # Check quantity variable
        quantity = quote_data.get('quantity', 'not found')
        print(f"Quantity variable: {quantity}")
        
        if quantity == 1:
            print("✅ PASS - Quantity variable is available and defaults to 1")
        else:
            print(f"❌ FAIL - Expected quantity to be 1, got {quantity}")
        
        # Show other key variables for reference
        print(f"\nOther template variables:")
        print(f"  part_number: {quote_data.get('part_number')}")
        print(f"  unit_price: {quote_data.get('total_price')}")
        print(f"  length_adder: {quote_data.get('length_adder')}")
        print(f"  adder_per: {quote_data.get('adder_per')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_quantity_variable() 
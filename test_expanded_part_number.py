#!/usr/bin/env python3
"""
Test script to verify that expanded part numbers are used in quotes
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser

def test_expanded_part_numbers():
    """Test that expanded part numbers are used in quotes"""
    print("Testing Expanded Part Numbers in Quotes")
    print("=" * 50)
    
    parser = PartNumberParser()
    
    # Test cases with shorthand inputs
    test_cases = [
        "ls2-112-2-10",
        "ls21-24-h-12",
        "ls7-230-stainless-24",
        "ls8-115-teflon-36",
    ]
    
    for test_case in test_cases:
        print(f"\nInput: {test_case}")
        print("-" * 40)
        
        # Parse the part number
        parsed_result = parser.parse_part_number(test_case)
        
        if parsed_result.get('error'):
            print(f"❌ Error: {parsed_result['error']}")
            continue
        
        # Get quote data
        quote_data = parser.get_quote_data(parsed_result)
        
        print(f"📝 Expanded Part Number: {quote_data['part_number']}")
        print(f"📝 Original Input: {quote_data.get('original_input', 'N/A')}")
        print(f"💰 Total Price: ${quote_data['total_price']:.2f}")
        
        # Show the components that were expanded
        print(f"   Model: {quote_data['model']}")
        print(f"   Voltage: {quote_data['voltage']}")
        print(f"   Material: {quote_data['probe_material']}")
        print(f"   Length: {quote_data['probe_length']}\"")
        
        if quote_data.get('options'):
            print(f"   Options: {', '.join(quote_data['options'])}")

if __name__ == "__main__":
    test_expanded_part_numbers() 
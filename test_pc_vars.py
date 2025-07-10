#!/usr/bin/env python3
"""
Test script to verify process connection variables and length adder variables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser

def test_part_numbers():
    """Test various part numbers to verify variables"""
    parser = PartNumberParser()
    
    # Test cases for length_adder and adder_per
    test_cases = [
        {
            'part_number': 'LS2000-115VAC-S-10"',
            'expected_length_adder': 45.0,
            'expected_adder_per': 'per foot',
            'description': 'S material should have 45 per foot'
        },
        {
            'part_number': 'LS2000-115VAC-U-10"',
            'expected_length_adder': 40.0,
            'expected_adder_per': 'per inch',
            'description': 'U material should have 40 per inch'
        },
        {
            'part_number': 'LS2000-115VAC-H-10"',
            'expected_length_adder': 110.0,
            'expected_adder_per': 'per foot',
            'description': 'H material should have 110 per foot'
        },
        {
            'part_number': 'LS2000-115VAC-T-10"',
            'expected_length_adder': 50.0,
            'expected_adder_per': 'per inch',
            'description': 'T material should have 50 per inch'
        }
    ]
    
    print("Testing length_adder and adder_per variables:")
    print("=" * 60)
    
    for test_case in test_cases:
        part_number = test_case['part_number']
        expected_adder = test_case['expected_length_adder']
        expected_per = test_case['expected_adder_per']
        description = test_case['description']
        
        print(f"\nTesting: {part_number}")
        print(f"Expected: {expected_adder} {expected_per}")
        print(f"Description: {description}")
        
        try:
            # Parse the part number
            parsed = parser.parse_part_number(part_number)
            
            if parsed.get('errors'):
                print(f"❌ Parse errors: {parsed['errors']}")
                continue
            
            # Get quote data
            quote_data = parser.get_quote_data(parsed)
            
            # Check length_adder and adder_per
            actual_adder = quote_data.get('length_adder', 0)
            actual_per = quote_data.get('adder_per', 'none')
            
            print(f"Actual: {actual_adder} {actual_per}")
            
            if actual_adder == expected_adder and actual_per == expected_per:
                print("✅ PASS")
            else:
                print("❌ FAIL")
                print(f"  Expected: {expected_adder} {expected_per}")
                print(f"  Actual: {actual_adder} {actual_per}")
            
            # Also show the material info for debugging
            material_code = parsed.get('probe_material', 'S')
            print(f"  Material code: {material_code}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Testing process connection variables:")
    print("=" * 60)
    
    # Test process connection variables
    pc_test_cases = [
        {
            'part_number': 'LS2000-115VAC-S-10"-1"150#RF',
            'expected_pc_type': 'Flange',
            'expected_pc_size': '1"',
            'expected_pc_matt': '316SS',
            'expected_pc_rate': '150#'
        },
        {
            'part_number': 'LS2000-115VAC-S-10"-2"TC',
            'expected_pc_type': 'Tri-Clamp',
            'expected_pc_size': '2"',
            'expected_pc_matt': '316SS',
            'expected_pc_rate': None
        },
        {
            'part_number': 'LS2000-115VAC-S-10"-1/2"NPT',
            'expected_pc_type': 'NPT',
            'expected_pc_size': '1/2"',
            'expected_pc_matt': '316SS',
            'expected_pc_rate': None
        }
    ]
    
    for test_case in pc_test_cases:
        part_number = test_case['part_number']
        expected_type = test_case['expected_pc_type']
        expected_size = test_case['expected_pc_size']
        expected_matt = test_case['expected_pc_matt']
        expected_rate = test_case['expected_pc_rate']
        
        print(f"\nTesting: {part_number}")
        
        try:
            parsed = parser.parse_part_number(part_number)
            
            if parsed.get('errors'):
                print(f"❌ Parse errors: {parsed['errors']}")
                continue
            
            quote_data = parser.get_quote_data(parsed)
            
            actual_type = quote_data.get('pc_type')
            actual_size = quote_data.get('pc_size')
            actual_matt = quote_data.get('pc_matt')
            actual_rate = quote_data.get('pc_rate')
            
            print(f"pc_type: {actual_type} (expected: {expected_type})")
            print(f"pc_size: {actual_size} (expected: {expected_size})")
            print(f"pc_matt: {actual_matt} (expected: {expected_matt})")
            print(f"pc_rate: {actual_rate} (expected: {expected_rate})")
            
            if (actual_type == expected_type and 
                actual_size == expected_size and 
                actual_matt == expected_matt and 
                actual_rate == expected_rate):
                print("✅ PASS")
            else:
                print("❌ FAIL")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_part_numbers() 
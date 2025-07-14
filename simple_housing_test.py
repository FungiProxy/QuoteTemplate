#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.part_parser import PartNumberParser

def test_housing():
    parser = PartNumberParser()
    
    # Test new housing codes
    print("Testing NEW housing codes:")
    test_cases = [
        'LS2000-115VAC-S-10"-VRHOUSING',
        'LS7000-115VAC-S-10"-SSHOUSING',
        'LS2000-115VAC-S-10"-XSP-VR-VRHOUSING-90DEG'
    ]
    
    for part_number in test_cases:
        print(f"\nTesting: {part_number}")
        result = parser.parse_part_number(part_number)
        
        if result.get('error'):
            print(f"  Error: {result['error']}")
        else:
            options = [opt['code'] for opt in result.get('options', [])]
            print(f"  Options: {options}")
            
            # Check option names
            for option in result.get('options', []):
                if option['code'] in ['VRHOUSING', 'SSHOUSING']:
                    print(f"  {option['code']}: {option['name']}")
    
    # Test old housing codes (should be flagged as unknown)
    print("\n\nTesting OLD housing codes (should be flagged as unknown):")
    old_test_cases = [
        'LS2000-115VAC-S-10"-VRHSE',
        'LS7000-115VAC-S-10"-SSHSE'
    ]
    
    for part_number in old_test_cases:
        print(f"\nTesting: {part_number}")
        result = parser.parse_part_number(part_number)
        
        if result.get('error'):
            print(f"  Error: {result['error']}")
        else:
            options = [opt['code'] for opt in result.get('options', [])]
            print(f"  Options: {options}")
            
            warnings = result.get('warnings', [])
            if warnings:
                print(f"  Warnings: {warnings}")
            else:
                print(f"  No warnings (should have unknown option warning)")

if __name__ == "__main__":
    test_housing() 
#!/usr/bin/env python3
"""
Test script for part number shorthand parsing
Tests the new shorthand functionality for various input patterns
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser

def test_shorthand_parsing():
    """Test the shorthand parsing functionality"""
    print("Testing Part Number Shorthand Parsing")
    print("=" * 50)
    
    # Initialize parser
    parser = PartNumberParser()
    
    # Test cases with various shorthand patterns
    test_cases = [
        # Your original example
        "ls2-112-2-10",
        
        # Model shorthands
        "ls21-115-2-10",      # LS21 → LS2100
        "ls6-24-2-10",        # LS6 → LS6000
        "ls7-230-2-10",       # LS7 → LS7000
        "ls72-115-2-10",      # LS72 → LS7000/2
        "ls8-24-2-10",        # LS8 → LS8000
        "lt9-115-2-10",       # LT9 → LT9000
        "fs10-115-2-10",      # FS10 → FS10000
        
        # Voltage shorthands
        "ls2000-115-s-10",    # 115 → 115VAC
        "ls2000-24-s-10",     # 24 → 24VDC
        "ls2000-230-s-10",    # 230 → 230VAC
        "ls2000-12-s-10",     # 12 → 12VDC
        "ls2000-110-s-10",    # 110 → 115VAC (approximation)
        "ls2000-240-s-10",    # 240 → 230VAC (approximation)
        
        # Material shorthands
        "ls2000-115-stainless-10",  # stainless → S
        "ls2000-115-steel-10",      # steel → S
        "ls2000-115-halar-10",      # halar → H
        "ls2000-115-teflon-10",     # teflon → T
        "ls2000-115-uhmw-10",       # uhmw → U
        "ls2000-115-ceramic-10",    # ceramic → C
        
        # Length shorthands
        "ls2000-115-s-12",          # 12 → 12.0
        "ls2000-115-s-24",          # 24 → 24.0
        "ls2000-115-s-36",          # 36 → 36.0
        
        # Mixed shorthands
        "ls2-112-stainless-12",
        "ls7-24-halar-24",
        "ls8-230-teflon-36",
        
        # Original full format (should still work)
        "LS2000-115VAC-S-10\"",
        "LS2100-24VDC-H-12\"",
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case}")
        print("-" * 40)
        
        try:
            result = parser.parse_part_number(test_case)
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✓ Parsed Model: {result['model']}")
                print(f"✓ Parsed Voltage: {result['voltage']}")
                print(f"✓ Parsed Material: {result['probe_material']} ({result.get('probe_material_name', 'Unknown')})")
                print(f"✓ Parsed Length: {result['probe_length']}\"")
                
                # Show options
                options = result.get('options', [])
                if options:
                    print(f"✓ Options:")
                    for opt in options:
                        original = opt.get('original_input', '')
                        if original:
                            print(f"  - {opt['code']} ({opt['name']}) [from: {original}]")
                        else:
                            print(f"  - {opt['code']} ({opt['name']})")
                else:
                    print("✓ Options: None")
                
                # Show warnings
                warnings = result.get('warnings', [])
                if warnings:
                    print(f"⚠ Warnings: {warnings}")
                
                # Show pricing
                pricing = result.get('pricing', {})
                if pricing.get('total_price', 0) > 0:
                    print(f"💰 Total Price: ${pricing['total_price']:.2f}")
                
                # Show the "expanded" part number
                expanded = f"{result['model']}-{result['voltage']}-{result['probe_material']}-{result['probe_length']}\""
                if len(result.get('options', [])) > 0:
                    option_codes = [opt['code'] for opt in result['options']]
                    expanded += "-" + "-".join(option_codes)
                
                print(f"📝 Expanded to: {expanded}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_individual_shorthand_methods():
    """Test individual shorthand parsing methods"""
    print("\n\nTesting Individual Shorthand Methods")
    print("=" * 50)
    
    parser = PartNumberParser()
    
    # Test model shorthand
    print("\nModel Shorthand Tests:")
    model_tests = ['ls2', 'ls21', 'ls6', 'ls7', 'ls72', 'ls8', 'ls82', 'lt9', 'fs10', 'fs1']
    for test in model_tests:
        result = parser._parse_model_shorthand(test)
        print(f"  {test} → {result}")
    
    # Test voltage shorthand
    print("\nVoltage Shorthand Tests:")
    voltage_tests = ['115', '24', '230', '12', '112', '110', '240']
    for test in voltage_tests:
        result = parser._parse_voltage_shorthand(test)
        print(f"  {test} → {result}")
    
    # Test material shorthand
    print("\nMaterial Shorthand Tests:")
    material_tests = ['stainless', 'steel', 'halar', 'teflon', 'uhmw', 'ceramic', 's', 'h', 't']
    for test in material_tests:
        result = parser._parse_material_shorthand(test)
        print(f"  {test} → {result}")
    
    # Test length shorthand
    print("\nLength Shorthand Tests:")
    length_tests = ['10', '12', '24', '36', '48', '60', '72', '96']
    for test in length_tests:
        result = parser._parse_length_shorthand(test)
        print(f"  {test} → {result}")

if __name__ == "__main__":
    test_shorthand_parsing()
    test_individual_shorthand_methods() 
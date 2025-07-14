#!/usr/bin/env python3
"""
Test script for part number aliases
Tests the new alias functionality for 3/4"ROD and HSE
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser
from database.db_manager import DatabaseManager

def test_aliases():
    """Test the alias functionality"""
    print("Testing Part Number Aliases")
    print("=" * 40)
    
    # Initialize parser and database
    parser = PartNumberParser()
    db = DatabaseManager()
    
    # Test cases with aliases
    test_cases = [
        "LS2000-115VAC-S-10\"-3/4\"ROD",  # Test 3/4"ROD alias
        "LS2000-115VAC-S-10\"-HSE",       # Test HSE alias
        "LS2000-115VAC-S-10\"-VRHSE",     # Test VRHSE alias
        "LS2000-115VAC-S-10\"-3/4\"OD",   # Test original 3/4"OD
        "LS2000-115VAC-S-10\"-SSHOUSING", # Test original SSHOUSING
        "LS2000-115VAC-S-10\"-VRHOUSING", # Test original VRHOUSING
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case}")
        print("-" * 30)
        
        result = parser.parse_part_number(test_case)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✓ Model: {result['model']}")
            print(f"✓ Voltage: {result['voltage']}")
            print(f"✓ Probe: {result['probe_material_name']} @ {result['probe_length']}\"")
            
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

def test_database_aliases():
    """Test database alias methods"""
    print("\n\nTesting Database Alias Methods")
    print("=" * 40)
    
    db = DatabaseManager()
    
    # Test getting aliases
    aliases = db.get_all_aliases()
    print(f"Found {len(aliases)} aliases in database:")
    for alias in aliases:
        print(f"  - {alias['section_type']}: {alias['alias']} → {alias['standard_code']}")
    
    # Test resolving specific aliases
    test_aliases = ['3/4"ROD', 'HSE', 'VRHSE', 'NONEXISTENT']
    
    print(f"\nTesting alias resolution:")
    for test_alias in test_aliases:
        resolved = db.get_section_alias('option', test_alias)
        if resolved:
            print(f"  ✓ {test_alias} → {resolved}")
        else:
            print(f"  ✗ {test_alias} → Not found")
    
    # Test autocomplete suggestions
    print(f"\nTesting autocomplete suggestions for '3/4':")
    suggestions = db.get_autocomplete_suggestions('option', '3/4', 5)
    for suggestion in suggestions:
        is_alias = suggestion.get('is_alias', False)
        alias_mark = " (alias)" if is_alias else ""
        print(f"  - {suggestion['code']} - {suggestion['name']}{alias_mark}")

if __name__ == "__main__":
    test_aliases()
    test_database_aliases() 
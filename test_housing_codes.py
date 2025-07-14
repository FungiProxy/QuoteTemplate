#!/usr/bin/env python3
"""
Test script to verify the new housing codes (SSHOUSING, VRHOUSING) work correctly
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from core.part_parser import PartNumberParser
from database.db_manager import DatabaseManager

def test_housing_codes():
    """Test the new housing codes"""
    
    print("🏠 Testing New Housing Codes")
    print("=" * 40)
    
    # Initialize parser and database manager
    parser = PartNumberParser()
    db_manager = DatabaseManager()
    
    # Test part numbers with new housing codes
    test_cases = [
        {
            'part_number': 'LS2000-115VAC-S-10"-VRHOUSING',
            'expected_options': ['VRHOUSING'],
            'description': 'LS2000 with epoxy housing'
        },
        {
            'part_number': 'LS7000-115VAC-S-10"-SSHOUSING',
            'expected_options': ['SSHOUSING'],
            'description': 'LS7000 with stainless steel housing'
        },
        {
            'part_number': 'LS2000-115VAC-S-10"-XSP-VR-VRHOUSING-90DEG',
            'expected_options': ['XSP', 'VR', 'VRHOUSING'],
            'description': 'LS2000 with multiple options including epoxy housing'
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['description']}")
        print(f"   Part Number: {test_case['part_number']}")
        
        try:
            # Parse the part number
            result = parser.parse_part_number(test_case['part_number'])
            
            if result.get('error'):
                print(f"   ❌ Parse Error: {result['error']}")
                all_passed = False
                continue
            
            # Check if options were parsed correctly
            parsed_options = [opt['code'] for opt in result.get('options', [])]
            expected_options = test_case['expected_options']
            
            if parsed_options == expected_options:
                print(f"   ✅ Options parsed correctly: {parsed_options}")
            else:
                print(f"   ❌ Options mismatch:")
                print(f"      Expected: {expected_options}")
                print(f"      Got: {parsed_options}")
                all_passed = False
            
            # Check if the option names are correct
            for option in result.get('options', []):
                if option['code'] == 'VRHOUSING':
                    if option['name'] == 'Epoxy Housing':
                        print(f"   ✅ VRHOUSING name correct: {option['name']}")
                    else:
                        print(f"   ❌ VRHOUSING name incorrect: {option['name']}")
                        all_passed = False
                elif option['code'] == 'SSHOUSING':
                    if option['name'] == 'Stainless Steel Housing':
                        print(f"   ✅ SSHOUSING name correct: {option['name']}")
                    else:
                        print(f"   ❌ SSHOUSING name incorrect: {option['name']}")
                        all_passed = False
            
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            all_passed = False
    
    # Test database integration
    print(f"\n🗄️  Testing Database Integration")
    print("=" * 40)
    
    try:
        if db_manager.connect():
            # Check if new codes exist in database
            housing_options = db_manager.execute_query(
                "SELECT code, name, price FROM options WHERE code IN ('SSHOUSING', 'VRHOUSING') ORDER BY code"
            )
            
            if housing_options:
                print("✅ New housing codes found in database:")
                for option in housing_options:
                    print(f"   {option['code']}: {option['name']} - ${option['price']}")
            else:
                print("❌ No housing codes found in database")
                all_passed = False
            
            # Check that old codes don't exist
            old_codes = db_manager.execute_query(
                "SELECT code FROM options WHERE code IN ('SSHSE', 'VRHSE')"
            )
            
            if old_codes:
                print(f"❌ Old codes still exist: {[option['code'] for option in old_codes]}")
                all_passed = False
            else:
                print("✅ Old codes successfully removed")
            
            db_manager.disconnect()
        else:
            print("❌ Could not connect to database")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        all_passed = False
    
    # Test backward compatibility with old codes (should fail gracefully)
    print(f"\n🔄 Testing Backward Compatibility")
    print("=" * 40)
    
    old_test_cases = [
        'LS2000-115VAC-S-10"-VRHSE',
        'LS7000-115VAC-S-10"-SSHSE'
    ]
    
    for part_number in old_test_cases:
        print(f"\n🧪 Testing old code: {part_number}")
        
        result = parser.parse_part_number(part_number)
        
        # Should have warnings about unknown options
        warnings = result.get('warnings', [])
        if any('Unknown option' in warning for warning in warnings):
            print(f"   ✅ Correctly flagged as unknown option")
        else:
            print(f"   ❌ Should have flagged as unknown option")
            all_passed = False
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 40)
    
    if all_passed:
        print("✅ All tests passed! New housing codes are working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    success = test_housing_codes()
    sys.exit(0 if success else 1) 
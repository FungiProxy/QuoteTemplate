#!/usr/bin/env python
"""
Test script for the unified template system.
This script tests both single-item and multi-item quote generation.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'export', 'unified_templates'))

from unified_template_processor import generate_unified_quote

def test_single_item_quote():
    """Test single item quote generation."""
    print("Testing single item quote...")
    
    quote_items = [{
        'part_number': 'LS2000-115VAC-S-12',
        'quantity': 2,
        'type': 'main',
        'data': {
            'total_price': 1250.00,
            'voltage': '115VAC',
            'probe_length': 12,
            'supply_voltage': '115VAC',
            'unit_price': '1,250.00',
            'pc_size': '¾"',
            'pc_type': 'NPT',
            'pc_matt': 'SS',
            'pc_rate': '300 PSI',
            'max_pressure': '300 PSI',
            'ins_material': 'UHMWPE',
            'ins_length': '4"',
            'ins_long': 'Long',
            'ins_temp': '450',
            'probe_size': '½',
            'probe_material': '316SS'
        }
    }]
    
    success = generate_unified_quote(
        quote_items=quote_items,
        customer_name="ACME Industrial Solutions",
        attention_name="John Smith, P.E.",
        quote_number="Q-2024-UNIFIED-SINGLE-001",
        output_path="test_unified_single_item.docx",
        lead_time="6-8 weeks"
    )
    
    if success:
        print("✅ Single item quote generated successfully: test_unified_single_item.docx")
        return True
    else:
        print("❌ Single item quote generation failed")
        return False

def test_multi_item_quote():
    """Test multi-item quote generation with different models."""
    print("Testing multi-item quote with different models...")
    
    quote_items = [
        {
            'part_number': 'LS2000-115VAC-S-12',
            'quantity': 1,
            'type': 'main',
            'data': {
                'total_price': 1250.00,
                'voltage': '115VAC',
                'probe_length': 12,
                'supply_voltage': '115VAC',
                'unit_price': '1,250.00',
                'pc_size': '¾"',
                'pc_type': 'NPT',
                'pc_matt': 'SS',
                'pc_rate': '300 PSI',
                'max_pressure': '300 PSI',
                'ins_material': 'UHMWPE',
                'ins_length': '4"',
                'ins_long': 'Long',
                'ins_temp': '450',
                'probe_size': '½',
                'probe_material': '316SS'
            }
        },
        {
            'part_number': 'LS7000-230VAC-S-18',
            'quantity': 2,
            'type': 'main',
            'data': {
                'total_price': 1850.00,
                'voltage': '230VAC',
                'probe_length': 18,
                'supply_voltage': '230VAC',
                'unit_price': '1,850.00',
                'pc_size': '1"',
                'pc_type': 'NPT',
                'pc_matt': 'SS',
                'pc_rate': '500 PSI',
                'max_pressure': '500 PSI',
                'max_temperature': '750°F',
                'ins_material': 'Teflon',
                'ins_length': '6"',
                'ins_long': 'Long',
                'ins_temp': '500',
                'probe_size': '½',
                'probe_material': '316SS'
            }
        }
    ]
    
    success = generate_unified_quote(
        quote_items=quote_items,
        customer_name="Industrial Manufacturing Co.",
        attention_name="Sarah Johnson",
        quote_number="Q-2024-UNIFIED-MULTI-001",
        output_path="test_unified_multi_item.docx",
        lead_time="8-10 weeks"
    )
    
    if success:
        print("✅ Multi-item quote generated successfully: test_unified_multi_item.docx")
        return True
    else:
        print("❌ Multi-item quote generation failed")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("UNIFIED TEMPLATE SYSTEM TESTS")
    print("=" * 60)
    
    results = []
    
    # Test 1: Single item
    results.append(test_single_item_quote())
    print()
    
    # Test 2: Multi-item
    results.append(test_multi_item_quote())
    print()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your unified template system is working correctly.")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Test script failed with error: {e}")
        import traceback
        traceback.print_exc()
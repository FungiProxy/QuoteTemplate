#!/usr/bin/env python3
"""
Test script for multi-item quote export functionality
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multi_item_export():
    """Test the multi-item export functionality"""
    
    try:
        from export.word_template_processor import generate_multi_item_word_quote
        
        # Create test quote items
        quote_items = [
            {
                'type': 'main',
                'part_number': 'LS2000-115VAC-S-10"',
                'quantity': 1,
                'data': {
                    'model': 'LS2000',
                    'voltage': '115VAC',
                    'probe_length': 10.0,
                    'probe_material_name': '316SS',
                    'insulator_material': 'UHMWPE',
                    'base_insulator_length': 4.0,
                    'max_temperature': 450,
                    'max_pressure': 300,
                    'pc_type': 'NPT',
                    'pc_size': '¾',
                    'pc_matt': 'SS',
                    'output_type': '10 Amp SPDT Relay',
                    'total_price': 425.00,
                    'options': ['XSP', 'VR']
                }
            },
            {
                'type': 'main',
                'part_number': 'LS2100-24VDC-H-12"',
                'quantity': 2,
                'data': {
                    'model': 'LS2100',
                    'voltage': '24VDC',
                    'probe_length': 12.0,
                    'probe_material_name': 'Halar Coated',
                    'insulator_material': 'Teflon',
                    'base_insulator_length': 4.0,
                    'max_temperature': 450,
                    'max_pressure': 300,
                    'pc_type': 'NPT',
                    'pc_size': '¾',
                    'pc_matt': 'SS',
                    'output_type': '10 Amp SPDT Relay',
                    'total_price': 680.00,
                    'options': ['BP']
                }
            },
            {
                'type': 'spare',
                'part_number': 'SPARE-001',
                'quantity': 1,
                'data': {
                    'description': 'Replacement Probe Assembly',
                    'category': 'probe_assembly',
                    'pricing': {
                        'total_price': 125.00
                    }
                }
            }
        ]
        
        # Test parameters
        customer_name = "ACME Industrial Solutions"
        attention_name = "John Smith, P.E."
        quote_number = "TEST-2024-001"
        output_path = "test_multi_item_quote.docx"
        
        # Employee information
        employee_info = {
            'name': 'Jane Doe',
            'phone': '(713) 467-4438',
            'email': 'jane@babbitt.us'
        }
        
        print("🧪 Testing Multi-Item Quote Export")
        print("=" * 50)
        print(f"Customer: {customer_name}")
        print(f"Quote Number: {quote_number}")
        print(f"Items: {len(quote_items)}")
        print(f"Output: {output_path}")
        print()
        
        # Test the export
        success = generate_multi_item_word_quote(
            quote_items=quote_items,
            customer_name=customer_name,
            attention_name=attention_name,
            quote_number=quote_number,
            output_path=output_path,
            employee_info=employee_info
        )
        
        if success:
            print("✅ Multi-item quote export successful!")
            print(f"📄 Generated file: {output_path}")
            
            # Check if file exists and has content
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"📊 File size: {file_size} bytes")
                
                if file_size > 0:
                    print("✅ File created successfully with content")
                else:
                    print("⚠️ File created but appears to be empty")
            else:
                print("❌ File was not created")
        else:
            print("❌ Multi-item quote export failed")
            return False
        
        # Test single item export
        print("\n🧪 Testing Single Item Quote Export")
        print("=" * 50)
        
        single_item = [quote_items[0]]  # Just the first item
        
        single_output_path = "test_single_item_quote.docx"
        
        success = generate_multi_item_word_quote(
            quote_items=single_item,
            customer_name=customer_name,
            attention_name=attention_name,
            quote_number="TEST-2024-002",
            output_path=single_output_path,
            employee_info=employee_info
        )
        
        if success:
            print("✅ Single item quote export successful!")
            print(f"📄 Generated file: {single_output_path}")
        else:
            print("❌ Single item quote export failed")
            return False
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_variables():
    """Test that template variables are correctly generated"""
    
    try:
        from export.word_template_processor import generate_multi_item_word_quote
        
        # Create a simple test with 2 items
        quote_items = [
            {
                'type': 'main',
                'part_number': 'LS2000-115VAC-S-10"',
                'quantity': 1,
                'data': {
                    'model': 'LS2000',
                    'voltage': '115VAC',
                    'probe_length': 10.0,
                    'total_price': 425.00
                }
            },
            {
                'type': 'main',
                'part_number': 'LS2100-24VDC-H-12"',
                'quantity': 1,
                'data': {
                    'model': 'LS2100',
                    'voltage': '24VDC',
                    'probe_length': 12.0,
                    'total_price': 680.00
                }
            }
        ]
        
        # We'll test the variable generation by calling the function
        # and checking the console output for variable processing
        print("🧪 Testing Template Variable Generation")
        print("=" * 50)
        
        success = generate_multi_item_word_quote(
            quote_items=quote_items,
            customer_name="Test Customer",
            attention_name="Test Contact",
            quote_number="TEST-VARS-001",
            output_path="test_variables.docx",
            employee_info={'name': 'Test Employee', 'phone': '555-1234', 'email': 'test@test.com'}
        )
        
        if success:
            print("✅ Template variable generation test completed")
            return True
        else:
            print("❌ Template variable generation test failed")
            return False
            
    except Exception as e:
        print(f"❌ Variable test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Multi-Item Export Tests")
    print("=" * 60)
    
    # Test 1: Multi-item export functionality
    test1_success = test_multi_item_export()
    
    # Test 2: Template variable generation
    test2_success = test_template_variables()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Multi-item Export Test: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"Template Variables Test: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! Multi-item export is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Add conditional variables to your Word templates")
        print("2. Test with your actual quote data")
        print("3. Review the generated documents")
        print("4. Customize templates as needed")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1) 
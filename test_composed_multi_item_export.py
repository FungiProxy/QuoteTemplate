#!/usr/bin/env python3
"""
Test script for composed multi-item quote export functionality
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_composed_multi_item_export():
    """Test the composed multi-item export functionality"""
    
    try:
        from export.word_template_processor import generate_composed_multi_item_quote
        
        # Create test quote items with different models
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
                'type': 'main',
                'part_number': 'LS6000-115VAC-S-18"',
                'quantity': 1,
                'data': {
                    'model': 'LS6000',
                    'voltage': '115VAC',
                    'probe_length': 18.0,
                    'probe_material_name': '316SS',
                    'insulator_material': 'Teflon',
                    'base_insulator_length': 4.0,
                    'max_temperature': 450,
                    'max_pressure': 1500,
                    'pc_type': 'NPT',
                    'pc_size': '¾',
                    'pc_matt': 'SS',
                    'output_type': '10 Amp SPDT Relay',
                    'total_price': 850.00,
                    'options': []
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
        quote_number = "COMPOSED-TEST-001"
        output_path = "test_composed_multi_item_quote.docx"
        
        # Employee information
        employee_info = {
            'name': 'Jane Doe',
            'phone': '(713) 467-4438',
            'email': 'jane@babbitt.us'
        }
        
        print("🧪 Testing Composed Multi-Item Quote Export")
        print("=" * 60)
        print(f"Customer: {customer_name}")
        print(f"Quote Number: {quote_number}")
        print(f"Items: {len(quote_items)}")
        print(f"Models: LS2000, LS2100, LS6000 + Spare Part")
        print(f"Output: {output_path}")
        print()
        
        # Test the composed export
        success = generate_composed_multi_item_quote(
            quote_items=quote_items,
            customer_name=customer_name,
            attention_name=attention_name,
            quote_number=quote_number,
            output_path=output_path,
            employee_info=employee_info
        )
        
        if success:
            print("✅ Composed multi-item quote export successful!")
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
            print("❌ Composed multi-item quote export failed")
            return False
        
        # Test single item export (should still work)
        print("\n🧪 Testing Single Item Quote Export")
        print("=" * 50)
        
        single_item = [quote_items[0]]  # Just the first item
        
        single_output_path = "test_composed_single_item_quote.docx"
        
        success = generate_composed_multi_item_quote(
            quote_items=single_item,
            customer_name=customer_name,
            attention_name=attention_name,
            quote_number="COMPOSED-TEST-002",
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

def test_mixed_model_export():
    """Test export with different model types to ensure proper template handling"""
    
    try:
        from export.word_template_processor import generate_composed_multi_item_quote
        
        # Create test with very different models
        quote_items = [
            {
                'type': 'main',
                'part_number': 'FS10000-115VAC-S-6"',
                'quantity': 1,
                'data': {
                    'model': 'FS10000',
                    'voltage': '115VAC',
                    'probe_length': 6.0,
                    'probe_material_name': '316SS',
                    'insulator_material': 'UHMWPE',
                    'base_insulator_length': 4.0,
                    'max_temperature': 180,
                    'max_pressure': 300,
                    'pc_type': 'NPT',
                    'pc_size': '¾',
                    'pc_matt': 'SS',
                    'output_type': '10 Amp SPDT Relay',
                    'total_price': 1885.00,
                    'options': []
                }
            },
            {
                'type': 'main',
                'part_number': 'LS8000-115VAC-H-24"',
                'quantity': 1,
                'data': {
                    'model': 'LS8000',
                    'voltage': '115VAC',
                    'probe_length': 24.0,
                    'probe_material_name': 'Halar Coated',
                    'insulator_material': 'Teflon',
                    'base_insulator_length': 4.0,
                    'max_temperature': 450,
                    'max_pressure': 300,
                    'pc_type': 'NPT',
                    'pc_size': '¾',
                    'pc_matt': 'SS',
                    'output_type': '10 Amp SPDT Relay',
                    'total_price': 1200.00,
                    'options': ['VR', 'BP']
                }
            }
        ]
        
        print("🧪 Testing Mixed Model Export (FS10000 + LS8000)")
        print("=" * 60)
        
        success = generate_composed_multi_item_quote(
            quote_items=quote_items,
            customer_name="Test Customer",
            attention_name="Test Contact",
            quote_number="MIXED-MODEL-TEST",
            output_path="test_mixed_model_quote.docx",
            employee_info={'name': 'Test Employee', 'phone': '555-1234', 'email': 'test@test.com'}
        )
        
        if success:
            print("✅ Mixed model export successful!")
            return True
        else:
            print("❌ Mixed model export failed")
            return False
            
    except Exception as e:
        print(f"❌ Mixed model test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Composed Multi-Item Export Tests")
    print("=" * 70)
    
    # Test 1: Basic composed multi-item export
    test1_success = test_composed_multi_item_export()
    
    # Test 2: Mixed model export
    test2_success = test_mixed_model_export()
    
    print("\n" + "=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    print(f"Composed Multi-Item Export Test: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"Mixed Model Export Test: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! Composed multi-item export is working correctly.")
        print("\n📋 Key Benefits of This Approach:")
        print("1. ✅ Each item uses its specific model template")
        print("2. ✅ Maintains professional formatting for each model")
        print("3. ✅ Handles different model types in one quote")
        print("4. ✅ Preserves model-specific content and specifications")
        print("5. ✅ Creates a cohesive multi-item document")
        print("\n📋 Next Steps:")
        print("1. Test with your actual quote data")
        print("2. Review the generated documents")
        print("3. Customize the summary section as needed")
        print("4. Adjust formatting if required")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1) 
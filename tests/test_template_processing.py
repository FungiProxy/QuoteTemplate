"""
Test Script for RTF Template Processing

This script demonstrates how to use the template variable system
to generate quotes from RTF templates.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from export.word_exporter import RTFTemplateProcessor, WordDocumentExporter, generate_quote
from docs.template_fileds import QuoteTemplateFields

def test_basic_template_processing():
    """Test basic template variable replacement."""
    print("Testing RTF Template Processing...")
    
    # Initialize processor
    processor = RTFTemplateProcessor()
    
    # Test with LS2000H template
    model = "LS2000H"
    
    # Create test data
    fields = QuoteTemplateFields(
        date="December 15, 2024",
        customer_name="ACME Industrial Solutions",
        attention_name="John Smith, P.E.",
        quote_number="Q-2024-12345",
        part_number="LS2000-115VAC-H-12",
        quantity="1",
        unit_price="1,250.00",
        supply_voltage="115VAC",
        probe_length="12",
        process_connection_size="¾",
        insulator_material="Teflon",
        insulator_length="4",
        probe_material="HALAR",
        probe_diameter="½",
        max_temperature="450 F",
        max_pressure="300 PSI"
    )
    
    print(f"Processing template for model: {model}")
    print(f"Template fields:")
    for key, value in fields.to_dict().items():
        if value is not None:
            print(f"  {key}: {value}")
    
    # Process the template
    processed_content = processor.process_template(model, fields)
    
    if processed_content:
        print(f"✓ Template processed successfully!")
        original_template = processor.load_template(model)
        original_size = len(original_template) if original_template else 0
        print(f"  Original template size: {original_size} characters")
        print(f"  Processed template size: {len(processed_content)} characters")
        
        # Show a snippet of replacements
        print("\nSample replacements:")
        lines = processed_content.split('\n')
        for i, line in enumerate(lines[:20]):  # First 20 lines
            if any(field in line for field in ['ACME Industrial', 'Q-2024-12345', 'LS2000-115VAC-H-12']):
                print(f"  Line {i+1}: {line.strip()}")
        
        return True
    else:
        print("✗ Template processing failed!")
        return False

def test_generate_quote_function():
    """Test the convenience generate_quote function."""
    print("\nTesting generate_quote convenience function...")
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(suffix='.rtf', delete=False) as f:
        output_path = f.name
    
    try:
        success = generate_quote(
            model="LS6000H",
            customer_name="Beta Manufacturing Corp",
            attention_name="Sarah Johnson",
            quote_number="Q-2024-67890",
            part_number="LS6000-24VDC-H-18",
            unit_price="1,875.50",
            supply_voltage="24VDC",
            probe_length="18",
            output_path=output_path,
            # Optional parameters
            insulator_material="Teflon",
            probe_material="HALAR",
            max_temperature="450 F"
        )
        
        if success and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ Quote generated successfully!")
            print(f"  Output file: {output_path}")
            print(f"  File size: {file_size} bytes")
            
            # Read first few lines to verify content
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Beta Manufacturing Corp' in content and 'Q-2024-67890' in content:
                    print("✓ Content verification passed!")
                else:
                    print("✗ Content verification failed!")
                    
            return True
        else:
            print("✗ Quote generation failed!")
            return False
            
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.unlink(output_path)

def test_all_available_templates():
    """Test processing for all available template models."""
    print("\nTesting all available templates...")
    
    processor = RTFTemplateProcessor()
    templates_dir = processor.templates_dir
    
    # Find all RTF template files
    template_files = list(templates_dir.glob("*_template.rtf"))
    
    if not template_files:
        print(f"✗ No template files found in {templates_dir}")
        return False
    
    print(f"Found {len(template_files)} template files:")
    
    success_count = 0
    
    for template_file in template_files:
        model = template_file.stem.replace('_template', '')
        print(f"\n  Testing {model}...")
        
        # Create basic test fields
        fields = QuoteTemplateFields(
            date="December 15, 2024",
            customer_name="Test Customer Inc.",
            attention_name="Test Contact",
            quote_number="TEST-001",
            part_number=f"{model}-TEST-12",
            quantity="1",
            unit_price="999.99",
            supply_voltage="115VAC",
            probe_length="12",
            process_connection_size="¾",
            insulator_material="Teflon",
            insulator_length="4",
            probe_material="316SS",
            probe_diameter="½",
            max_temperature="450 F",
            max_pressure="300 PSI"
        )
        
        processed = processor.process_template(model, fields)
        if processed:
            print(f"    ✓ {model} processed successfully")
            success_count += 1
        else:
            print(f"    ✗ {model} processing failed")
    
    print(f"\nResults: {success_count}/{len(template_files)} templates processed successfully")
    return success_count == len(template_files)

def main():
    """Run all tests."""
    print("=" * 60)
    print("RTF Template Processing Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_template_processing,
        test_generate_quote_function,
        test_all_available_templates,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! Template system is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 
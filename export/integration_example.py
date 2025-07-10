"""
Integration Example: Template System with Quote Generation

This example shows how to integrate the RTF template processing
with your existing quote generation and pricing system.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import new template system
from export.word_exporter import generate_quote
from docs.template_fileds import QuoteTemplateFields

# Note: These imports would be used in actual integration
# from core.quote_generator import QuoteGenerator
# from core.pricing_engine import PricingEngine  
# from core.part_parser import PartParser

class IntegratedQuoteExporter:
    """
    Integrated quote exporter that combines existing quote generation
    with the new RTF template system.
    """
    
    def __init__(self):
        # Note: In actual implementation, these would be initialized:
        # self.quote_generator = QuoteGenerator()
        # self.pricing_engine = PricingEngine()
        # self.part_parser = PartParser()
        pass
    
    def generate_quote_document(
        self,
        part_number: str,
        customer_name: str,
        attention_name: str = "",
        quote_number: str = "",
        output_path: str = "",
        format: str = 'rtf'
    ) -> bool:
        """
        Generate a complete quote document from a part number.
        
        Args:
            part_number: The part number to quote
            customer_name: Customer company name
            attention_name: Contact person name
            quote_number: Quote number (auto-generated if None)
            output_path: Output file path (auto-generated if None)
            format: Output format ('rtf' or 'docx')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Parse the part number to get model and specifications
            # In actual implementation: parsed_part = self.part_parser.parse_part_number(part_number)
            parsed_part = self._mock_parse_part_number(part_number)
            if not parsed_part:
                print(f"Error: Could not parse part number: {part_number}")
                return False
            
            model = parsed_part.get('model', '')
            print(f"Model identified: {model}")
            
            # Step 2: Generate pricing
            # In actual implementation: pricing_result = self.pricing_engine.calculate_pricing(parsed_part)
            unit_price = self._mock_calculate_price(parsed_part)
            print(f"Unit price calculated: ${unit_price}")
            
            # Step 3: Extract technical specifications
            specs = self._extract_specifications(parsed_part)
            
            # Step 4: Generate quote number if not provided
            if not quote_number:
                quote_number = self._generate_quote_number()
            
            # Step 5: Generate output path if not provided
            if not output_path:
                safe_customer = "".join(c for c in customer_name if c.isalnum() or c in (' ', '-', '_')).strip()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Quote_{safe_customer}_{quote_number}_{timestamp}.{format}"
                output_path = os.path.join('output', filename)
                
                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Step 6: Generate the quote document using template system
            success = generate_quote(
                model=model,
                customer_name=customer_name,
                attention_name=attention_name,
                quote_number=quote_number,
                part_number=part_number,
                unit_price=unit_price,
                supply_voltage=specs.get('supply_voltage', '115VAC'),
                probe_length=specs.get('probe_length', '12'),
                output_path=output_path,
                # Additional technical specifications
                **specs
            )
            
            if success:
                print(f"✓ Quote document generated successfully!")
                print(f"  Output file: {output_path}")
                print(f"  Customer: {customer_name}")
                print(f"  Part Number: {part_number}")
                print(f"  Quote Number: {quote_number}")
                print(f"  Unit Price: ${unit_price}")
                return True
            else:
                print(f"✗ Failed to generate quote document")
                return False
                
        except Exception as e:
            print(f"Error generating quote: {e}")
            return False
    
    def _extract_specifications(self, parsed_part: dict) -> dict:
        """
        Extract technical specifications from parsed part data.
        
        Args:
            parsed_part: Parsed part number data
            
        Returns:
            Dictionary of technical specifications
        """
        specs = {}
        
        # Extract common specifications
        specs['supply_voltage'] = parsed_part.get('voltage', '115VAC')
        specs['probe_length'] = str(parsed_part.get('length', 12))
        specs['process_connection_size'] = parsed_part.get('connection_size', '¾')
        
        # Extract insulator information
        insulator_code = parsed_part.get('insulator_code', 'H')
        if insulator_code == 'H':
            specs['insulator_material'] = 'Teflon'
            specs['probe_material'] = 'HALAR'
            specs['max_temperature'] = '450 F'
        elif insulator_code == 'S':
            specs['insulator_material'] = 'UHMPE'
            specs['probe_material'] = '316SS'
            specs['max_temperature'] = '180 F'
        else:
            specs['insulator_material'] = 'Teflon'
            specs['probe_material'] = '316SS'
            specs['max_temperature'] = '450 F'
        
        # Set other common defaults
        specs['insulator_length'] = '4'
        specs['probe_diameter'] = '½'
        specs['max_pressure'] = '300 PSI'
        
        # Model-specific specifications
        model = parsed_part.get('model', '')
        if model.startswith('LS6000') or model.startswith('LS7000'):
            specs['max_pressure'] = '1500 PSI'
            specs['process_connection_size'] = '1'
        elif model.startswith('LS7500') or model.startswith('LS8500'):
            specs['flange_size'] = parsed_part.get('flange_size', '150#')
            specs['sensor_type'] = 'Partial Ring' if 'PR' in parsed_part.get('options', []) else 'Full Ring'
        
        return specs
    
    def _generate_quote_number(self) -> str:
        """Generate a unique quote number."""
        timestamp = datetime.now()
        return f"Q-{timestamp.strftime('%Y-%m')}-{timestamp.strftime('%d%H%M')}"
    
    def _mock_parse_part_number(self, part_number: str) -> dict:
        """Mock implementation of part number parsing for demonstration."""
        # Extract model from part number
        model = part_number.split('-')[0] if '-' in part_number else part_number[:6]
        
        # Mock parsed part data
        return {
            'model': model,
            'voltage': '115VAC' if '115VAC' in part_number else '24VDC',
            'length': int(part_number.split('-')[-1]) if part_number.split('-')[-1].isdigit() else 12,
            'insulator_code': 'H' if '-H-' in part_number else 'S',
            'connection_size': '¾',
            'options': []
        }
    
    def _mock_calculate_price(self, parsed_part: dict) -> str:
        """Mock implementation of pricing calculation for demonstration."""
        base_prices = {
            'LS2000': '1250.00',
            'LS6000': '1875.00', 
            'LS7000': '2100.00',
            'LS7500': '2450.00',
            'LS8000': '1950.00',
            'LS8500': '2350.00',
            'LT9000': '2750.00',
            'FS10000': '1650.00'
        }
        
        model = parsed_part.get('model', '')
        for prefix, price in base_prices.items():
            if model.startswith(prefix):
                return price
        
        return '1500.00'  # Default price

# Example usage functions
def example_basic_quote():
    """Example: Generate a basic quote."""
    print("Example 1: Basic Quote Generation")
    print("-" * 40)
    
    exporter = IntegratedQuoteExporter()
    
    success = exporter.generate_quote_document(
        part_number="LS2000-115VAC-H-12",
        customer_name="Acme Manufacturing Corp",
        attention_name="John Smith, Engineering Manager",
        quote_number="Q-2024-001"
    )
    
    if success:
        print("✓ Basic quote generated successfully!")
    else:
        print("✗ Basic quote generation failed!")
    
    return success

def example_multiple_quotes():
    """Example: Generate multiple quotes for different models."""
    print("\nExample 2: Multiple Quote Generation")
    print("-" * 40)
    
    exporter = IntegratedQuoteExporter()
    
    quotes = [
        {
            'part_number': 'LS6000-24VDC-H-18',
            'customer': 'Beta Industrial Systems',
            'contact': 'Sarah Johnson'
        },
        {
            'part_number': 'FS10000-115VAC-S-24',
            'customer': 'Gamma Process Controls',
            'contact': 'Mike Wilson'
        },
        {
            'part_number': 'LT9000-24VDC-H-15',
            'customer': 'Delta Automation',
            'contact': 'Lisa Chen'
        }
    ]
    
    success_count = 0
    
    for i, quote_data in enumerate(quotes, 1):
        print(f"\nGenerating quote {i}/{len(quotes)}...")
        success = exporter.generate_quote_document(
            part_number=quote_data['part_number'],
            customer_name=quote_data['customer'],
            attention_name=quote_data['contact']
        )
        
        if success:
            success_count += 1
    
    print(f"\nResults: {success_count}/{len(quotes)} quotes generated successfully")
    return success_count == len(quotes)

def example_custom_specifications():
    """Example: Generate quote with custom specifications."""
    print("\nExample 3: Custom Specifications")
    print("-" * 40)
    
    # This example shows how you could manually create a quote
    # with custom specifications using the template system directly
    
    from export.word_exporter import generate_quote
    
    success = generate_quote(
        model="LS7000H",
        customer_name="Custom Solutions Inc.",
        attention_name="Robert Taylor, Lead Engineer",
        quote_number="Q-CUSTOM-001",
        part_number="LS7000-230VAC-H-30",
        unit_price="2,450.00",
        supply_voltage="230VAC",
        probe_length="30",
        output_path="output/custom_quote_example.rtf",
        # Custom specifications
        insulator_material="Teflon",
        probe_material="HALAR",
        max_temperature="450 F",
        max_pressure="1500 PSI",
        process_connection_size="1"
    )
    
    if success:
        print("✓ Custom quote generated successfully!")
        print("  File: output/custom_quote_example.rtf")
    else:
        print("✗ Custom quote generation failed!")
    
    return success

def main():
    """Run integration examples."""
    print("=" * 60)
    print("RTF Template Integration Examples")
    print("=" * 60)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    examples = [
        example_basic_quote,
        example_multiple_quotes,
        example_custom_specifications,
    ]
    
    passed = 0
    total = len(examples)
    
    for example in examples:
        try:
            if example():
                passed += 1
        except Exception as e:
            print(f"✗ Example failed with exception: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"Integration Examples: {passed}/{total} completed successfully")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All examples completed! Integration system is working.")
    else:
        print("⚠️  Some examples failed. Check your existing modules.")

if __name__ == "__main__":
    main() 
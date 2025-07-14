import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from core.part_parser import PartNumberParser

def test_1_2_npt_pricing():
    """Test that 1/2 inch NPT process connections are properly parsed and priced"""
    
    parser = PartNumberParser()
    
    # Test part numbers with 1/2 inch NPT
    test_cases = [
        "LS2000-115VAC-S-10\"-1/2\"NPT",
        "LS2100-24VDC-H-12\"-1/2\"NPT",
        "LS6000-115VAC-S-14\"-XSP-1/2\"NPT"
    ]
    
    print("Testing 1/2 inch NPT process connection pricing...")
    print("=" * 50)
    
    for part_number in test_cases:
        print(f"\nParsing: {part_number}")
        print("-" * 30)
        
        result = parser.parse_part_number(part_number)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            continue
        
        # Check if process connection was parsed correctly
        process_connection = result.get('process_connection')
        if process_connection:
            print(f"✅ Process Connection: {process_connection['display']}")
            print(f"   Type: {process_connection['type']}")
            print(f"   Size: {process_connection['size']}")
        else:
            print("❌ No process connection found")
            continue
        
        # Check pricing
        pricing = result.get('pricing', {})
        if pricing.get('connection_cost', 0) > 0:
            print(f"✅ Connection Cost: ${pricing['connection_cost']:.2f}")
        else:
            print("❌ No connection cost found")
        
        # Check total price
        total_price = pricing.get('total_price', 0)
        print(f"💰 Total Price: ${total_price:.2f}")
        
        # Verify the connection cost is $25.00
        connection_cost = pricing.get('connection_cost', 0)
        if connection_cost == 25.0:
            print("✅ 1/2 inch NPT pricing correctly applied ($25.00)")
        else:
            print(f"❌ Expected $25.00 connection cost, got ${connection_cost:.2f}")

if __name__ == "__main__":
    test_1_2_npt_pricing() 
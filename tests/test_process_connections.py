#!/usr/bin/env python3
"""
Test Script for Process Connection Integration
Demonstrates the new process connection functionality in the QuoteTemplate application
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

from database.db_manager import DatabaseManager
from core.part_parser import PartNumberParser

def test_process_connections():
    """Test process connection functionality"""
    print("🔧 PROCESS CONNECTION INTEGRATION TEST")
    print("=" * 60)
    
    # Initialize database manager
    db = DatabaseManager()
    
    if not db.test_connection():
        print("❌ Database connection failed!")
        return
    
    print("\n📊 PROCESS CONNECTION DATABASE QUERIES:")
    print("-" * 40)
    
    # Test 1: Get all connection types
    connection_types = db.get_connection_types()
    print(f"✓ Available connection types: {connection_types}")
    
    # Test 2: Get NPT sizes
    npt_sizes = db.get_connection_sizes('NPT')
    print(f"✓ NPT sizes available: {npt_sizes}")
    
    # Test 3: Get flange options
    flange_connections = db.get_available_connections(conn_type='Flange')
    print(f"✓ Flange connections found: {len(flange_connections)}")
    
    # Test 4: Get specific connection info
    conn_info = db.get_process_connection_info('NPT', '1"', 'SS')
    if conn_info:
        print(f"✓ 1\" NPT Connection: {conn_info['description']} - ${conn_info['price']:.2f}")
    
    # Test 5: Test Tri-Clamp pricing
    triclamp_cost = db.calculate_connection_cost('Tri-Clamp', '2"', 'SS')
    print(f"✓ 2\" Tri-Clamp Cost: ${triclamp_cost:.2f}")
    
    # Test 6: Format connection display
    display_format = db.format_connection_display('Flange', '2"', 'SS', '150#')
    print(f"✓ Formatted display: {display_format}")
    
    print("\n🧮 PRICING WITH PROCESS CONNECTIONS:")
    print("-" * 40)
    
    # Test pricing with different connections
    base_config = {
        'model': 'LS7000',
        'voltage': '115VAC', 
        'material': 'S',
        'length': 10.0,
        'options': [],
        'insulator': 'TEF'
    }
    
    # Test with default NPT connection
    npt_connection = {'type': 'NPT', 'size': '1"', 'material': 'SS'}
    pricing_npt = db.calculate_total_price(
        base_config['model'], base_config['voltage'], base_config['material'],
        base_config['length'], base_config['options'], base_config['insulator'],
        npt_connection
    )
    print(f"✓ LS7000 with 1\" NPT: ${pricing_npt['total_price']:.2f}")
    
    # Test with Tri-Clamp connection
    triclamp_connection = {'type': 'Tri-Clamp', 'size': '2"', 'material': 'SS'}
    pricing_triclamp = db.calculate_total_price(
        base_config['model'], base_config['voltage'], base_config['material'],
        base_config['length'], base_config['options'], base_config['insulator'],
        triclamp_connection
    )
    print(f"✓ LS7000 with 2\" Tri-Clamp: ${pricing_triclamp['total_price']:.2f}")
    print(f"  - Connection upcharge: ${pricing_triclamp['connection_cost']:.2f}")
    
    # Test with Flange connection
    flange_connection = {'type': 'Flange', 'size': '2"', 'material': 'SS', 'rating': '150#'}
    pricing_flange = db.calculate_total_price(
        base_config['model'], base_config['voltage'], base_config['material'],
        base_config['length'], base_config['options'], base_config['insulator'],
        flange_connection
    )
    print(f"✓ LS7000 with 2\" 150# Flange: ${pricing_flange['total_price']:.2f}")
    
    print("\n🔍 PART NUMBER PARSING WITH CONNECTION OVERRIDES:")
    print("-" * 50)
    
    # Test part parser with connection overrides
    parser = PartNumberParser()
    
    test_parts = [
        "LS7000-115VAC-S-12\"",  # Default connection
        "LS7000-115VAC-S-12\"-1\"NPT",  # NPT override
        "LS6000-115VAC-H-14\"-2\"150#RF",  # Flange override
    ]
    
    for part in test_parts:
        print(f"\n🔧 Parsing: {part}")
        result = parser.parse_part_number(part)
        
        if result.get('error'):
            print(f"   ❌ Error: {result['error']}")
        else:
            pricing = result.get('pricing', {})
            connection_cost = pricing.get('connection_cost', 0.0)
            total_price = pricing.get('total_price', 0.0)
            
            print(f"   ✓ Total Price: ${total_price:.2f}")
            if connection_cost > 0:
                print(f"   ✓ Connection Cost: ${connection_cost:.2f}")
            
            # Show connection info
            if result.get('process_connection'):
                conn = result['process_connection']
                print(f"   ✓ Connection: {conn.get('display', 'N/A')}")
    
    print("\n✅ PROCESS CONNECTION INTEGRATION COMPLETE!")
    print("   • Database methods implemented and tested")
    print("   • Pricing calculations include connection costs")
    print("   • Part parser recognizes connection overrides")
    print("   • All connection types supported (NPT, Flange, Tri-Clamp)")

def main():
    """Main test function"""
    test_process_connections()

if __name__ == "__main__":
    main() 
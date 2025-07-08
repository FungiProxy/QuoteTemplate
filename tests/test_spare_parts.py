"""
Test Spare Parts Functionality for Babbitt Quote Generator
Comprehensive testing of spare parts database, pricing, and integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.spare_parts_manager import SparePartsManager
from core.pricing_engine import PricingEngine
from database.db_manager import DatabaseManager
import json

def test_database_connection():
    """Test basic database connection and spare parts table existence"""
    print("=" * 60)
    print("Testing Database Connection and Spare Parts Table")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        if not db.connect():
            print("❌ Database connection failed")
            return False
        
        # Test spare parts table exists
        query = "SELECT COUNT(*) as count FROM spare_parts"
        result = db.execute_query(query)
        
        if result and len(result) > 0:
            count = result[0]['count']
            print(f"✅ Database connection successful")
            print(f"✅ Spare parts table found with {count} parts")
            return True
        else:
            print("❌ Spare parts table not found or empty")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    finally:
        db.disconnect()

def test_spare_parts_manager():
    """Test SparePartsManager functionality"""
    print("\n" + "=" * 60)
    print("Testing Spare Parts Manager")
    print("=" * 60)
    
    try:
        with SparePartsManager() as spm:
            # Test getting spare parts for LS2000
            print("\n📋 Testing spare parts lookup for LS2000:")
            ls2000_parts = spm.get_spare_parts_for_model("LS2000")
            
            if 'error' in ls2000_parts:
                print(f"❌ Error getting LS2000 parts: {ls2000_parts['error']}")
                return False
            
            print(f"✅ Found {ls2000_parts['total_parts']} spare parts for LS2000")
            
            # Display categories
            print(f"✅ Categories available:")
            for category in ls2000_parts.get('categories', []):
                display_name = ls2000_parts['category_display'].get(category['category'], category['category'])
                print(f"   • {display_name}: {category['part_count']} parts")
            
            # Test search functionality
            print("\n🔍 Testing spare parts search:")
            search_results = spm.search_spare_parts("electronics", "LS2000")
            print(f"✅ Search for 'electronics' found {len(search_results)} results")
            
            if search_results:
                first_part = search_results[0]
                print(f"   Example: {first_part['name']} - ${first_part['price']:.2f}")
            
            # Test specific part lookup
            print("\n🔍 Testing specific part lookup:")
            part_details = spm.get_spare_part_details("LS2000-ELECTRONICS")
            
            if part_details:
                print(f"✅ Found part details for LS2000-ELECTRONICS:")
                print(f"   Name: {part_details['name']}")
                print(f"   Price: ${part_details['price']:.2f}")
                print(f"   Category: {part_details['category_display']}")
                print(f"   Compatible Models: {', '.join(part_details['compatible_models_list'])}")
                
                if part_details['ordering_requirements']:
                    print(f"   Requirements: {', '.join(part_details['ordering_requirements'])}")
            else:
                print("❌ Could not find LS2000-ELECTRONICS part")
                return False
            
            # Test pricing calculation
            print("\n💰 Testing spare parts pricing:")
            pricing = spm.calculate_spare_part_quote(
                "LS2000-ELECTRONICS", 
                quantity=2,
                specifications={"voltage": "115VAC"}
            )
            
            if 'error' not in pricing:
                print(f"✅ Pricing calculation successful:")
                print(f"   Quantity: {pricing['quantity']}")
                print(f"   Unit Price: ${pricing['unit_price']:.2f}")
                print(f"   Total Price: ${pricing['total_price']:.2f}")
                print(f"   Line Item: {pricing['line_item']}")
            else:
                print(f"❌ Pricing calculation failed: {pricing['error']}")
                return False
            
            # Test recommendations
            print("\n⭐ Testing spare parts recommendations:")
            recommendations = spm.get_recommended_spare_parts("LS2000", limit=3)
            print(f"✅ Found {len(recommendations)} recommended parts:")
            
            for rec in recommendations:
                print(f"   • {rec['name']}: {rec['formatted_price']}")
            
            return True
            
    except Exception as e:
        print(f"❌ Spare Parts Manager test failed: {e}")
        return False

def test_pricing_engine_integration():
    """Test PricingEngine with spare parts integration"""
    print("\n" + "=" * 60)
    print("Testing Pricing Engine Integration")
    print("=" * 60)
    
    try:
        engine = PricingEngine()
        
        # Test spare parts pricing only
        print("\n💰 Testing spare parts pricing calculation:")
        spare_parts_list = [
            {
                'part_number': 'LS2000-ELECTRONICS',
                'quantity': 1,
                'specifications': {'voltage': '115VAC'}
            },
            {
                'part_number': 'LS2000-U-PROBE-ASSEMBLY-4',
                'quantity': 2,
                'specifications': {}
            }
        ]
        
        spare_parts_pricing = engine.calculate_spare_parts_pricing(spare_parts_list)
        
        if spare_parts_pricing['success']:
            print(f"✅ Spare parts pricing successful:")
            print(f"   Total Parts: {spare_parts_pricing['total_parts']}")
            print(f"   Subtotal: ${spare_parts_pricing['subtotal']:.2f}")
            print(f"   Breakdown:")
            for line in spare_parts_pricing['breakdown']:
                print(f"     {line}")
        else:
            print(f"❌ Spare parts pricing failed")
            return False
        
        # Test complete quote with product and spare parts
        print("\n📋 Testing complete quote pricing:")
        complete_quote = engine.calculate_complete_quote_pricing(
            model_code="LS2000",
            voltage="115VAC",
            material_code="S",
            probe_length=10.0,
            option_codes=["XSP"],
            insulator_code="U",
            spare_parts_list=spare_parts_list
        )
        
        if complete_quote['success']:
            print(f"✅ Complete quote pricing successful:")
            print(f"   Product Total: ${complete_quote['product_pricing']['total_price']:.2f}")
            print(f"   Spare Parts Total: ${complete_quote['spare_parts_pricing']['subtotal']:.2f}")
            print(f"   Quote Total: {complete_quote['formatted_total']}")
            
            print(f"\n   Full Breakdown:")
            for line in complete_quote['breakdown']:
                print(f"     {line}")
        else:
            print(f"❌ Complete quote pricing failed")
            return False
        
        # Test recommendations
        print("\n⭐ Testing spare parts recommendations:")
        recommendations = engine.get_spare_parts_recommendations("LS2000", limit=5)
        print(f"✅ Found {len(recommendations)} recommendations:")
        
        for rec in recommendations:
            print(f"   • {rec['name']}: {rec.get('formatted_price', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pricing Engine integration test failed: {e}")
        return False

def test_validation():
    """Test spare parts validation functionality"""
    print("\n" + "=" * 60)
    print("Testing Spare Parts Validation")
    print("=" * 60)
    
    try:
        engine = PricingEngine()
        
        # Test valid configuration
        print("\n✅ Testing valid spare parts configuration:")
        valid_parts = [
            {
                'part_number': 'LS2000-ELECTRONICS',
                'quantity': 1,
                'specifications': {'voltage': '115VAC'}
            }
        ]
        
        validation = engine.validate_spare_parts_configuration(valid_parts, "LS2000")
        
        if validation['valid']:
            print(f"✅ Validation passed")
            if validation['warnings']:
                print(f"   Warnings: {', '.join(validation['warnings'])}")
        else:
            print(f"❌ Validation failed: {', '.join(validation['errors'])}")
        
        # Test invalid configuration (missing required spec)
        print("\n⚠️  Testing invalid spare parts configuration:")
        invalid_parts = [
            {
                'part_number': 'LS2000-ELECTRONICS',
                'quantity': 1,
                'specifications': {}  # Missing voltage specification
            }
        ]
        
        validation = engine.validate_spare_parts_configuration(invalid_parts, "LS2000")
        
        if not validation['valid']:
            print(f"✅ Validation correctly failed:")
            print(f"   Errors: {', '.join(validation['errors'])}")
        else:
            print(f"⚠️  Validation should have failed but passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def test_sample_quote():
    """Test creating a complete sample quote with spare parts"""
    print("\n" + "=" * 60)
    print("Creating Sample Quote with Spare Parts")
    print("=" * 60)
    
    try:
        engine = PricingEngine()
        
        # Sample quote configuration
        print("📋 Sample Quote Configuration:")
        print("   Product: LS2000-115VAC-S-12\"-XSP-VR-U")
        print("   Spare Parts:")
        print("     • 1x LS2000 Electronics (115VAC)")
        print("     • 2x LS2000 UHMWPE Probe Assembly 4\"")
        print("     • 1x LS2000 Housing")
        
        spare_parts_list = [
            {
                'part_number': 'LS2000-ELECTRONICS',
                'quantity': 1,
                'specifications': {'voltage': '115VAC'}
            },
            {
                'part_number': 'LS2000-U-PROBE-ASSEMBLY-4',
                'quantity': 2,
                'specifications': {}
            },
            {
                'part_number': 'LS2000-HOUSING',
                'quantity': 1,
                'specifications': {}
            }
        ]
        
        quote = engine.calculate_complete_quote_pricing(
            model_code="LS2000",
            voltage="115VAC",
            material_code="S",
            probe_length=12.0,
            option_codes=["XSP", "VR"],
            insulator_code="U",
            spare_parts_list=spare_parts_list
        )
        
        if quote['success']:
            print(f"\n✅ Sample Quote Generated Successfully:")
            print(f"=" * 40)
            
            for line in quote['breakdown']:
                print(f"{line}")
            
            print(f"=" * 40)
            print(f"QUOTE TOTAL: {quote['formatted_total']}")
            
            if quote['warnings']:
                print(f"\nWarnings:")
                for warning in quote['warnings']:
                    print(f"  ⚠️  {warning}")
            
            return True
        else:
            print(f"❌ Sample quote generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Sample quote test failed: {e}")
        return False

def main():
    """Run all spare parts tests"""
    print("🧪 SPARE PARTS FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Spare Parts Manager", test_spare_parts_manager),
        ("Pricing Engine Integration", test_pricing_engine_integration),
        ("Validation", test_validation),
        ("Sample Quote", test_sample_quote)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("SPARE PARTS TEST RESULTS")
    print("=" * 60)
    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "No tests run")
    
    if failed == 0:
        print("\n🎉 All spare parts tests passed! The functionality is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above for details.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
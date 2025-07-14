import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from core.pricing_engine import PricingEngine
from database.db_manager import DatabaseManager

class TestInsulatorLengthPricing:
    """Test the insulator length pricing logic"""
    
    def setup_method(self):
        """Set up test environment"""
        self.db_manager = DatabaseManager()
        self.pricing_engine = PricingEngine()
        
        # Connect to database
        if not self.db_manager.connect():
            pytest.skip("Database connection failed")
    
    def teardown_method(self):
        """Clean up test environment"""
        self.db_manager.disconnect()
    
    def test_insulator_length_adder_calculation(self):
        """Test the insulator length adder calculation"""
        # Test the pricing engine method
        test_cases = [
            (4.0, 0.0),    # Base length - no adder
            (5.0, 150.0),  # 5-6" bracket - $150
            (6.0, 150.0),  # 5-6" bracket - $150
            (7.0, 200.0),  # 7-8" bracket - $200
            (8.0, 200.0),  # 7-8" bracket - $200
            (9.0, 250.0),  # 9-10" bracket - $250
            (10.0, 250.0), # 9-10" bracket - $250
            (11.0, 300.0), # 11-12" bracket - $300
            (12.0, 300.0), # 11-12" bracket - $300
            (13.0, 350.0), # 13-14" bracket - $350
            (14.0, 350.0), # 13-14" bracket - $350
            (15.0, 400.0), # 15-16" bracket - $400
            (16.0, 400.0), # 15-16" bracket - $400
            (17.0, 450.0), # 17-18" bracket - $450
            (18.0, 450.0), # 17-18" bracket - $450
            (19.0, 500.0), # 19-20" bracket - $500
            (20.0, 500.0), # 19-20" bracket - $500
            (25.0, 500.0), # Above 20" - capped at $500
        ]
        
        for length, expected_adder in test_cases:
            # Test pricing engine method
            result = self.pricing_engine._calculate_insulator_length_adder(length)
            assert result == expected_adder, f"Length {length}\" should have ${expected_adder} adder, got ${result}"
            
            # Test database manager method
            result = self.db_manager._calculate_insulator_length_adder(length)
            assert result == expected_adder, f"Length {length}\" should have ${expected_adder} adder, got ${result}"
    
    def test_insulator_pricing_with_length(self):
        """Test complete insulator pricing with length adders"""
        # Test Teflon insulator with different lengths
        test_cases = [
            (4.0, 40.0),   # Base Teflon price only
            (5.0, 190.0),  # Base + $150 length adder
            (6.0, 190.0),  # Base + $150 length adder
            (7.0, 240.0),  # Base + $200 length adder
            (8.0, 240.0),  # Base + $200 length adder
            (10.0, 290.0), # Base + $250 length adder
            (15.0, 440.0), # Base + $400 length adder
            (20.0, 540.0), # Base + $500 length adder
        ]
        
        for length, expected_total in test_cases:
            # Test pricing engine
            result = self.pricing_engine._calculate_insulator_pricing('TEF', 'S', 'LS2000', length)
            assert result['cost'] == expected_total, f"Teflon at {length}\" should cost ${expected_total}, got ${result['cost']}"
            
            # Test database manager
            result = self.db_manager.calculate_insulator_cost('TEF', 'S', 'LS2000', length)
            assert result == expected_total, f"Teflon at {length}\" should cost ${expected_total}, got ${result}"
    
    def test_insulator_pricing_without_length(self):
        """Test insulator pricing without length specification"""
        # Test that insulator pricing works without length (backward compatibility)
        result = self.pricing_engine._calculate_insulator_pricing('TEF', 'S', 'LS2000')
        assert result['cost'] == 40.0, f"Teflon without length should cost $40.00, got ${result['cost']}"
        
        result = self.db_manager.calculate_insulator_cost('TEF', 'S', 'LS2000')
        assert result == 40.0, f"Teflon without length should cost $40.00, got ${result}"
    
    def test_complete_pricing_integration(self):
        """Test that insulator length adders are included in complete pricing"""
        # Test a configuration with extended insulator length
        result = self.pricing_engine.calculate_complete_pricing(
            model_code='LS2000',
            voltage='24V',
            material_code='S',
            probe_length=10.0,
            insulator_code='TEF',
            insulator_length=8.0  # Should add $200
        )
        
        # Teflon base price is $40, length adder is $200, total insulator cost should be $240
        assert result['insulator_cost'] == 240.0, f"Insulator cost should be $240.00, got ${result['insulator_cost']}"
        assert result['total_price'] > 0, "Total price should be calculated"
        
        # Verify the length adder is mentioned in breakdown
        breakdown_text = ' '.join(result['breakdown'])
        assert 'Insulator Length Adder' in breakdown_text, "Breakdown should mention the length adder"
        assert '200.00' in breakdown_text, "Breakdown should show $200 length adder"
    
    def test_part_parser_integration(self):
        """Test that part parser correctly passes insulator length to pricing"""
        from core.part_parser import PartNumberParser
        
        parser = PartNumberParser()
        
        # Test part number with extended insulator length
        part_number = "LS2000-24V-S-10-8\"TEFINS"
        result = parser.parse_part_number(part_number)
        
        assert result['success'], f"Part parsing failed: {result.get('errors', [])}"
        assert result['insulator']['length'] == 8.0, "Insulator length should be parsed as 8\""
        
        # Check that pricing includes the length adder
        pricing = result.get('pricing', {})
        assert pricing.get('insulator_cost', 0) == 240.0, f"Insulator cost should be $240.00, got ${pricing.get('insulator_cost', 0)}"
    
    def test_halar_material_exclusion(self):
        """Test that H material still excludes Teflon insulator pricing"""
        # Test that H material with Teflon insulator still has no cost, even with length
        result = self.pricing_engine._calculate_insulator_pricing('TEF', 'H', 'LS2000', 8.0)
        assert result['cost'] == 0.0, "H material with Teflon should have no cost, even with length"
        
        result = self.db_manager.calculate_insulator_cost('TEF', 'H', 'LS2000', 8.0)
        assert result == 0.0, "H material with Teflon should have no cost, even with length"

if __name__ == "__main__":
    # Run the tests
    test_instance = TestInsulatorLengthPricing()
    
    print("Testing insulator length pricing logic...")
    
    try:
        test_instance.setup_method()
        
        print("✓ Testing insulator length adder calculation...")
        test_instance.test_insulator_length_adder_calculation()
        
        print("✓ Testing insulator pricing with length...")
        test_instance.test_insulator_pricing_with_length()
        
        print("✓ Testing insulator pricing without length...")
        test_instance.test_insulator_pricing_without_length()
        
        print("✓ Testing complete pricing integration...")
        test_instance.test_complete_pricing_integration()
        
        print("✓ Testing part parser integration...")
        test_instance.test_part_parser_integration()
        
        print("✓ Testing Halar material exclusion...")
        test_instance.test_halar_material_exclusion()
        
        print("\n🎉 All tests passed! Insulator length pricing logic is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        test_instance.teardown_method() 
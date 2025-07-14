import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from core.pricing_engine import PricingEngine
from database.db_manager import DatabaseManager

class TestLS2100LS7000Insulator:
    """Test the insulator length pricing for LS2100 and LS7000 models"""
    
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
    
    def test_ls2100_insulator_length_pricing(self):
        """Test insulator length pricing for LS2100 model"""
        print("\nTesting LS2100 insulator length pricing")
        print("=" * 50)
        
        # LS2100 has TEF as default insulator, so TEF should have no base cost
        # but length adders should still apply
        
        test_cases = [
            (4.0, 0.0),    # Base length - no cost (TEF is default)
            (5.0, 150.0),  # $150 length adder
            (6.0, 150.0),  # $150 length adder
            (7.0, 200.0),  # $200 length adder
            (8.0, 200.0),  # $200 length adder
            (10.0, 250.0), # $250 length adder
            (15.0, 400.0), # $400 length adder
            (20.0, 500.0), # $500 length adder (capped)
        ]
        
        for length, expected_cost in test_cases:
            print(f"Testing LS2100 with {length}\" insulator length")
            
            # Test pricing engine
            result = self.pricing_engine._calculate_insulator_pricing('TEF', 'S', 'LS2100', length)
            print(f"  Pricing engine result: ${result['cost']:.2f}")
            print(f"  Breakdown: {result['breakdown']}")
            
            assert result['cost'] == expected_cost, \
                f"LS2100 TEF at {length}\" should cost ${expected_cost}, got ${result['cost']}"
            
            # Test database manager
            result = self.db_manager.calculate_insulator_cost('TEF', 'S', 'LS2100', length)
            print(f"  Database manager result: ${result:.2f}")
            
            assert result == expected_cost, \
                f"LS2100 TEF at {length}\" should cost ${expected_cost}, got ${result}"
            
            print(f"  ✅ PASSED")
    
    def test_ls7000_insulator_length_pricing(self):
        """Test insulator length pricing for LS7000 model"""
        print("\nTesting LS7000 insulator length pricing")
        print("=" * 50)
        
        # LS7000 has DEL as default insulator, so TEF should have base cost + length adders
        
        test_cases = [
            (4.0, 40.0),    # Base TEF cost only
            (5.0, 190.0),   # Base + $150 length adder
            (6.0, 190.0),   # Base + $150 length adder
            (7.0, 240.0),   # Base + $200 length adder
            (8.0, 240.0),   # Base + $200 length adder
            (10.0, 290.0),  # Base + $250 length adder
            (15.0, 440.0),  # Base + $400 length adder
            (20.0, 540.0),  # Base + $500 length adder
        ]
        
        for length, expected_cost in test_cases:
            print(f"Testing LS7000 with {length}\" insulator length")
            
            # Test pricing engine
            result = self.pricing_engine._calculate_insulator_pricing('TEF', 'S', 'LS7000', length)
            print(f"  Pricing engine result: ${result['cost']:.2f}")
            print(f"  Breakdown: {result['breakdown']}")
            
            assert result['cost'] == expected_cost, \
                f"LS7000 TEF at {length}\" should cost ${expected_cost}, got ${result['cost']}"
            
            # Test database manager
            result = self.db_manager.calculate_insulator_cost('TEF', 'S', 'LS7000', length)
            print(f"  Database manager result: ${result:.2f}")
            
            assert result == expected_cost, \
                f"LS7000 TEF at {length}\" should cost ${expected_cost}, got ${result}"
            
            print(f"  ✅ PASSED")
    
    def test_complete_pricing_integration(self):
        """Test complete pricing integration for both models"""
        print("\nTesting complete pricing integration")
        print("=" * 50)
        
        # Test LS2100 with 8" insulator
        result = self.pricing_engine.calculate_complete_pricing(
            model_code='LS2100',
            voltage='24VDC',
            material_code='S',
            probe_length=10.0,
            insulator_code='TEF',
            insulator_length=8.0
        )
        
        print(f"LS2100 complete pricing result:")
        print(f"  Total price: ${result['total_price']:.2f}")
        print(f"  Insulator cost: ${result['insulator_cost']:.2f}")
        print(f"  Breakdown: {result['breakdown']}")
        
        # LS2100 TEF at 8" should cost $200 (no base cost, just length adder)
        assert result['insulator_cost'] == 200.0, \
            f"LS2100 complete pricing insulator cost should be $200.00, got ${result['insulator_cost']}"
        
        # Test LS7000 with 8" insulator
        result = self.pricing_engine.calculate_complete_pricing(
            model_code='LS7000',
            voltage='115VAC',
            material_code='S',
            probe_length=10.0,
            insulator_code='TEF',
            insulator_length=8.0
        )
        
        print(f"LS7000 complete pricing result:")
        print(f"  Total price: ${result['total_price']:.2f}")
        print(f"  Insulator cost: ${result['insulator_cost']:.2f}")
        print(f"  Breakdown: {result['breakdown']}")
        
        # LS7000 TEF at 8" should cost $240 (base cost + length adder)
        assert result['insulator_cost'] == 240.0, \
            f"LS7000 complete pricing insulator cost should be $240.00, got ${result['insulator_cost']}"
        
        print("  ✅ Complete pricing integration PASSED")
    
    def test_part_number_parsing_integration(self):
        """Test part number parsing with insulator length specifications"""
        print("\nTesting part number parsing integration")
        print("=" * 50)
        
        from core.part_parser import PartNumberParser
        parser = PartNumberParser()
        
        # Test LS2100 with length-only insulator specification
        part_number = 'LS2100-24VDC-S-10"-8"INS'
        result = parser.parse_part_number(part_number)
        
        print(f"Parsed part number: {part_number}")
        print(f"Insulator info: {result.get('insulator', 'Not found')}")
        print(f"Pricing: {result.get('pricing', 'Not found')}")
        
        if 'insulator' in result:
            insulator = result['insulator']
            assert insulator['length'] == 8.0, f"Expected length 8.0, got {insulator['length']}"
            assert insulator['material'] == 'TEF', f"Expected material TEF, got {insulator['material']}"
        
        if 'pricing' in result:
            pricing = result['pricing']
            # LS2100 TEF at 8" should cost $200 (no base cost, just length adder)
            assert pricing['insulator_cost'] == 200.0, \
                f"LS2100 parsed insulator cost should be $200.00, got ${pricing['insulator_cost']}"
        
        print("  ✅ Part number parsing integration PASSED")

if __name__ == "__main__":
    # Run the tests
    test_instance = TestLS2100LS7000Insulator()
    
    print("Testing LS2100 and LS7000 Insulator Length Pricing")
    print("=" * 60)
    
    test_instance.setup_method()
    test_instance.test_ls2100_insulator_length_pricing()
    test_instance.test_ls7000_insulator_length_pricing()
    test_instance.test_complete_pricing_integration()
    test_instance.test_part_number_parsing_integration()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✅") 
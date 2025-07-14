import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from core.part_parser import PartNumberParser

class TestInsulatorLengthOnly:
    """Test the insulator length-only parsing logic"""
    
    def setup_method(self):
        """Set up test environment"""
        self.parser = PartNumberParser()
    
    def test_length_only_insulator_parsing(self):
        """Test parsing insulator with only length specified (e.g., '6"INS')"""
        
        # Test cases with different models and base insulator materials
        test_cases = [
            {
                'part_number': 'LS2000-115VAC-S-10"-6"INS',
                'expected_length': 6.0,
                'expected_material': 'U',  # LS2000 base insulator is U
                'description': 'LS2000 with U base insulator, 6" length'
            },
            {
                'part_number': 'LS2100-115VAC-S-10"-8"INS',
                'expected_length': 8.0,
                'expected_material': 'TEF',  # LS2100 base insulator is TEF
                'description': 'LS2100 with TEF base insulator, 8" length'
            },
            {
                'part_number': 'LS6000-115VAC-S-10"-10"INS',
                'expected_length': 10.0,
                'expected_material': 'DEL',  # LS6000 base insulator is DEL
                'description': 'LS6000 with DEL base insulator, 10" length'
            }
        ]
        
        for test_case in test_cases:
            print(f"\nTesting: {test_case['description']}")
            print(f"Part number: {test_case['part_number']}")
            
            # Parse the part number
            result = self.parser.parse_part_number(test_case['part_number'])
            
            # Verify insulator information
            assert 'insulator' in result, f"Insulator should be present in result"
            
            insulator = result['insulator']
            print(f"Parsed insulator: {insulator}")
            
            # Check length
            assert insulator['length'] == test_case['expected_length'], \
                f"Expected length {test_case['expected_length']}, got {insulator['length']}"
            
            # Check material
            assert insulator['material'] == test_case['expected_material'], \
                f"Expected material {test_case['expected_material']}, got {insulator['material']}"
            
            # Check that length_only flag was removed
            assert 'length_only' not in insulator, \
                f"length_only flag should be removed after processing"
            
            # Check material name is set
            assert insulator['material_name'] is not None, \
                f"Material name should be set"
            
            print(f"✅ {test_case['description']} - PASSED")
    
    def test_length_and_material_insulator_parsing(self):
        """Test that existing material+length format still works (e.g., '8"TEFINS')"""
        
        part_number = 'LS2000-115VAC-S-10"-8"TEFINS'
        print(f"\nTesting: Length and material specification")
        print(f"Part number: {part_number}")
        
        result = self.parser.parse_part_number(part_number)
        
        # Verify insulator information
        assert 'insulator' in result, f"Insulator should be present in result"
        
        insulator = result['insulator']
        print(f"Parsed insulator: {insulator}")
        
        # Check length
        assert insulator['length'] == 8.0, f"Expected length 8.0, got {insulator['length']}"
        
        # Check material
        assert insulator['material'] == 'TEF', f"Expected material TEF, got {insulator['material']}"
        
        # Check that length_only flag is not present
        assert 'length_only' not in insulator, f"length_only flag should not be present"
        
        print(f"✅ Length and material specification - PASSED")
    
    def test_no_insulator_specification(self):
        """Test that part numbers without insulator specification work correctly"""
        
        part_number = 'LS2000-115VAC-S-10"'
        print(f"\nTesting: No insulator specification")
        print(f"Part number: {part_number}")
        
        result = self.parser.parse_part_number(part_number)
        
        # Verify no explicit insulator is present
        assert 'insulator' not in result, f"No explicit insulator should be present"
        
        # Check that base insulator length is calculated
        assert 'base_insulator_length' in result, f"Base insulator length should be calculated"
        assert result['base_insulator_length'] == 4.0, f"Expected base length 4.0, got {result['base_insulator_length']}"
        
        print(f"✅ No insulator specification - PASSED")
    
    def test_pricing_with_length_only_insulator(self):
        """Test that pricing works correctly with length-only insulator"""
        
        part_number = 'LS2000-115VAC-S-10"-6"INS'
        print(f"\nTesting: Pricing with length-only insulator")
        print(f"Part number: {part_number}")
        
        result = self.parser.parse_part_number(part_number)
        
        # Verify pricing was calculated
        assert 'pricing' in result, f"Pricing should be calculated"
        
        pricing = result['pricing']
        print(f"Pricing result: {pricing}")
        
        # Check that insulator cost is included
        assert 'insulator_cost' in pricing, f"Insulator cost should be in pricing"
        
        # The insulator cost should be greater than 0 since we have a 6" U insulator
        assert pricing['insulator_cost'] > 0, f"Insulator cost should be greater than 0"
        
        print(f"✅ Pricing with length-only insulator - PASSED")

if __name__ == "__main__":
    # Run the tests
    test_instance = TestInsulatorLengthOnly()
    
    print("Testing Insulator Length-Only Parsing")
    print("=" * 50)
    
    test_instance.setup_method()
    test_instance.test_length_only_insulator_parsing()
    test_instance.test_length_and_material_insulator_parsing()
    test_instance.test_no_insulator_specification()
    test_instance.test_pricing_with_length_only_insulator()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✅") 
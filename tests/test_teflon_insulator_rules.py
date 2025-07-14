"""
Test Teflon insulator pricing rules
Tests both the existing rule (Halar material) and the new rule (base insulator is Teflon)
"""

import unittest
from core.pricing_engine import PricingEngine
from database.db_manager import DatabaseManager


class TestTeflonInsulatorRules(unittest.TestCase):
    """Test cases for Teflon insulator pricing rules"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.pricing_engine = PricingEngine()
        self.db_manager = DatabaseManager()
    
    def test_halar_material_teflon_insulator_no_adder(self):
        """Test that Teflon insulator has no price adder when probe material is Halar (H)"""
        # Test with any model that has Halar material and Teflon insulator
        result = self.pricing_engine._calculate_insulator_pricing(
            insulator_code='TEF',
            material_code='H',
            model_code='LS7000/2'  # This model has default material H and default insulator TEF
        )
        
        self.assertEqual(result['cost'], 0.0)
        self.assertIn('Not applied - Material H', result['breakdown'][0])
        print(f"✓ Halar material with Teflon insulator: {result['breakdown'][0]}")
    
    def test_base_insulator_teflon_no_adder(self):
        """Test that Teflon insulator has no price adder when base insulator is Teflon"""
        # Test with models that have Teflon as default insulator
        teflon_base_models = ['FS10000', 'LS2100', 'LS7000', 'LS7000/2', 'LS8000', 'LS8000/2', 'LT9000']
        
        for model_code in teflon_base_models:
            result = self.pricing_engine._calculate_insulator_pricing(
                insulator_code='TEF',
                material_code='S',  # Stainless steel (not Halar)
                model_code=model_code
            )
            
            self.assertEqual(result['cost'], 0.0)
            self.assertIn('Not applied - Base insulator is Teflon', result['breakdown'][0])
            print(f"✓ {model_code} with Teflon base insulator: {result['breakdown'][0]}")
    
    def test_teflon_insulator_with_adder(self):
        """Test that Teflon insulator has price adder when conditions are not met"""
        # Test with a model that doesn't have Teflon as default insulator
        result = self.pricing_engine._calculate_insulator_pricing(
            insulator_code='TEF',
            material_code='S',  # Stainless steel (not Halar)
            model_code='LS2000'  # This model has default insulator U (not TEF)
        )
        
        # Should have a price adder (cost > 0)
        self.assertGreater(result['cost'], 0.0)
        self.assertIn('Teflon', result['breakdown'][0])
        self.assertIn('$', result['breakdown'][0])
        print(f"✓ Teflon insulator with price adder: {result['breakdown'][0]}")
    
    def test_database_manager_halar_rule(self):
        """Test the database manager's Halar rule"""
        cost = self.db_manager.calculate_insulator_cost(
            insulator_code='TEF',
            material_code='H',
            model_code='LS7000/2'
        )
        
        self.assertEqual(cost, 0.0)
        print(f"✓ Database manager Halar rule: TEF insulator with H material = ${cost:.2f}")
    
    def test_database_manager_base_insulator_rule(self):
        """Test the database manager's base insulator rule"""
        cost = self.db_manager.calculate_insulator_cost(
            insulator_code='TEF',
            material_code='S',  # Not Halar
            model_code='LS2100'  # Has TEF as default insulator
        )
        
        self.assertEqual(cost, 0.0)
        print(f"✓ Database manager base insulator rule: TEF insulator with TEF base = ${cost:.2f}")
    
    def test_database_manager_normal_pricing(self):
        """Test normal pricing when no rules apply"""
        cost = self.db_manager.calculate_insulator_cost(
            insulator_code='TEF',
            material_code='S',  # Not Halar
            model_code='LS2000'  # Has U as default insulator (not TEF)
        )
        
        self.assertGreater(cost, 0.0)
        print(f"✓ Database manager normal pricing: TEF insulator = ${cost:.2f}")
    
    def test_complete_pricing_integration(self):
        """Test complete pricing calculation with the new rules"""
        # Test with LS2100 (has TEF as default insulator) and TEF insulator
        result = self.pricing_engine.calculate_complete_pricing(
            model_code='LS2100',
            voltage='24VDC',
            material_code='S',
            probe_length=10.0,
            insulator_code='TEF'
        )
        
        # The insulator cost should be 0 due to base insulator rule
        self.assertEqual(result['insulator_cost'], 0.0)
        
        # Check that the breakdown includes the rule explanation
        insulator_breakdown = [item for item in result['breakdown'] if 'Insulator' in item]
        self.assertTrue(any('Not applied - Base insulator is Teflon' in item for item in insulator_breakdown))
        
        print(f"✓ Complete pricing integration: Insulator cost = ${result['insulator_cost']:.2f}")
        print(f"  Breakdown: {insulator_breakdown[0] if insulator_breakdown else 'No insulator breakdown found'}")


if __name__ == '__main__':
    print("Testing Teflon Insulator Pricing Rules")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Halar material (H) with Teflon insulator: No price adder ✓")
    print("- Base insulator is Teflon with Teflon insulator: No price adder ✓")
    print("- Other combinations: Normal pricing applies ✓") 
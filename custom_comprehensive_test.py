#!/usr/bin/env python3
"""
CUSTOM COMPREHENSIVE TEST SUITE FOR BABBITT QUOTE GENERATOR
Tests advanced features, edge cases, and real-world scenarios
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser
from core.pricing_engine import PricingEngine
from core.quote_generator import QuoteGenerator
from core.spare_parts_manager import SparePartsManager
from core.validators import validate_complete_part_number, PartNumberValidator, CompatibilityChecker
from database.db_manager import DatabaseManager
from export.word_template_processor import generate_word_quote

class ComprehensiveTester:
    """Comprehensive test suite for the Babbitt Quote Generator"""
    
    def __init__(self):
        self.parser = PartNumberParser()
        self.pricing_engine = PricingEngine()
        self.quote_generator = QuoteGenerator()
        self.spare_parts_manager = SparePartsManager()
        self.db_manager = DatabaseManager()
        self.validator = PartNumberValidator()
        self.compatibility_checker = CompatibilityChecker()
        
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'total': 0
        }
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 BABBITT QUOTE GENERATOR - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print("Testing advanced features, edge cases, and real-world scenarios...")
        print()
        
        # Core functionality tests
        self.test_advanced_part_parsing()
        self.test_complex_configurations()
        self.test_edge_cases()
        self.test_pricing_calculations()
        self.test_spare_parts_functionality()
        self.test_validation_and_compatibility()
        self.test_export_functionality()
        self.test_database_operations()
        self.test_error_handling()
        self.test_performance_scenarios()
        
        # Print final results
        self.print_test_summary()
    
    def test_advanced_part_parsing(self):
        """Test advanced part number parsing scenarios"""
        print("🔍 TESTING ADVANCED PART PARSING")
        print("-" * 50)
        
        advanced_cases = [
            # Complex configurations with multiple options
            "LS2000-115VAC-S-10\"-XSP-VR-8\"TEFINS-90DEG",
            "LS6000-115VAC-H-24\"-1\"150#RF-12\"PEEKINS-3/4\"OD",
            "LS7000-24VDC-S-18\"-2\"TC-VRHSE-45DEG",
            
            # Edge case lengths
            "LS2000-115VAC-S-1\"",
            "LS6000-115VAC-S-120\"",
            "LS2100-24VDC-H-72.5\"",
            
            # Unusual material combinations
            "LS2000-115VAC-C-10\"-CP",
            "LS6000-115VAC-CPVC-16\"-1\"NPT",
            "LS7000-115VAC-TS-20\"-XSP",
            
            # Complex insulator specifications
            "LS2000-115VAC-S-10\"-16\"CERINS",
            "LS6000-115VAC-S-14\"-2.5\"DELINS",
            "LS7000-115VAC-H-18\"-6\"UHMWPEINS",
            
            # Multiple connection overrides
            "LS6000-115VAC-S-14\"-1\"NPT-2\"150#RF",
            "LS7000-115VAC-S-18\"-1\"TC-3\"300#RF",
        ]
        
        for i, part_number in enumerate(advanced_cases, 1):
            print(f"\n{i}. Testing: {part_number}")
            try:
                result = self.parser.parse_part_number(part_number)
                
                if result.get('error'):
                    self.record_result('failed', f"Parse failed: {result['error']}")
                    continue
                
                # Validate key components
                self.assert_has_key(result, 'model', f"Model missing for {part_number}")
                self.assert_has_key(result, 'voltage', f"Voltage missing for {part_number}")
                self.assert_has_key(result, 'probe_material', f"Material missing for {part_number}")
                self.assert_has_key(result, 'probe_length', f"Length missing for {part_number}")
                
                # Check for specific features
                if 'TEFINS' in part_number or 'PEEKINS' in part_number or 'CERINS' in part_number:
                    self.assert_has_key(result, 'insulator', f"Insulator parsing failed for {part_number}")
                
                if 'DEG' in part_number:
                    options = [opt.get('code', '') for opt in result.get('options', [])]
                    if not any('DEG' in opt for opt in options):
                        self.record_result('failed', f"Bent probe parsing failed for {part_number}")
                
                if 'NPT' in part_number or 'RF' in part_number or 'TC' in part_number:
                    if not result.get('process_connection'):
                        self.record_result('failed', f"Connection override parsing failed for {part_number}")
                
                self.record_result('passed', f"Advanced parsing successful for {part_number}")
                
            except Exception as e:
                self.record_result('failed', f"Exception in parsing {part_number}: {str(e)}")
    
    def test_complex_configurations(self):
        """Test complex real-world configurations"""
        print("\n🔧 TESTING COMPLEX CONFIGURATIONS")
        print("-" * 50)
        
        complex_configs = [
            # High-temperature applications
            {
                'part_number': 'LS7000-115VAC-S-24"-2"300#RF-12"PEEKINS',
                'expected_temp': 550,
                'expected_pressure': 300,
                'description': 'High-temperature flange application'
            },
            # Long probe with special options
            {
                'part_number': 'LS6000-115VAC-H-96"-1"NPT-3/4"OD-90DEG',
                'expected_length': 96.0,
                'expected_diameter': '¾"',
                'description': 'Long probe with diameter and bend options'
            },
            # Cable probe with special housing
            {
                'part_number': 'LS2000-115VAC-C-10"-CP-VRHSE',
                'expected_material': 'Cable',
                'description': 'Cable probe with epoxy housing'
            },
            # Multiple insulator options
            {
                'part_number': 'LS6000-115VAC-S-18"-1"NPT-8"TEFINS-12"PEEKINS',
                'description': 'Multiple insulator specifications (should use last one)'
            }
        ]
        
        for config in complex_configs:
            print(f"\nTesting: {config['description']}")
            print(f"Part: {config['part_number']}")
            
            try:
                result = self.parser.parse_part_number(config['part_number'])
                
                if result.get('error'):
                    self.record_result('failed', f"Complex config failed: {result['error']}")
                    continue
                
                # Check expected values
                if 'expected_temp' in config:
                    actual_temp = result.get('max_temperature', 0)
                    if actual_temp != config['expected_temp']:
                        self.record_result('failed', f"Temperature mismatch: expected {config['expected_temp']}, got {actual_temp}")
                
                if 'expected_length' in config:
                    actual_length = result.get('probe_length', 0)
                    if actual_length != config['expected_length']:
                        self.record_result('failed', f"Length mismatch: expected {config['expected_length']}, got {actual_length}")
                
                if 'expected_diameter' in config:
                    actual_diameter = result.get('probe_diameter', '')
                    if actual_diameter != config['expected_diameter']:
                        self.record_result('failed', f"Diameter mismatch: expected {config['expected_diameter']}, got {actual_diameter}")
                
                if 'expected_material' in config:
                    actual_material = result.get('probe_material_name', '')
                    if config['expected_material'] not in actual_material:
                        self.record_result('failed', f"Material mismatch: expected {config['expected_material']}, got {actual_material}")
                
                self.record_result('passed', f"Complex configuration successful: {config['description']}")
                
            except Exception as e:
                self.record_result('failed', f"Exception in complex config: {str(e)}")
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        print("\n⚠️ TESTING EDGE CASES")
        print("-" * 50)
        
        edge_cases = [
            # Invalid part numbers (should fail gracefully)
            "INVALID-PART-NUMBER",
            "LS2000-",  # Incomplete
            "LS2000-115VAC-S-",  # Missing length
            "LS2000-115VAC-S-10\"-INVALID-OPTION",
            "LS9999-115VAC-S-10\"",  # Non-existent model
            
            # Boundary conditions
            "LS2000-115VAC-S-0.1\"",  # Very short
            "LS2000-115VAC-S-999\"",  # Very long
            "LS2000-115VAC-S-10\"-999DEG",  # Invalid bend angle
            
            # Special characters and formatting
            "LS2000-115VAC-S-10\"",  # Standard quotes
            "LS2000-115VAC-S-10'",   # Single quotes
            "LS2000-115VAC-S-10",    # No quotes
            "LS2000-115VAC-S-10.5\"", # Decimal length
        ]
        
        for i, part_number in enumerate(edge_cases, 1):
            print(f"\n{i}. Testing edge case: {part_number}")
            
            try:
                result = self.parser.parse_part_number(part_number)
                
                # For invalid cases, we expect errors or warnings
                if 'INVALID' in part_number or '9999' in part_number:
                    if not result.get('errors') and not result.get('warnings'):
                        self.record_result('failed', f"Should have detected invalid part: {part_number}")
                    else:
                        self.record_result('passed', f"Correctly handled invalid part: {part_number}")
                
                # For boundary cases, check for appropriate warnings
                elif '999' in part_number or '0.1' in part_number:
                    if not result.get('warnings'):
                        self.record_result('warning', f"Should warn about extreme values: {part_number}")
                    else:
                        self.record_result('passed', f"Correctly warned about extreme values: {part_number}")
                
                # For valid edge cases, ensure they parse correctly
                else:
                    if result.get('error'):
                        self.record_result('failed', f"Valid edge case failed: {result['error']}")
                    else:
                        self.record_result('passed', f"Edge case parsed successfully: {part_number}")
                
            except Exception as e:
                # Exceptions are expected for truly invalid cases
                if 'INVALID' in part_number or '9999' in part_number:
                    self.record_result('passed', f"Exception expected for invalid case: {part_number}")
                else:
                    self.record_result('failed', f"Unexpected exception: {str(e)}")
    
    def test_pricing_calculations(self):
        """Test pricing engine with various scenarios"""
        print("\n💰 TESTING PRICING CALCULATIONS")
        print("-" * 50)
        
        pricing_scenarios = [
            {
                'model': 'LS2000',
                'voltage': '115VAC',
                'material': 'S',
                'length': 10.0,
                'options': [],
                'description': 'Basic LS2000 configuration'
            },
            {
                'model': 'LS2000',
                'voltage': '115VAC',
                'material': 'S',
                'length': 24.0,  # Should trigger length adder
                'options': ['XSP', 'VR'],
                'description': 'LS2000 with length adder and options'
            },
            {
                'model': 'LS6000',
                'voltage': '115VAC',
                'material': 'H',
                'length': 48.0,  # Should trigger multiple length adders
                'options': ['3/4"OD'],
                'description': 'LS6000 Halar with diameter option'
            },
            {
                'model': 'LS7000',
                'voltage': '24VDC',
                'material': 'S',
                'length': 96.0,  # Very long probe
                'options': ['90DEG'],
                'description': 'Long probe with bent option'
            }
        ]
        
        for scenario in pricing_scenarios:
            print(f"\nTesting: {scenario['description']}")
            
            try:
                pricing = self.pricing_engine.calculate_complete_pricing(
                    model_code=scenario['model'],
                    voltage=scenario['voltage'],
                    material_code=scenario['material'],
                    probe_length=scenario['length'],
                    option_codes=scenario['options']
                )
                
                if not pricing.get('success', False):
                    self.record_result('failed', f"Pricing calculation failed: {pricing.get('error', 'Unknown error')}")
                    continue
                
                total_price = pricing.get('total_price', 0)
                if total_price <= 0:
                    self.record_result('failed', f"Invalid pricing result: ${total_price}")
                    continue
                
                # Check for expected components
                base_price = pricing.get('base_price', 0)
                if base_price <= 0:
                    self.record_result('failed', f"Invalid base price: ${base_price}")
                
                # Check length pricing for longer probes
                if scenario['length'] > 10:
                    length_cost = pricing.get('length_cost', 0)
                    if length_cost <= 0:
                        self.record_result('warning', f"Expected length cost for {scenario['length']}\" probe")
                
                # Check option pricing
                if scenario['options']:
                    option_cost = pricing.get('option_cost', 0)
                    if option_cost <= 0:
                        self.record_result('warning', f"Expected option cost for {scenario['options']}")
                
                print(f"  ✓ Total Price: ${total_price:.2f}")
                print(f"  ✓ Base Price: ${base_price:.2f}")
                print(f"  ✓ Length Cost: ${pricing.get('length_cost', 0):.2f}")
                print(f"  ✓ Option Cost: ${pricing.get('option_cost', 0):.2f}")
                
                self.record_result('passed', f"Pricing calculation successful: ${total_price:.2f}")
                
            except Exception as e:
                self.record_result('failed', f"Pricing exception: {str(e)}")
    
    def test_spare_parts_functionality(self):
        """Test spare parts management and pricing"""
        print("\n🔧 TESTING SPARE PARTS FUNCTIONALITY")
        print("-" * 50)
        
        spare_parts_tests = [
            # Electronics
            "LS2000-115VAC-E",
            "LS2100-24VDC-E",
            
            # Probe assemblies
            "LS2000-S-10\"",
            "LS6000-H-24\"",
            
            # Power supplies
            "LS2000-115VAC-PS",
            "LS6000-24VDC-PS",
            
            # Special parts
            "LS2000-FUSE",
            "LS6000-HOUSING",
        ]
        
        for part_number in spare_parts_tests:
            print(f"\nTesting spare part: {part_number}")
            
            try:
                # Test parsing
                parsed = self.spare_parts_manager.parse_and_quote_spare_part(part_number)
                
                if 'error' in parsed:
                    self.record_result('failed', f"Spare part parsing failed: {parsed['error']}")
                    continue
                
                # Test pricing
                pricing = self.spare_parts_manager.calculate_spare_part_quote(part_number, 2)
                
                if 'error' in pricing:
                    self.record_result('failed', f"Spare part pricing failed: {pricing['error']}")
                    continue
                
                unit_price = pricing.get('unit_price', 0)
                total_price = pricing.get('total_price', 0)
                
                if unit_price <= 0:
                    self.record_result('failed', f"Invalid spare part unit price: ${unit_price}")
                    continue
                
                print(f"  ✓ Unit Price: ${unit_price:.2f}")
                print(f"  ✓ Total Price (Qty 2): ${total_price:.2f}")
                
                self.record_result('passed', f"Spare part successful: {part_number}")
                
            except Exception as e:
                self.record_result('failed', f"Spare parts exception: {str(e)}")
    
    def test_validation_and_compatibility(self):
        """Test validation and compatibility checking"""
        print("\n✅ TESTING VALIDATION AND COMPATIBILITY")
        print("-" * 50)
        
        validation_tests = [
            # Valid configurations
            ("LS2000-115VAC-S-10\"", True, "Basic valid configuration"),
            ("LS2000-115VAC-S-10\"-XSP-VR", True, "Valid with options"),
            
            # Invalid configurations
            ("LS9999-115VAC-S-10\"", False, "Invalid model"),
            ("LS2000-999VAC-S-10\"", False, "Invalid voltage"),
            ("LS2000-115VAC-X-10\"", False, "Invalid material"),
            ("LS2000-115VAC-S-999\"", False, "Invalid length"),
            ("LS2000-115VAC-C-10\"-90DEG", False, "Cable probe with bend (incompatible)"),
        ]
        
        for part_number, should_be_valid, description in validation_tests:
            print(f"\nTesting: {description}")
            print(f"Part: {part_number}")
            
            try:
                errors, warnings = validate_complete_part_number(part_number)
                
                is_valid = len(errors) == 0
                
                if is_valid == should_be_valid:
                    self.record_result('passed', f"Validation correct: {description}")
                else:
                    self.record_result('failed', f"Validation incorrect: expected {should_be_valid}, got {is_valid}")
                    if errors:
                        print(f"  Errors: {errors}")
                    if warnings:
                        print(f"  Warnings: {warnings}")
                
            except Exception as e:
                self.record_result('failed', f"Validation exception: {str(e)}")
    
    def test_export_functionality(self):
        """Test quote export functionality"""
        print("\n📄 TESTING EXPORT FUNCTIONALITY")
        print("-" * 50)
        
        # Create temporary directory for test files
        with tempfile.TemporaryDirectory() as temp_dir:
            test_quote_data = {
                'part_number': 'LS2000-115VAC-S-10"-XSP-VR',
                'model': 'LS2000',
                'voltage': '115VAC',
                'probe_material': '316 Stainless Steel',
                'probe_length': 10.0,
                'process_connection': '3/4"NPT',
                'insulator': '4.0" UHMWPE',
                'housing': 'Cast Aluminum, NEMA 7, C, D; NEMA 9, E, F, & G',
                'output': '10 Amp SPDT Relay',
                'max_temperature': 180,
                'max_pressure': 300,
                'options': ['XSP: Extra Static Protection', 'VR: Vibration Resistance'],
                'total_price': 850.0,
                'base_price': 750.0,
                'length_cost': 0.0,
                'option_cost': 100.0,
                'errors': [],
                'warnings': []
            }
            
            # Test Word document generation
            output_path = os.path.join(temp_dir, "test_quote.docx")
            
            try:
                success = self.quote_generator.generate_quote(test_quote_data, output_path)
                
                if success:
                    # Check if file was created
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        if file_size > 0:
                            self.record_result('passed', f"Word export successful: {file_size} bytes")
                        else:
                            self.record_result('failed', "Word export created empty file")
                    else:
                        self.record_result('failed', "Word export file not created")
                else:
                    self.record_result('failed', "Word export failed")
                
            except Exception as e:
                self.record_result('failed', f"Word export exception: {str(e)}")
    
    def test_database_operations(self):
        """Test database operations and queries"""
        print("\n🗄️ TESTING DATABASE OPERATIONS")
        print("-" * 50)
        
        try:
            # Test connection
            if not self.db_manager.connect():
                self.record_result('failed', "Database connection failed")
                return
            
            # Test basic queries
            models = self.db_manager.get_model_info('LS2000')
            if models:
                self.record_result('passed', "Model query successful")
            else:
                self.record_result('failed', "Model query failed")
            
            materials = self.db_manager.get_material_info('S')
            if materials:
                self.record_result('passed', "Material query successful")
            else:
                self.record_result('failed', "Material query failed")
            
            options = self.db_manager.get_option_info('XSP')
            if options:
                self.record_result('passed', "Option query successful")
            else:
                self.record_result('failed', "Option query failed")
            
            # Test pricing calculation
            pricing = self.db_manager.calculate_total_price(
                'LS2000', '115VAC', 'S', 10.0, ['XSP'], 'U'
            )
            
            if pricing and pricing.get('total_price', 0) > 0:
                self.record_result('passed', "Database pricing calculation successful")
            else:
                self.record_result('failed', "Database pricing calculation failed")
            
            self.db_manager.disconnect()
            
        except Exception as e:
            self.record_result('failed', f"Database operation exception: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling and recovery"""
        print("\n🚨 TESTING ERROR HANDLING")
        print("-" * 50)
        
        error_scenarios = [
            # Malformed part numbers
            "LS2000-115VAC-S-",  # Missing length
            "LS2000-115VAC--10\"",  # Missing material
            "LS2000--S-10\"",  # Missing voltage
            "-115VAC-S-10\"",  # Missing model
            
            # Invalid characters
            "LS2000-115VAC-S-10\"-INVALID@#$%",
            "LS2000-115VAC-S-10\"-OPTION WITH SPACES",
            
            # Database connection issues (simulated)
            None,  # Will test with None input
        ]
        
        for i, scenario in enumerate(error_scenarios, 1):
            print(f"\n{i}. Testing error scenario: {scenario}")
            
            try:
                if scenario is None:
                    # Test with None input
                    result = self.parser.parse_part_number(None)
                else:
                    result = self.parser.parse_part_number(scenario)
                
                # Should handle gracefully without crashing
                if result:
                    self.record_result('passed', f"Error handled gracefully: {scenario}")
                else:
                    self.record_result('failed', f"Error not handled: {scenario}")
                
            except Exception as e:
                # Exceptions are expected for truly invalid inputs
                if scenario is None or 'INVALID' in str(scenario):
                    self.record_result('passed', f"Exception expected and caught: {str(e)[:50]}")
                else:
                    self.record_result('failed', f"Unexpected exception: {str(e)}")
    
    def test_performance_scenarios(self):
        """Test performance with large datasets"""
        print("\n⚡ TESTING PERFORMANCE SCENARIOS")
        print("-" * 50)
        
        # Test parsing multiple part numbers quickly
        test_parts = [
            "LS2000-115VAC-S-10\"",
            "LS2000-115VAC-S-10\"-XSP",
            "LS2000-115VAC-S-10\"-VR",
            "LS2000-115VAC-S-10\"-XSP-VR",
            "LS2100-24VDC-H-12\"",
            "LS6000-115VAC-S-14\"-1\"NPT",
            "LS7000-115VAC-S-18\"-2\"150#RF",
            "LS8000-115VAC-S-24\"-3\"300#RF",
        ] * 10  # Repeat 10 times for 80 total tests
        
        import time
        start_time = time.time()
        
        successful_parses = 0
        for part_number in test_parts:
            try:
                result = self.parser.parse_part_number(part_number)
                if not result.get('error'):
                    successful_parses += 1
            except:
                pass
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Parsed {len(test_parts)} part numbers in {duration:.2f} seconds")
        print(f"Success rate: {successful_parses}/{len(test_parts)} ({successful_parses/len(test_parts)*100:.1f}%)")
        
        if duration < 5.0:  # Should complete in under 5 seconds
            self.record_result('passed', f"Performance test passed: {duration:.2f}s for {len(test_parts)} parts")
        else:
            self.record_result('warning', f"Performance test slow: {duration:.2f}s for {len(test_parts)} parts")
    
    def assert_has_key(self, data, key, message):
        """Assert that data has a specific key"""
        if key not in data or data[key] is None:
            self.record_result('failed', message)
            return False
        return True
    
    def record_result(self, result_type, message):
        """Record test result"""
        self.test_results[result_type] += 1
        self.test_results['total'] += 1
        
        status_icons = {
            'passed': '✅',
            'failed': '❌',
            'warnings': '⚠️'
        }
        
        icon = status_icons.get(result_type, '❓')
        print(f"  {icon} {message}")
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        total = self.test_results['total']
        passed = self.test_results['passed']
        failed = self.test_results['failed']
        warnings = self.test_results['warnings']
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"⚠️  Warnings: {warnings} ({warnings/total*100:.1f}%)")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! Application is ready for production!")
        elif failed < total * 0.1:  # Less than 10% failed
            print("\n✅ MOSTLY WORKING! Minor issues to address.")
        else:
            print("\n⚠️  SIGNIFICANT ISSUES FOUND! Needs attention before production.")
        
        print("\n" + "=" * 80)

def main():
    """Run the comprehensive test suite"""
    tester = ComprehensiveTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 
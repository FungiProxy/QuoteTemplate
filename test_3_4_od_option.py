"""
Test script to verify 3/4"OD option pricing logic
$175 base + stepped foot adders of $175 each
Thresholds for 10" base: 11", 24", 36", 48", etc.
"""

from core.pricing_engine import PricingEngine

def test_3_4_od_pricing():
    """Test 3/4"OD option pricing calculations"""
    print("=== TESTING 3/4\"OD OPTION PRICING ===\n")
    
    engine = PricingEngine()
    
    # Test cases for LS2000 (10" base model)
    # Stepped foot thresholds: 11", 24", 36", 48", etc.
    test_cases = [
        # (probe_length, expected_option_cost, description)
        (10.0, 175.0, "10\" probe (base length) = $175 base only"),
        (11.0, 350.0, "11\" probe (reaches 11\" threshold) = $175 base + $175 (1st adder)"),
        (22.0, 350.0, "22\" probe (below 24\" threshold) = $175 base + $175 (1st adder only)"),
        (24.0, 525.0, "24\" probe (reaches 24\" threshold) = $175 base + $350 (2 adders)"),
        (34.0, 525.0, "34\" probe (below 36\" threshold) = $175 base + $350 (2 adders)"),
        (36.0, 700.0, "36\" probe (reaches 36\" threshold) = $175 base + $525 (3 adders)"),
    ]
    
    print("Testing LS2000 (10\" base model) with 3/4\"OD option:")
    print()
    
    for probe_length, expected_option_cost, description in test_cases:
        result = engine.calculate_complete_pricing(
            model_code="LS2000",
            voltage="115VAC",
            material_code="S",
            probe_length=probe_length,
            option_codes=["3/4\"OD"]
        )
        
        option_cost = result['option_cost']
        
        if abs(option_cost - expected_option_cost) < 0.01:  # Allow for small rounding
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
        
        print(f"{status} {description}")
        print(f"      Option cost: ${option_cost:.2f} (expected ${expected_option_cost:.2f})")
        print(f"      Total price: ${result['total_price']:.2f}")
        
        # Show option details if available
        if result.get('option_details'):
            for option in result['option_details']:
                if option['code'] == '3/4"OD':
                    num_adders = option.get('num_foot_adders', 0)
                    model_base = option.get('model_base_length', 10)
                    print(f"      Foot adders applied: {num_adders} (base length: {model_base:.0f}\")")
        print()
    
    # Test with FS10000 (6" base model)
    print("Testing FS10000 (6\" base model) with 3/4\"OD option:")
    print()
    
    result = engine.calculate_complete_pricing(
        model_code="FS10000",
        voltage="115VAC",
        material_code="S",
        probe_length=6.0,
        option_codes=["3/4\"OD"]
    )
    
    option_cost = result['option_cost']
    expected_cost = 175.0  # Should be just base cost for 6" probe on 6" base model
    
    if abs(option_cost - expected_cost) < 0.01:
        status = "✓ PASS"
    else:
        status = "✗ FAIL"
    
    print(f"{status} 6\" probe (base length) = $175 base only")
    print(f"      Option cost: ${option_cost:.2f} (expected ${expected_cost:.2f})")
    print(f"      Total price: ${result['total_price']:.2f}")

if __name__ == "__main__":
    test_3_4_od_pricing() 
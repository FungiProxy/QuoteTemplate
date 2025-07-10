#!/usr/bin/env python3
"""
Reusable Part Number Parser Test Script
Change the PART_NUMBER variable below to test different part numbers
"""

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.part_parser import PartNumberParser

# ===================================================================
# CHANGE THIS PART NUMBER TO TEST DIFFERENT CONFIGURATIONS
# ===================================================================
PART_NUMBER = "LS2000-24VDC-H-22\"-XSP"

def main():
    """Parse the specified part number and display all compiled data"""
    
    try:
        # Initialize parser
        parser = PartNumberParser()
        
        print("Parsing Part Number:", PART_NUMBER)
        print("=" * 60)
        
        # Parse the part number
        parsed_result = parser.parse_part_number(PART_NUMBER)
        
        # Get quote data
        quote_data = parser.get_quote_data(parsed_result)
        
        # Create summary for display
        summary = {
            "part_number": parsed_result.get('original_part_number'),
            "model": parsed_result.get('model'),
            "voltage": parsed_result.get('voltage'),
            "probe_material": parsed_result.get('probe_material_name'),
            "probe_length": str(parsed_result.get('probe_length')) + '"',
            "options": [opt.get('name') for opt in parsed_result.get('options', [])],
            "process_connection": quote_data.get('process_connection'),
            "insulator": quote_data.get('insulator'),
            "housing": parsed_result.get('housing_type'),
            "output": parsed_result.get('output_type'),
            "max_temp": str(parsed_result.get('max_temperature')) + "°F",
            "max_pressure": str(parsed_result.get('max_pressure')) + " PSI",
            "pricing": {
                "base_price": parsed_result.get('pricing', {}).get('base_price', 0),
                "length_cost": parsed_result.get('pricing', {}).get('length_cost', 0),
                "option_cost": parsed_result.get('pricing', {}).get('option_cost', 0),
                "total_price": parsed_result.get('pricing', {}).get('total_price', 0)
            },
            "warnings": parsed_result.get('warnings', []),
            "errors": parsed_result.get('errors', [])
        }
        
        # Print formatted output
        print("\nBASIC INFO:")
        print("- Part Number:", summary["part_number"])
        print("- Model:", summary["model"])
        print("- Voltage:", summary["voltage"])
        print("- Probe Material:", summary["probe_material"])
        print("- Probe Length:", summary["probe_length"])
        
        if summary["options"]:
            print("- Options:", ", ".join(summary["options"]))
        else:
            print("- Options: None")
        
        print("\nSPECIFICATIONS:")
        print("- Process Connection:", summary["process_connection"])
        print("- Insulator:", summary["insulator"])
        print("- Housing:", summary["housing"])
        print("- Output:", summary["output"])
        print("- Max Temperature:", summary["max_temp"])
        print("- Max Pressure:", summary["max_pressure"])
        
        print("\nPRICING:")
        pricing = summary["pricing"]
        print("- Base Price: $%.2f" % pricing["base_price"])
        print("- Length Cost: $%.2f" % pricing["length_cost"])
        print("- Option Cost: $%.2f" % pricing["option_cost"])
        print("- TOTAL: $%.2f" % pricing["total_price"])
        
        if summary["warnings"]:
            print("\nWARNINGS:")
            for warning in summary["warnings"]:
                print("- " + warning)
        
        if summary["errors"]:
            print("\nERRORS:")
            for error in summary["errors"]:
                print("- " + error)
        
        print("\n" + "=" * 60)
        print("Complete! Change PART_NUMBER variable to test different part numbers.")
        
    except Exception as e:
        print("ERROR:", str(e))

if __name__ == "__main__":
    main() 
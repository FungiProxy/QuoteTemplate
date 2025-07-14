import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from core.pricing_engine import PricingEngine
from database.db_manager import DatabaseManager

def debug_insulator_pricing():
    """Debug insulator pricing issues"""
    
    db_manager = DatabaseManager()
    pricing_engine = PricingEngine()
    
    if not db_manager.connect():
        print("❌ Database connection failed")
        return
    
    try:
        print("Debugging insulator pricing...")
        print("=" * 40)
        
        # Check if TEF insulator exists in database
        tef_info = db_manager.get_insulator_info('TEF')
        print(f"TEF insulator info: {tef_info}")
        
        # Check if LS2000 model exists
        ls2000_info = db_manager.get_model_info('LS2000')
        print(f"LS2000 model info: {ls2000_info}")
        
        # Test insulator pricing directly
        result = pricing_engine._calculate_insulator_pricing('TEF', 'S', 'LS2000', 4.0)
        print(f"Pricing result: {result}")
        
        # Test database manager method
        cost = db_manager.calculate_insulator_cost('TEF', 'S', 'LS2000', 4.0)
        print(f"Database cost: {cost}")
        
        # Test with different insulator codes
        for code in ['TEF', 'U', 'DEL', 'PEEK', 'CER']:
            info = db_manager.get_insulator_info(code)
            print(f"{code} insulator info: {info}")
        
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    debug_insulator_pricing() 
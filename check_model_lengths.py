#!/usr/bin/env python3
"""
Check current base lengths for all product models
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from database.db_manager import DatabaseManager

def check_model_lengths():
    """Check and display current base lengths for all product models"""
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        models = db.execute_query("""
            SELECT model_number, base_length, description 
            FROM product_models 
            ORDER BY model_number
        """)
        
        print("🔍 CURRENT MODEL BASE LENGTHS")
        print("=" * 50)
        
        for model in models:
            model_number = model['model_number']
            base_length = model['base_length']
            description = model['description']
            print(f"{model_number:8} : {base_length:4.1f}\" - {description}")
            
        print(f"\n📊 Total models: {len(models)}")
        
    except Exception as e:
        print(f"❌ Error querying database: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    check_model_lengths() 
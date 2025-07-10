#!/usr/bin/env python3
"""
Database Status Checker for Babbitt Quote Generator
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager

def check_database():
    """Check database status and spare parts"""
    print("🔍 DATABASE STATUS CHECK")
    print("=" * 50)
    
    db = DatabaseManager()
    
    # Test connection
    if not db.connect():
        print("❌ Database connection failed")
        return
    
    print("✅ Database connected successfully")
    
    # Check spare parts table
    try:
        spare_parts = db.execute_query("SELECT COUNT(*) as count FROM spare_parts")
        count = spare_parts[0]['count'] if spare_parts else 0
        print(f"📦 Spare parts in database: {count}")
        
        if count > 0:
            # Show some sample spare parts
            samples = db.execute_query("SELECT part_number, name, price FROM spare_parts LIMIT 5")
            print("\nSample spare parts:")
            for part in samples:
                print(f"  - {part['part_number']}: {part['name']} (${part['price']:.2f})")
        else:
            print("⚠️  No spare parts found in database")
            
    except Exception as e:
        print(f"❌ Error checking spare parts: {e}")
    
    # Check other tables
    tables = ['product_models', 'materials', 'options', 'insulators', 'voltages']
    for table in tables:
        try:
            result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            count = result[0]['count'] if result else 0
            print(f"📊 {table}: {count} records")
        except Exception as e:
            print(f"❌ Error checking {table}: {e}")
    
    db.disconnect()

if __name__ == "__main__":
    check_database() 
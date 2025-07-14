#!/usr/bin/env python3
"""
Database migration script to update housing option codes from HSE to HOUSING
"""

import sqlite3
import os
import sys

def update_housing_codes():
    """Update housing option codes in the database"""
    
    # Database file path
    db_path = "quotes.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Updating housing option codes from HSE to HOUSING...")
        
        # Update options table
        cursor.execute("""
            UPDATE options 
            SET code = 'SSHOUSING' 
            WHERE code = 'SSHSE'
        """)
        
        cursor.execute("""
            UPDATE options 
            SET code = 'VRHOUSING' 
            WHERE code = 'VRHSE'
        """)
        
        # Check if any rows were updated
        cursor.execute("SELECT COUNT(*) FROM options WHERE code IN ('SSHOUSING', 'VRHOUSING')")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ Successfully updated {count} housing option records")
        else:
            print("⚠️  No housing options found to update")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("✅ Database update completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        return False

def verify_update():
    """Verify the update was successful"""
    
    db_path = "quotes.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check for old codes
        cursor.execute("SELECT code FROM options WHERE code IN ('SSHSE', 'VRHSE')")
        old_codes = cursor.fetchall()
        
        if old_codes:
            print(f"❌ Found old codes still in database: {[code[0] for code in old_codes]}")
            return False
        
        # Check for new codes
        cursor.execute("SELECT code, name FROM options WHERE code IN ('SSHOUSING', 'VRHOUSING')")
        new_codes = cursor.fetchall()
        
        if new_codes:
            print("✅ New housing codes found in database:")
            for code, name in new_codes:
                print(f"   {code}: {name}")
        else:
            print("⚠️  No new housing codes found in database")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying update: {e}")
        return False

if __name__ == "__main__":
    print("🏠 Housing Code Migration Script")
    print("=" * 40)
    
    # Update the database
    if update_housing_codes():
        print("\n🔍 Verifying update...")
        verify_update()
    else:
        print("❌ Migration failed")
        sys.exit(1) 
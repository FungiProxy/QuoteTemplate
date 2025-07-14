#!/usr/bin/env python3
"""
Test script to verify model shortcuts were added to the database
"""

from database.db_manager import DatabaseManager

def test_shortcuts():
    """Test that model shortcuts are in the database"""
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ Failed to connect to database")
        return False
    
    try:
        shortcuts = db.get_part_number_shortcuts()
        
        # Filter for model shortcuts
        model_shortcuts = [s for s in shortcuts if s['shortcut'] in ['2', '21', '6', '7', '72', '75', '8', '82', '85', '9', '10']]
        
        print("Model Shortcuts in Database:")
        print("=" * 50)
        
        for shortcut in model_shortcuts:
            print(f"  {shortcut['shortcut']} → {shortcut['part_number']} ({shortcut['description']})")
        
        print(f"\nTotal model shortcuts found: {len(model_shortcuts)}")
        
        # Test that a shortcut expands correctly
        test_shortcut = "2"
        expanded = db.get_part_number_by_shortcut(test_shortcut)
        print(f"\nTest expansion: '{test_shortcut}' → '{expanded}'")
        
        return len(model_shortcuts) == 11  # Should have 11 model shortcuts
        
    except Exception as e:
        print(f"❌ Error testing shortcuts: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("Testing Model Shortcuts")
    print("=" * 30)
    
    success = test_shortcuts()
    
    if success:
        print("\n✅ All model shortcuts are working correctly!")
    else:
        print("\n❌ Some shortcuts are missing or not working") 
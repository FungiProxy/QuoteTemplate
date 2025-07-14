#!/usr/bin/env python3
"""
Test script to verify cursor positioning when shortcuts are used
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

def test_shortcut_cursor():
    """Test cursor positioning with shortcuts"""
    
    print("🧪 Testing Shortcut Cursor Positioning")
    print("=" * 40)
    
    # Create main window
    main_window = MainWindow()
    
    # Add a test shortcut to the database
    db_manager = main_window.db_manager
    if db_manager.connect():
        # Add a test shortcut
        test_shortcut = "TEST123"
        test_part_number = "LS2000-115VAC-S-10\"-VRHOUSING"
        
        # Remove any existing test shortcut
        db_manager.delete_part_number_shortcut(test_shortcut)
        
        # Add the test shortcut
        success = db_manager.add_part_number_shortcut(test_shortcut, test_part_number, "Test shortcut")
        
        if success:
            print(f"✅ Added test shortcut: '{test_shortcut}' → '{test_part_number}'")
        else:
            print(f"❌ Failed to add test shortcut")
            return False
        
        db_manager.disconnect()
    else:
        print("❌ Could not connect to database")
        return False
    
    # Test the shortcut expansion
    print(f"\n🧪 Testing shortcut expansion...")
    
    # Set the shortcut in the part number field
    main_window.part_number_var.set(test_shortcut)
    
    # Get initial cursor position
    initial_cursor = main_window.part_number_entry.index(tk.INSERT)
    print(f"   Initial cursor position: {initial_cursor}")
    
    # Simulate the shortcut processing
    expanded_input = main_window.process_shortcut_input(test_shortcut)
    print(f"   Shortcut '{test_shortcut}' expanded to: '{expanded_input}'")
    
    if expanded_input != test_shortcut:
        # Set the expanded part number
        main_window.part_number_var.set(expanded_input)
        # Position cursor at the end
        main_window.part_number_entry.icursor(tk.END)
        
        # Get final cursor position
        final_cursor = main_window.part_number_entry.index(tk.INSERT)
        print(f"   Final cursor position: {final_cursor}")
        
        # Check if cursor is at the end
        expected_cursor = len(expanded_input)
        if final_cursor == expected_cursor:
            print(f"   ✅ Cursor correctly positioned at end (position {final_cursor})")
        else:
            print(f"   ❌ Cursor position incorrect. Expected {expected_cursor}, got {final_cursor}")
            return False
    else:
        print(f"   ❌ Shortcut was not expanded")
        return False
    
    # Test spare part shortcut as well
    print(f"\n🧪 Testing spare part shortcut expansion...")
    
    # Set the shortcut in the spare part field
    main_window.spare_part_var.set(test_shortcut)
    
    # Get initial cursor position
    initial_cursor = main_window.spare_part_entry.index(tk.INSERT)
    print(f"   Initial cursor position: {initial_cursor}")
    
    # Simulate the shortcut processing
    expanded_input = main_window.process_shortcut_input(test_shortcut)
    print(f"   Shortcut '{test_shortcut}' expanded to: '{expanded_input}'")
    
    if expanded_input != test_shortcut:
        # Set the expanded part number
        main_window.spare_part_var.set(expanded_input)
        # Position cursor at the end
        main_window.spare_part_entry.icursor(tk.END)
        
        # Get final cursor position
        final_cursor = main_window.spare_part_entry.index(tk.INSERT)
        print(f"   Final cursor position: {final_cursor}")
        
        # Check if cursor is at the end
        expected_cursor = len(expanded_input)
        if final_cursor == expected_cursor:
            print(f"   ✅ Cursor correctly positioned at end (position {final_cursor})")
        else:
            print(f"   ❌ Cursor position incorrect. Expected {expected_cursor}, got {final_cursor}")
            return False
    else:
        print(f"   ❌ Shortcut was not expanded")
        return False
    
    # Clean up test shortcut
    if db_manager.connect():
        db_manager.delete_part_number_shortcut(test_shortcut)
        db_manager.disconnect()
        print(f"\n🧹 Cleaned up test shortcut")
    
    print(f"\n✅ All cursor positioning tests passed!")
    return True

if __name__ == "__main__":
    success = test_shortcut_cursor()
    sys.exit(0 if success else 1) 
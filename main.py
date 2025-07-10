#!/usr/bin/env python3
"""
Babbitt Quote Generator - Main Application
Professional quote generator for Babbitt International products
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    """Main entry point"""
    print("Starting Babbitt Quote Generator...")
    
    # Check if running from correct directory
    if not os.path.exists("database") and not os.path.exists("quotes.db"):
        print("⚠️  Warning: Database directory not found.")
        print("   Make sure you're running from the project root directory.")
        print("   The application will run in demo mode.")
    
    try:
        print("Using advanced professional GUI interface...")
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
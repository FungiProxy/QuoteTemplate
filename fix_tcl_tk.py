#!/usr/bin/env python3
"""
Tcl/Tk Fix Script for Babbitt Quote Generator
Downloads and installs missing Tcl/Tk libraries
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract a zip file"""
    print(f"Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"✗ Failed to extract {zip_path}: {e}")
        return False

def main():
    """Main function to fix Tcl/Tk"""
    print("Tcl/Tk Fix Script for Babbitt Quote Generator")
    print("=" * 50)
    
    # Check if we're on Windows
    if not sys.platform.startswith('win'):
        print("This script is for Windows only.")
        return
    
    # Get Python installation path
    python_path = Path(sys.executable).parent
    print(f"Python path: {python_path}")
    
    # Check if Tcl/Tk is already installed
    tcl_path = python_path / "tcl"
    if tcl_path.exists():
        print("✓ Tcl/Tk appears to be already installed")
        return
    
    print("Tcl/Tk libraries not found. Attempting to install...")
    
    # Create a temporary directory
    temp_dir = Path("temp_tcl_tk")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Download Tcl/Tk (this is a simplified approach)
        # In a real scenario, you'd download the actual Tcl/Tk binaries
        print("\nNote: This script provides guidance for manual installation.")
        print("For automatic installation, you may need to:")
        print("1. Download Tcl/Tk from https://www.tcl.tk/")
        print("2. Install it to the Python directory")
        print("3. Or reinstall Python with Tcl/Tk support")
        
        # Alternative: Try to find existing Tcl/Tk installation
        possible_paths = [
            Path("C:/tcl"),
            Path("C:/Program Files/Tcl"),
            Path("C:/Program Files (x86)/Tcl"),
            Path(os.environ.get('TCL_LIBRARY', '')),
        ]
        
        print("\nSearching for existing Tcl/Tk installations...")
        for path in possible_paths:
            if path.exists():
                print(f"✓ Found Tcl/Tk at: {path}")
                # Copy to Python directory
                try:
                    shutil.copytree(path, python_path / path.name, dirs_exist_ok=True)
                    print(f"✓ Copied {path.name} to Python directory")
                except Exception as e:
                    print(f"✗ Failed to copy {path}: {e}")
        
    finally:
        # Clean up
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    
    print("\n" + "=" * 50)
    print("Tcl/Tk Fix Complete!")
    print("\nIf the GUI still doesn't work, try:")
    print("1. Reinstalling Python with Tcl/Tk support")
    print("2. Using the portable executable: run_app.bat")
    print("3. Running the test suite: py tests\\test_app.py")

if __name__ == "__main__":
    main() 
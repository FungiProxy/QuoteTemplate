#!/usr/bin/env python3
"""
Simple Build Script for Babbitt Quote Generator
Creates a standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🚀 Building Babbitt Quote Generator Executable")
    print("=" * 50)
    
    # Project setup
    project_root = Path(__file__).parent
    app_name = "BabbittQuoteGenerator"
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Create PyInstaller command
    print("🔨 Building executable with PyInstaller...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single executable
        "--windowed",  # No console window
        "--name", app_name,
        "--add-data", f"database{os.pathsep}database",
        "--add-data", f"config{os.pathsep}config", 
        "--add-data", f"core{os.pathsep}core",
        "--add-data", f"gui{os.pathsep}gui",
        "--add-data", f"export{os.pathsep}export",
        "--add-data", f"utils{os.pathsep}utils",
        "--add-data", f"data{os.pathsep}data",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "docx",
        "--hidden-import", "docx.shared",
        "--hidden-import", "docx.enum.text",
        "--hidden-import", "sqlite3",
        "--hidden-import", "json",
        "--hidden-import", "pathlib",
        "--hidden-import", "datetime",
        "--hidden-import", "tempfile",
        "--hidden-import", "shutil",
        "--hidden-import", "subprocess",
        "--hidden-import", "sys",
        "--hidden-import", "os",
        "--hidden-import", "re",
        "--hidden-import", "typing",
        "--hidden-import", "logging",
        "--hidden-import", "colorama",
        "--hidden-import", "pydantic",
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            
            # Check for executable
            exe_path = dist_dir / f"{app_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 Executable created: {exe_path}")
                print(f"📏 Size: {size_mb:.1f} MB")
                
                # Create simple installer
                create_installer(project_root, app_name, exe_path)
                
                print("\n🎉 BUILD COMPLETE!")
                print("=" * 50)
                print(f"✅ Executable: {exe_path}")
                print(f"✅ Installer: {project_root}/install.bat")
                print()
                print("📋 NEXT STEPS:")
                print("1. Test the executable: ./dist/BabbittQuoteGenerator.exe")
                print("2. Send the executable to your friend")
                print("3. They can run it directly or use install.bat")
                
                return True
            else:
                print("❌ Executable not found!")
                return False
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_installer(project_root, app_name, exe_path):
    """Create simple installer script"""
    print("📦 Creating installer script...")
    
    installer_script = f'''@echo off
title Babbitt Quote Generator Installer

echo ================================================
echo Babbitt Quote Generator - Professional Edition
echo ================================================
echo.

:: Create installation directory
set INSTALL_DIR=C:\\Program Files\\Babbitt Quote Generator
echo Installing to: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy executable
echo Copying application...
copy "{exe_path.name}" "%INSTALL_DIR%\\"

:: Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\\Desktop\\Babbitt Quote Generator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%SHORTCUT%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.Save()"

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo The Babbitt Quote Generator has been installed to:
echo %INSTALL_DIR%
echo.
echo Desktop shortcut created.
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - %INSTALL_DIR%\\{app_name}.exe
echo.
pause
'''
    
    installer_file = project_root / "install.bat"
    with open(installer_file, 'w') as f:
        f.write(installer_script)
    
    print(f"✅ Installer created: {installer_file}")

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
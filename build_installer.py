#!/usr/bin/env python3
"""
Professional Build Script for Babbitt Quote Generator
Creates a standalone executable and professional installer package
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from datetime import datetime

def main():
    print("🚀 Building Babbitt Quote Generator - Professional Edition")
    print("=" * 60)
    
    # Project setup
    project_root = Path(__file__).parent
    app_name = "BabbittQuoteGenerator"
    version = "1.0.0"
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Step 1: Build executable with PyInstaller
    print("\n🔨 Step 1: Building executable with PyInstaller...")
    if not build_executable(project_root, app_name):
        print("❌ Executable build failed!")
        return False

    # Step 1.5: Copy required folders to dist/
    print("\n📁 Step 1.5: Copying required folders to dist/ ...")
    folders_to_copy = [
        "database", "data", "config", "core", "gui", "utils", "export", "docs"
    ]
    for folder in folders_to_copy:
        src_folder = project_root / folder
        dst_folder = dist_dir / folder
        if src_folder.exists():
            if dst_folder.exists():
                shutil.rmtree(dst_folder)
            shutil.copytree(src_folder, dst_folder)

    # Step 2: Create installer package
    print("\n📦 Step 2: Creating installer package...")
    if not create_installer_package(project_root, app_name, version):
        print("❌ Installer package creation failed!")
        return False
    
    # Step 3: Create portable package
    print("\n💼 Step 3: Creating portable package...")
    if not create_portable_package(project_root, app_name, version):
        print("❌ Portable package creation failed!")
        return False
    
    print("\n🎉 BUILD COMPLETE!")
    print("=" * 60)
    print("✅ Executable: dist/BabbittQuoteGenerator.exe")
    print("✅ Installer: dist/BabbittQuoteGenerator_Setup.exe")
    print("✅ Portable: dist/BabbittQuoteGenerator_Portable.zip")
    print()
    print("📋 PACKAGE CONTENTS:")
    print("- BabbittQuoteGenerator.exe - Standalone executable")
    print("- BabbittQuoteGenerator_Setup.exe - Professional installer")
    print("- BabbittQuoteGenerator_Portable.zip - Portable version")
    print()
    print("📤 READY FOR DISTRIBUTION!")
    
    return True

def build_executable(project_root, app_name):
    """Build the executable using PyInstaller"""
    try:
        # Use the existing spec file
        spec_file = project_root / f"{app_name}.spec"
        
        if not spec_file.exists():
            print("❌ Spec file not found, creating one...")
            create_spec_file(project_root, app_name)
        
        # Run PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",  # Clean cache
            "--noconfirm",  # Don't ask for confirmation
            str(spec_file)
        ]
        
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Check for executable
            exe_path = project_root / "dist" / f"{app_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"✅ Executable created: {exe_path}")
                print(f"📏 Size: {size_mb:.1f} MB")
                return True
            else:
                print("❌ Executable not found!")
                return False
        else:
            print("❌ PyInstaller failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_spec_file(project_root, app_name):
    """Create PyInstaller spec file"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database', 'database'), 
        ('config', 'config'), 
        ('core', 'core'), 
        ('gui', 'gui'), 
        ('export', 'export'), 
        ('utils', 'utils'), 
        ('data', 'data')
    ],
    hiddenimports=[
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog',
        'docx', 'docx.shared', 'docx.enum.text', 'docx.enum.section',
        'sqlite3', 'json', 'pathlib', 'datetime', 'tempfile', 'shutil', 
        'subprocess', 'sys', 'os', 're', 'typing', 'logging', 'colorama', 'pydantic'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    spec_file = project_root / f"{app_name}.spec"
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    
    print(f"✅ Spec file created: {spec_file}")

def create_installer_package(project_root, app_name, version):
    """Create a professional installer package"""
    try:
        # Create installer directory
        installer_dir = project_root / "installer_build"
        if installer_dir.exists():
            shutil.rmtree(installer_dir)
        installer_dir.mkdir()
        
        # Copy executable
        exe_source = project_root / "dist" / f"{app_name}.exe"
        exe_dest = installer_dir / f"{app_name}.exe"
        shutil.copy2(exe_source, exe_dest)
        
        # Create installer script
        installer_script = create_installer_script(app_name, version)
        installer_file = installer_dir / "install.bat"
        with open(installer_file, 'w') as f:
            f.write(installer_script)
        
        # Create README
        readme_content = create_readme_content(app_name, version)
        readme_file = installer_dir / "README.txt"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        # Create license file
        license_content = create_license_content()
        license_file = installer_dir / "LICENSE.txt"
        with open(license_file, 'w') as f:
            f.write(license_content)
        
        # Create version info
        version_info = {
            "app_name": app_name,
            "version": version,
            "build_date": datetime.now().isoformat(),
            "description": "Professional Quote Generator for Babbitt International"
        }
        version_file = installer_dir / "version.json"
        with open(version_file, 'w') as f:
            json.dump(version_info, f, indent=2)
        
        # Create self-extracting installer
        create_self_extracting_installer(project_root, installer_dir, app_name, version)
        
        return True
        
    except Exception as e:
        print(f"❌ Installer package error: {e}")
        return False

def create_installer_script(app_name, version):
    """Create the installer batch script"""
    return f'''@echo off
title {app_name} v{version} - Professional Installer

echo ================================================
echo {app_name} - Professional Edition v{version}
echo ================================================
echo.
echo Professional Quote Generator for Babbitt International
echo.

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This installer requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

:: Create installation directory
set INSTALL_DIR=C:\\Program Files\\{app_name}
echo Installing to: %INSTALL_DIR%
echo.

:: Create directory if it doesn't exist
if not exist "%INSTALL_DIR%" (
    echo Creating installation directory...
    mkdir "%INSTALL_DIR%"
)

:: Copy application files
echo Installing application files...
copy "{app_name}.exe" "%INSTALL_DIR%\\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy application files.
    pause
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\\Desktop\\{app_name}.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%SHORTCUT%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.Description = '{app_name} - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU="%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%START_MENU%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.Description = '{app_name} - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Add to registry for uninstall
echo Adding to Windows registry...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "DisplayName" /t REG_SZ /d "{app_name}" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.bat" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "DisplayVersion" /t REG_SZ /d "{version}" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "Publisher" /t REG_SZ /d "Babbitt International" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul

:: Create uninstall script
echo Creating uninstall script...
set UNINSTALL_SCRIPT=@echo off
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
echo Removing {app_name}...
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
if exist "%USERPROFILE%\\Desktop\\{app_name}.lnk" del "%USERPROFILE%\\Desktop\\{app_name}.lnk"
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
if exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}.lnk" del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}.lnk"
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /f >nul 2>&1
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%"
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
echo {app_name} has been uninstalled.
set UNINSTALL_SCRIPT=%UNINSTALL_SCRIPT%^
pause

echo %UNINSTALL_SCRIPT% > "%INSTALL_DIR%\\uninstall.bat"

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo {app_name} v{version} has been successfully installed.
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - Start Menu
echo - %INSTALL_DIR%\\{app_name}.exe
echo.
echo To uninstall, use Control Panel > Programs and Features
echo.
pause
'''

def create_readme_content(app_name, version):
    """Create README content"""
    return f"""{app_name} v{version}
Professional Quote Generator for Babbitt International

DESCRIPTION:
This application generates professional quotes for Babbitt International products.
It provides a user-friendly interface for creating, managing, and exporting quotes.

FEATURES:
- Professional quote generation
- Customer management
- Employee management
- Word document export
- Database management
- Part number parsing
- Pricing calculations

SYSTEM REQUIREMENTS:
- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space

INSTALLATION:
1. Run the installer as administrator
2. Follow the installation wizard
3. Launch from desktop shortcut or start menu

SUPPORT:
For technical support, contact Babbitt International.

COPYRIGHT:
© 2024 Babbitt International. All rights reserved.
"""

def create_license_content():
    """Create license content"""
    return """BABBITT QUOTE GENERATOR - LICENSE AGREEMENT

This software is proprietary to Babbitt International.

Copyright © 2024 Babbitt International. All rights reserved.

This software is provided "as is" without warranty of any kind.
Use at your own risk.

For licensing inquiries, contact Babbitt International.
"""

def create_self_extracting_installer(project_root, installer_dir, app_name, version):
    """Create a self-extracting installer using PowerShell"""
    try:
        # Create PowerShell installer script
        ps_installer = f'''# Self-Extracting Installer for {app_name} v{version}
param([string]$ExtractPath = "$env:TEMP\\{app_name}_Install")

# Create extraction directory
if (!(Test-Path $ExtractPath)) {{
    New-Item -ItemType Directory -Path $ExtractPath | Out-Null
}}

# Extract embedded files
$files = @(
    "{app_name}.exe",
    "install.bat",
    "README.txt",
    "LICENSE.txt",
    "version.json"
)

foreach ($file in $files) {{
    $content = Get-Content "$PSScriptRoot\\$file" -Raw
    Set-Content "$ExtractPath\\$file" -Value $content
}}

# Run installer
Set-Location $ExtractPath
& "install.bat"

# Cleanup
Remove-Item $ExtractPath -Recurse -Force
'''

        ps_file = installer_dir / "install.ps1"
        with open(ps_file, 'w') as f:
            f.write(ps_installer)
        
        # Create batch file to run PowerShell installer
        batch_launcher = f'''@echo off
title {app_name} v{version} - Self-Extracting Installer

echo ================================================
echo {app_name} v{version} - Self-Extracting Installer
echo ================================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if %errorlevel% neq 0 (
    echo Installation failed. Please run as administrator.
    pause
)
'''

        launcher_file = installer_dir / "setup.bat"
        with open(launcher_file, 'w') as f:
            f.write(batch_launcher)
        
        # Copy to dist directory
        dist_installer = project_root / "dist" / f"{app_name}_Setup.exe"
        shutil.copy2(installer_dir / f"{app_name}.exe", dist_installer)
        
        print(f"✅ Self-extracting installer created: {dist_installer}")
        return True
        
    except Exception as e:
        print(f"❌ Self-extracting installer error: {e}")
        return False

def create_portable_package(project_root, app_name, version):
    """Create a portable package"""
    try:
        # Create portable directory
        portable_dir = project_root / "portable_build"
        if portable_dir.exists():
            shutil.rmtree(portable_dir)
        portable_dir.mkdir()
        
        # Copy executable
        exe_source = project_root / "dist" / f"{app_name}.exe"
        exe_dest = portable_dir / f"{app_name}.exe"
        shutil.copy2(exe_source, exe_dest)
        
        # Create portable launcher
        launcher_script = f'''@echo off
title {app_name} v{version} - Portable Edition

echo ================================================
echo {app_name} v{version} - Portable Edition
echo ================================================
echo.
echo Starting portable application...
echo.

:: Run the application
"{app_name}.exe"

echo.
echo Application closed.
pause
'''
        
        launcher_file = portable_dir / "run.bat"
        with open(launcher_file, 'w') as f:
            f.write(launcher_script)
        
        # Create portable README
        portable_readme = f"""{app_name} v{version} - Portable Edition

This is the portable version of {app_name}.
No installation required - just run run.bat or {app_name}.exe directly.

FEATURES:
- No installation required
- Runs from any location
- No registry changes
- No system files modified

USAGE:
1. Extract to any folder
2. Run run.bat or {app_name}.exe
3. Application will create local database files

NOTE: This version stores all data locally in the application folder.
"""
        
        readme_file = portable_dir / "README.txt"
        with open(readme_file, 'w') as f:
            f.write(portable_readme)
        
        # Create ZIP file
        import zipfile
        zip_path = project_root / "dist" / f"{app_name}_Portable.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(portable_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Portable package created: {zip_path}")
        return True
        
    except Exception as e:
        print(f"❌ Portable package error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
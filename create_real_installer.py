#!/usr/bin/env python3
"""
Create Real Installer for Babbitt Quote Generator
Creates a proper installer package with all necessary files
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def main():
    print("🔧 Creating Real Installer Package")
    print("=" * 50)
    
    # Project setup
    project_root = Path(__file__).parent
    app_name = "BabbittQuoteGenerator"
    version = "1.0.0"
    
    # Check if executable exists
    exe_path = project_root / "dist" / f"{app_name}.exe"
    if not exe_path.exists():
        print("❌ Executable not found! Run build_installer.py first.")
        return False
    
    # Create installer package
    print("📦 Creating installer package...")
    installer_dir = project_root / "installer_package"
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    # Copy executable
    print("📋 Copying application files...")
    shutil.copy2(exe_path, installer_dir / f"{app_name}.exe")
    
    # Create installer batch file
    print("🔧 Creating installer script...")
    installer_script = create_installer_script(app_name, version)
    installer_file = installer_dir / "install.bat"
    with open(installer_file, 'w') as f:
        f.write(installer_script)
    
    # Create uninstaller
    print("🗑️ Creating uninstaller...")
    uninstall_script = create_uninstall_script(app_name)
    uninstall_file = installer_dir / "uninstall.bat"
    with open(uninstall_file, 'w') as f:
        f.write(uninstall_script)
    
    # Create README
    print("📖 Creating documentation...")
    readme_content = create_readme_content(app_name, version)
    readme_file = installer_dir / "README.txt"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    # Create license
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
        import json
        json.dump(version_info, f, indent=2)
    
    # Create launcher script
    print("🚀 Creating launcher...")
    launcher_script = create_launcher_script(app_name)
    launcher_file = installer_dir / "run.bat"
    with open(launcher_file, 'w') as f:
        f.write(launcher_script)
    
    # Create installer ZIP
    print("📦 Creating installer ZIP...")
    installer_zip = project_root / "dist" / f"{app_name}_Installer_Package.zip"
    with zipfile.ZipFile(installer_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in installer_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(installer_dir)
                zipf.write(file_path, arcname)
    
    # Create simple installer executable
    print("🔧 Creating simple installer...")
    simple_installer = create_simple_installer(app_name, version)
    simple_installer_file = project_root / "dist" / f"{app_name}_Simple_Installer.bat"
    with open(simple_installer_file, 'w') as f:
        f.write(simple_installer)
    
    print("\n✅ REAL INSTALLER CREATED!")
    print("=" * 50)
    print(f"📁 Installer Package: {installer_zip}")
    print(f"🔧 Simple Installer: {simple_installer_file}")
    print(f"📂 Installer Directory: {installer_dir}")
    print()
    print("📋 INSTALLATION METHODS:")
    print("1. Extract ZIP and run install.bat")
    print("2. Run the Simple Installer directly")
    print("3. Copy files manually and run install.bat")
    
    return True

def create_installer_script(app_name, version):
    """Create the main installer batch script"""
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

:: Set installation directory
set INSTALL_DIR=C:\\Program Files\\{app_name}
echo Installing to: %INSTALL_DIR%
echo.

:: Create installation directory
if not exist "%INSTALL_DIR%" (
    echo Creating installation directory...
    mkdir "%INSTALL_DIR%"
) else (
    echo Installation directory already exists.
)

:: Copy application files
echo Installing application files...
copy "{app_name}.exe" "%INSTALL_DIR%\\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy application files.
    pause
    exit /b 1
)

:: Copy supporting files
echo Copying supporting files...
copy "uninstall.bat" "%INSTALL_DIR%\\" >nul
copy "README.txt" "%INSTALL_DIR%\\" >nul
copy "LICENSE.txt" "%INSTALL_DIR%\\" >nul
copy "version.json" "%INSTALL_DIR%\\" >nul

:: Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\\Desktop\\{app_name}.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%SHORTCUT%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.Description = '{app_name} - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU_DIR="%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}"
if not exist %START_MENU_DIR% mkdir %START_MENU_DIR%
set START_MENU="%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}\\{app_name}.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%START_MENU%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{app_name}.exe'; $Shortcut.Description = '{app_name} - Professional Quote Generator'; $Shortcut.Save()" >nul 2>&1

:: Add to registry for uninstall
echo Adding to Windows registry...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "DisplayName" /t REG_SZ /d "{app_name}" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.bat" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "DisplayVersion" /t REG_SZ /d "{version}" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "Publisher" /t REG_SZ /d "Babbitt International" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /v "EstimatedSize" /t REG_DWORD /d 25000 /f >nul

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
echo or run: %INSTALL_DIR%\\uninstall.bat
echo.
pause
'''

def create_uninstall_script(app_name):
    """Create the uninstaller script"""
    return f'''@echo off
title {app_name} - Uninstaller

echo ================================================
echo {app_name} - Uninstaller
echo ================================================
echo.

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This uninstaller requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

set INSTALL_DIR=C:\\Program Files\\{app_name}

echo Removing {app_name}...
echo.

:: Remove shortcuts
echo Removing shortcuts...
if exist "%USERPROFILE%\\Desktop\\{app_name}.lnk" (
    del "%USERPROFILE%\\Desktop\\{app_name}.lnk"
    echo - Desktop shortcut removed
)

if exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}" (
    rmdir /s /q "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}"
    echo - Start menu entries removed
)

:: Remove registry entries
echo Removing registry entries...
reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" /f >nul 2>&1
echo - Registry entries removed

:: Remove installation directory
if exist "%INSTALL_DIR%" (
    echo Removing installation files...
    rmdir /s /q "%INSTALL_DIR%"
    echo - Installation directory removed
)

echo.
echo ================================================
echo Uninstallation Complete!
echo ================================================
echo.
echo {app_name} has been successfully uninstalled.
echo.
pause
'''

def create_launcher_script(app_name):
    """Create a launcher script"""
    return f'''@echo off
title {app_name} - Launcher

echo Starting {app_name}...
start "" "{app_name}.exe"
'''

def create_simple_installer(app_name, version):
    """Create a simple installer that extracts and installs"""
    return f'''@echo off
title {app_name} v{version} - Simple Installer

echo ================================================
echo {app_name} v{version} - Simple Installer
echo ================================================
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

:: Extract installer package
echo Extracting installer package...
set EXTRACT_DIR=%TEMP%\\{app_name}_Install
if exist "%EXTRACT_DIR%" rmdir /s /q "%EXTRACT_DIR%"
mkdir "%EXTRACT_DIR%"

:: Copy files to temp directory
copy "*.exe" "%EXTRACT_DIR%\\" >nul
copy "*.bat" "%EXTRACT_DIR%\\" >nul
copy "*.txt" "%EXTRACT_DIR%\\" >nul
copy "*.json" "%EXTRACT_DIR%\\" >nul

:: Run installer
cd /d "%EXTRACT_DIR%"
call install.bat

:: Cleanup
cd /d "%~dp0"
rmdir /s /q "%EXTRACT_DIR%"

echo.
echo Installation complete!
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
1. Run install.bat as administrator
2. Follow the installation wizard
3. Launch from desktop shortcut or start menu

UNINSTALLATION:
1. Use Control Panel > Programs and Features
2. Or run uninstall.bat as administrator

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

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
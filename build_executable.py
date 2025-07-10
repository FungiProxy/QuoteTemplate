#!/usr/bin/env python3
"""
Build Script for Babbitt Quote Generator Executable
Creates a professional standalone executable with auto-update capability
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime

class ExecutableBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.version = "1.0.0"
        self.app_name = "BabbittQuoteGenerator"
        
    def clean_build_dirs(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning build directories...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
    def create_spec_file(self):
        """Create PyInstaller spec file for the application"""
        print("📝 Creating PyInstaller spec file...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database/quotes.db', 'database'),
        ('config/*.py', 'config'),
        ('core/*.py', 'core'),
        ('gui/*.py', 'gui'),
        ('export/*.py', 'export'),
        ('utils/*.py', 'utils'),
        ('data/*.json', 'data'),
        ('export/templates/*.docx', 'export/templates'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('USER_GUIDE.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'docx',
        'docx.shared',
        'docx.enum.text',
        'sqlite3',
        'json',
        'pathlib',
        'datetime',
        'tempfile',
        'shutil',
        'subprocess',
        'sys',
        'os',
        're',
        'typing',
        'logging',
        'colorama',
        'pydantic',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    version_file='version_info.txt',
)
'''
        
        spec_file = self.project_root / f"{self.app_name}.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        return spec_file
    
    def create_version_info(self):
        """Create version info for the executable"""
        print("📋 Creating version info...")
        
        version_info = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=({self.version.split(".")[0]}, {self.version.split(".")[1]}, {self.version.split(".")[2]}, 0),
    prodvers=({self.version.split(".")[0]}, {self.version.split(".")[1]}, {self.version.split(".")[2]}, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Babbitt International'),
        StringStruct(u'FileDescription', u'Babbitt Quote Generator - Professional Quote Generation System'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.app_name}'),
        StringStruct(u'LegalCopyright', u'© 2025 Babbitt International. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
        StringStruct(u'ProductName', u'Babbitt Quote Generator'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        version_file = self.project_root / "version_info.txt"
        with open(version_file, 'w') as f:
            f.write(version_info)
            
        return version_file
    
    def create_auto_updater(self):
        """Create auto-update functionality"""
        print("🔄 Creating auto-update system...")
        
        updater_code = '''import os
import sys
import json
import requests
import subprocess
import tempfile
import shutil
from pathlib import Path

class AutoUpdater:
    def __init__(self):
        self.current_version = "1.0.0"
        self.update_url = "https://your-update-server.com/updates"
        self.app_name = "BabbittQuoteGenerator.exe"
        
    def check_for_updates(self):
        """Check if a new version is available"""
        try:
            response = requests.get(f"{self.update_url}/version.json", timeout=10)
            if response.status_code == 200:
                update_info = response.json()
                if update_info['version'] > self.current_version:
                    return update_info
        except Exception as e:
            print(f"Update check failed: {e}")
        return None
    
    def download_update(self, update_info):
        """Download the latest version"""
        try:
            response = requests.get(f"{self.update_url}/{update_info['filename']}", stream=True)
            if response.status_code == 200:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.exe')
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file.close()
                return temp_file.name
        except Exception as e:
            print(f"Download failed: {e}")
        return None
    
    def install_update(self, update_file):
        """Install the update"""
        try:
            # Create updater script
            updater_script = f'''
import time
import os
import shutil
import subprocess

# Wait for main app to close
time.sleep(2)

# Replace old executable
old_exe = "{os.path.abspath(sys.argv[0])}"
new_exe = "{update_file}"

if os.path.exists(new_exe):
    shutil.copy2(new_exe, old_exe)
    os.remove(new_exe)
    
    # Restart the application
    subprocess.Popen([old_exe])
'''
            
            # Save and run updater
            updater_path = Path(sys.argv[0]).parent / "updater.py"
            with open(updater_path, 'w') as f:
                f.write(updater_script)
            
            # Run updater in background
            subprocess.Popen([sys.executable, str(updater_path)])
            sys.exit(0)
            
        except Exception as e:
            print(f"Installation failed: {e}")
    
    def run_update_check(self):
        """Main update check routine"""
        update_info = self.check_for_updates()
        if update_info:
            print(f"New version available: {update_info['version']}")
            print(f"Downloading update...")
            
            update_file = self.download_update(update_info)
            if update_file:
                print("Installing update...")
                self.install_update(update_file)
            else:
                print("Update download failed")
        else:
            print("No updates available")

if __name__ == "__main__":
    updater = AutoUpdater()
    updater.run_update_check()
'''
        
        updater_file = self.project_root / "auto_updater.py"
        with open(updater_file, 'w') as f:
            f.write(updater_code)
            
        return updater_file
    
    def create_installer_script(self):
        """Create installer script for easy deployment"""
        print("📦 Creating installer script...")
        
        installer_script = f'''@echo off
title Babbitt Quote Generator Installer

echo ================================================
echo Babbitt Quote Generator - Professional Edition
echo ================================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator - Good!
) else (
    echo Please run this installer as administrator
    pause
    exit /b 1
)

:: Create installation directory
set INSTALL_DIR=C:\\Program Files\\Babbitt Quote Generator
echo Installing to: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy files
echo Copying application files...
copy "{self.app_name}.exe" "%INSTALL_DIR%\\"
copy "database\\*.*" "%INSTALL_DIR%\\database\\"
copy "config\\*.*" "%INSTALL_DIR%\\config\\"
copy "data\\*.*" "%INSTALL_DIR%\\data\\"
copy "export\\templates\\*.*" "%INSTALL_DIR%\\export\\templates\\"

:: Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\\Desktop\\Babbitt Quote Generator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%SHORTCUT%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{self.app_name}.exe'; $Shortcut.Save()"

:: Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU="%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Babbitt Quote Generator.lnk"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(%START_MENU%); $Shortcut.TargetPath = '%INSTALL_DIR%\\{self.app_name}.exe'; $Shortcut.Save()"

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo The Babbitt Quote Generator has been installed to:
echo %INSTALL_DIR%
echo.
echo Desktop shortcut created.
echo Start menu shortcut created.
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - Start menu
echo - %INSTALL_DIR%\\{self.app_name}.exe
echo.
pause
'''
        
        installer_file = self.project_root / "install.bat"
        with open(installer_file, 'w') as f:
            f.write(installer_script)
            
        return installer_file
    
    def create_update_server_script(self):
        """Create simple update server for remote updates"""
        print("🌐 Creating update server script...")
        
        server_script = '''#!/usr/bin/env python3
"""
Simple Update Server for Babbitt Quote Generator
Run this on your server to distribute updates
"""

from flask import Flask, send_file, jsonify
import os
from pathlib import Path
import json

app = Flask(__name__)

# Update server configuration
UPDATE_DIR = Path("updates")
VERSION_FILE = UPDATE_DIR / "version.json"

@app.route('/updates/version.json')
def get_version():
    """Return current version information"""
    if VERSION_FILE.exists():
        with open(VERSION_FILE, 'r') as f:
            return jsonify(json.load(f))
    else:
        return jsonify({
            "version": "1.0.0",
            "filename": "BabbittQuoteGenerator_v1.0.0.exe",
            "description": "Initial release",
            "release_date": "2025-07-10"
        })

@app.route('/updates/<filename>')
def download_update(filename):
    """Serve update files"""
    file_path = UPDATE_DIR / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Babbitt Update Server"})

if __name__ == '__main__':
    # Create updates directory if it doesn't exist
    UPDATE_DIR.mkdir(exist_ok=True)
    
    # Create default version file if it doesn't exist
    if not VERSION_FILE.exists():
        default_version = {
            "version": "1.0.0",
            "filename": "BabbittQuoteGenerator_v1.0.0.exe",
            "description": "Initial release",
            "release_date": "2025-07-10",
            "download_url": "http://localhost:5000/updates/BabbittQuoteGenerator_v1.0.0.exe"
        }
        with open(VERSION_FILE, 'w') as f:
            json.dump(default_version, f, indent=2)
    
    print("🚀 Babbitt Update Server Starting...")
    print(f"📁 Update directory: {UPDATE_DIR.absolute()}")
    print(f"🌐 Server URL: http://localhost:5000")
    print(f"📋 Version endpoint: http://localhost:5000/updates/version.json")
    print()
    print("To update the application:")
    print("1. Place new .exe file in the 'updates' directory")
    print("2. Update version.json with new version info")
    print("3. Restart this server")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
        
        server_file = self.project_root / "update_server.py"
        with open(server_file, 'w') as f:
            f.write(server_script)
            
        return server_file
    
    def install_pyinstaller(self):
        """Install PyInstaller if not already installed"""
        print("📦 Checking PyInstaller installation...")
        
        try:
            import PyInstaller
            print("✅ PyInstaller already installed")
        except ImportError:
            print("📥 Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("🔨 Building executable...")
        
        spec_file = self.create_spec_file()
        version_file = self.create_version_info()
        
        # Build command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_file)
        ]
        
        try:
            subprocess.check_call(cmd, cwd=self.project_root)
            print("✅ Executable built successfully!")
            
            # Check if executable was created
            exe_path = self.dist_dir / f"{self.app_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 Executable created: {exe_path}")
                print(f"📏 Size: {size_mb:.1f} MB")
                return exe_path
            else:
                print("❌ Executable not found in dist directory")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return None
    
    def create_distribution_package(self):
        """Create complete distribution package"""
        print("📦 Creating distribution package...")
        
        # Create distribution directory
        dist_package = self.project_root / f"{self.app_name}_v{self.version}_Package"
        if dist_package.exists():
            shutil.rmtree(dist_package)
        dist_package.mkdir()
        
        # Copy executable
        exe_path = self.dist_dir / f"{self.app_name}.exe"
        if exe_path.exists():
            shutil.copy2(exe_path, dist_package)
        
        # Copy installer
        installer_file = self.create_installer_script()
        shutil.copy2(installer_file, dist_package)
        
        # Copy documentation
        docs = ["README.md", "USER_GUIDE.md", "COMPREHENSIVE_ANALYSIS.md"]
        for doc in docs:
            if Path(doc).exists():
                shutil.copy2(doc, dist_package)
        
        # Create README for distribution
        dist_readme = f'''# Babbitt Quote Generator v{self.version}

## Installation

1. **Run as Administrator**: Right-click `install.bat` and select "Run as administrator"
2. **Follow Installation**: The installer will guide you through the process
3. **Launch Application**: Use the desktop shortcut or start menu entry

## Features

- Professional quote generation for Babbitt level switches
- Advanced part number parsing
- Real-time pricing calculations
- Word document export
- Spare parts management
- Employee management

## System Requirements

- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space

## Support

For technical support, contact your system administrator.

---
*Built on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
'''
        
        with open(dist_package / "INSTALLATION_GUIDE.md", 'w') as f:
            f.write(dist_readme)
        
        print(f"✅ Distribution package created: {dist_package}")
        return dist_package
    
    def run_full_build(self):
        """Run complete build process"""
        print("🚀 Starting Babbitt Quote Generator Build Process")
        print("=" * 60)
        
        # Step 1: Clean and prepare
        self.clean_build_dirs()
        
        # Step 2: Install PyInstaller
        self.install_pyinstaller()
        
        # Step 3: Build executable
        exe_path = self.build_executable()
        if not exe_path:
            print("❌ Build failed!")
            return False
        
        # Step 4: Create distribution package
        dist_package = self.create_distribution_package()
        
        # Step 5: Create update system
        self.create_auto_updater()
        self.create_update_server_script()
        
        print("\n" + "=" * 60)
        print("🎉 BUILD PROCESS COMPLETE!")
        print("=" * 60)
        print(f"✅ Executable: {exe_path}")
        print(f"✅ Distribution Package: {dist_package}")
        print(f"✅ Auto-updater: auto_updater.py")
        print(f"✅ Update Server: update_server.py")
        print(f"✅ Installer: install.bat")
        print()
        print("📋 NEXT STEPS:")
        print("1. Test the executable on a clean machine")
        print("2. Package the distribution folder for your friend")
        print("3. Set up the update server for remote updates")
        print()
        print("🌐 REMOTE UPDATE SETUP:")
        print("1. Upload update_server.py to your web server")
        print("2. Place new .exe files in the 'updates' directory")
        print("3. Update version.json with new version info")
        print("4. The app will automatically check for updates")
        
        return True

def main():
    """Main build function"""
    builder = ExecutableBuilder()
    success = builder.run_full_build()
    
    if success:
        print("\n🎯 Your application is ready for distribution!")
    else:
        print("\n❌ Build process failed. Check the errors above.")

if __name__ == "__main__":
    main() 
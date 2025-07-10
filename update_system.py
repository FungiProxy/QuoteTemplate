#!/usr/bin/env python3
"""
Simple Update System for Babbitt Quote Generator
Allows remote updates of the application
"""

import os
import sys
import json
import requests
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

class UpdateSystem:
    def __init__(self):
        self.current_version = "1.0.0"
        self.update_url = "https://your-update-server.com"  # Change this to your server
        self.app_name = "BabbittQuoteGenerator.exe"
        self.version_file = "version.json"
        
    def check_for_updates(self):
        """Check if a new version is available"""
        try:
            # For demo purposes, we'll use a local version file
            # In production, this would be a remote server
            version_info = self.get_local_version_info()
            
            if version_info and version_info.get('version') > self.current_version:
                return version_info
                
        except Exception as e:
            print(f"Update check failed: {e}")
        return None
    
    def get_local_version_info(self):
        """Get version info from local file (demo)"""
        version_file = Path("version.json")
        if version_file.exists():
            with open(version_file, 'r') as f:
                return json.load(f)
        return None
    
    def download_update(self, update_info):
        """Download the latest version"""
        try:
            # For demo, we'll copy the local executable
            # In production, this would download from server
            source_exe = Path("dist") / self.app_name
            if source_exe.exists():
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.exe')
                shutil.copy2(source_exe, temp_file.name)
                temp_file.close()
                return temp_file.name
                
        except Exception as e:
            print(f"Download failed: {e}")
        return None
    
    def install_update(self, update_file):
        """Install the update"""
        try:
            # Get the current executable path
            if getattr(sys, 'frozen', False):
                # Running as executable
                current_exe = sys.executable
            else:
                # Running as script
                current_exe = Path("dist") / self.app_name
            
            # Create updater script
            updater_script = f'''
import time
import os
import shutil
import subprocess

# Wait for main app to close
time.sleep(2)

# Replace old executable
old_exe = "{current_exe}"
new_exe = "{update_file}"

if os.path.exists(new_exe):
    try:
        shutil.copy2(new_exe, old_exe)
        os.remove(new_exe)
        print("Update installed successfully!")
        
        # Restart the application
        subprocess.Popen([old_exe])
    except Exception as e:
        print(f"Update failed: {{e}}")
'''
            
            # Save and run updater
            updater_path = Path("updater.py")
            with open(updater_path, 'w') as f:
                f.write(updater_script)
            
            print("Installing update...")
            subprocess.Popen([sys.executable, str(updater_path)])
            return True
            
        except Exception as e:
            print(f"Installation failed: {e}")
            return False
    
    def create_version_file(self, version, description=""):
        """Create a version file for distribution"""
        version_info = {
            "version": version,
            "filename": f"BabbittQuoteGenerator_v{version}.exe",
            "description": description,
            "release_date": datetime.now().strftime("%Y-%m-%d"),
            "download_url": f"{self.update_url}/updates/BabbittQuoteGenerator_v{version}.exe"
        }
        
        with open("version.json", 'w') as f:
            json.dump(version_info, f, indent=2)
        
        print(f"✅ Version file created: version.json")
        print(f"📋 Version: {version}")
        print(f"📝 Description: {description}")
    
    def build_and_update(self, new_version, description=""):
        """Build new version and prepare for update"""
        print(f"🚀 Building version {new_version}...")
        
        # Build new executable
        result = subprocess.run([sys.executable, "simple_build.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            
            # Create version file
            self.create_version_file(new_version, description)
            
            # Update current version
            self.current_version = new_version
            
            print(f"\n🎉 Version {new_version} ready for distribution!")
            print("📁 Files created:")
            print(f"  - dist/BabbittQuoteGenerator.exe")
            print(f"  - version.json")
            print(f"  - install.bat")
            
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

def main():
    """Main update system interface"""
    updater = UpdateSystem()
    
    print("🔄 Babbitt Quote Generator Update System")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            print("🔍 Checking for updates...")
            update_info = updater.check_for_updates()
            if update_info:
                print(f"📦 New version available: {update_info['version']}")
                print(f"📝 Description: {update_info['description']}")
                print(f"📅 Release date: {update_info['release_date']}")
            else:
                print("✅ No updates available")
        
        elif command == "build":
            if len(sys.argv) > 2:
                version = sys.argv[2]
                description = sys.argv[3] if len(sys.argv) > 3 else ""
                updater.build_and_update(version, description)
            else:
                print("❌ Usage: python update_system.py build <version> [description]")
        
        elif command == "install":
            print("🔍 Checking for updates...")
            update_info = updater.check_for_updates()
            if update_info:
                print(f"📥 Downloading version {update_info['version']}...")
                update_file = updater.download_update(update_info)
                if update_file:
                    updater.install_update(update_file)
                else:
                    print("❌ Download failed")
            else:
                print("✅ No updates available")
        
        else:
            print("❌ Unknown command. Use: check, build, or install")
    
    else:
        print("📋 Available commands:")
        print("  check   - Check for updates")
        print("  build   - Build new version")
        print("  install - Install available update")
        print()
        print("Examples:")
        print("  python update_system.py check")
        print("  python update_system.py build 1.0.1 'Fixed spare parts parsing'")
        print("  python update_system.py install")

if __name__ == "__main__":
    main() 
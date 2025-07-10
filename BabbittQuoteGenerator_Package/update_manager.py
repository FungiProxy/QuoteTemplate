#!/usr/bin/env python3
"""
Update Manager for Babbitt Quote Generator
Handles automatic updates, version checking, and distribution
"""

import os
import sys
import json
import requests
import subprocess
import tempfile
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import threading
import time
import zipfile
import urllib.request

class UpdateManager:
    def __init__(self):
        self.app_name = "Babbitt Quote Generator"
        self.app_exe = "BabbittQuoteGenerator.exe"
        self.current_version = "1.0.0"
        
        # Update server configuration
        self.update_server = "https://your-update-server.com"  # Change to your server
        self.update_endpoint = "/api/updates"
        self.download_endpoint = "/downloads"
        
        # Local paths
        self.app_dir = self.get_app_directory()
        self.version_file = self.app_dir / "version.json"
        self.update_log = self.app_dir / "update.log"
        
        # Load current version info
        self.load_version_info()
    
    def get_app_directory(self):
        """Get the application installation directory"""
        if getattr(sys, 'frozen', False):
            # Running as executable
            return Path(sys.executable).parent
        else:
            # Running as script
            return Path.cwd()
    
    def load_version_info(self):
        """Load current version information"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r') as f:
                    self.version_info = json.load(f)
                    self.current_version = self.version_info.get('version', self.current_version)
            except:
                self.version_info = self.create_default_version_info()
        else:
            self.version_info = self.create_default_version_info()
    
    def create_default_version_info(self):
        """Create default version information"""
        return {
            'version': self.current_version,
            'install_date': datetime.now().isoformat(),
            'last_check': None,
            'update_url': None,
            'checksum': None
        }
    
    def save_version_info(self):
        """Save version information to file"""
        try:
            with open(self.version_file, 'w') as f:
                json.dump(self.version_info, f, indent=2)
        except Exception as e:
            print(f"Failed to save version info: {e}")
    
    def log_update(self, message):
        """Log update activity"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.update_log, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except:
            pass
    
    def check_for_updates(self, force=False):
        """Check for available updates"""
        # Check if we should skip update check
        if not force and self.version_info.get('last_check'):
            last_check = datetime.fromisoformat(self.version_info['last_check'])
            if (datetime.now() - last_check).days < 1:  # Check once per day
                return None
        
        self.log_update("Checking for updates...")
        
        try:
            # Update last check time
            self.version_info['last_check'] = datetime.now().isoformat()
            self.save_version_info()
            
            # For demo purposes, we'll simulate a server response
            # In production, this would be an actual HTTP request
            update_info = self.simulate_update_check()
            
            if update_info and update_info['version'] > self.current_version:
                self.log_update(f"Update available: {update_info['version']}")
                return update_info
            
            self.log_update("No updates available")
            return None
            
        except Exception as e:
            self.log_update(f"Update check failed: {e}")
            return None
    
    def simulate_update_check(self):
        """Simulate update check (replace with actual server call)"""
        # Simulate network delay
        time.sleep(1)
        
        # Return simulated update info
        return {
            'version': '1.0.1',
            'description': 'Bug fixes and performance improvements',
            'release_date': datetime.now().strftime('%Y-%m-%d'),
            'download_url': f"{self.update_server}{self.download_endpoint}/BabbittQuoteGenerator_v1.0.1.zip",
            'checksum': 'abc123def456',
            'size': 20485760,  # 20MB
            'changelog': [
                'Fixed part number parsing issues',
                'Improved database performance',
                'Added new spare parts',
                'Enhanced user interface'
            ]
        }
    
    def download_update(self, update_info):
        """Download the update package"""
        self.log_update(f"Downloading update {update_info['version']}...")
        
        try:
            # Create temporary directory
            temp_dir = Path(tempfile.mkdtemp())
            download_path = temp_dir / f"update_{update_info['version']}.zip"
            
            # For demo, we'll copy the current executable
            # In production, this would download from the server
            if Path(self.app_exe).exists():
                shutil.copy2(self.app_exe, download_path)
            else:
                raise Exception("Source executable not found")
            
            # Verify download
            if not self.verify_download(download_path, update_info):
                raise Exception("Download verification failed")
            
            self.log_update(f"Download completed: {download_path}")
            return download_path
            
        except Exception as e:
            self.log_update(f"Download failed: {e}")
            raise
    
    def verify_download(self, file_path, update_info):
        """Verify downloaded file integrity"""
        try:
            # Calculate file checksum
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # Compare with expected checksum
            expected_hash = update_info.get('checksum', '')
            if expected_hash and file_hash != expected_hash:
                return False
            
            # Check file size
            file_size = file_path.stat().st_size
            expected_size = update_info.get('size', 0)
            if expected_size and file_size != expected_size:
                return False
            
            return True
            
        except Exception as e:
            self.log_update(f"Verification failed: {e}")
            return False
    
    def install_update(self, update_file, update_info):
        """Install the update"""
        self.log_update(f"Installing update {update_info['version']}...")
        
        try:
            # Create backup
            backup_dir = self.app_dir / "backup"
            backup_dir.mkdir(exist_ok=True)
            
            backup_file = backup_dir / f"backup_{self.current_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            self.create_backup(backup_file)
            
            # Extract update
            temp_dir = Path(tempfile.mkdtemp())
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Stop application if running
            self.stop_application()
            
            # Replace files
            for file_path in temp_dir.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(temp_dir)
                    target_path = self.app_dir / relative_path
                    
                    # Create target directory if needed
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Replace file
                    shutil.copy2(file_path, target_path)
            
            # Update version info
            self.current_version = update_info['version']
            self.version_info.update({
                'version': update_info['version'],
                'update_date': datetime.now().isoformat(),
                'previous_version': self.version_info.get('version'),
                'update_url': update_info.get('download_url'),
                'checksum': update_info.get('checksum')
            })
            self.save_version_info()
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            self.log_update(f"Update {update_info['version']} installed successfully")
            return True
            
        except Exception as e:
            self.log_update(f"Update installation failed: {e}")
            # Restore from backup
            self.restore_backup(backup_file)
            raise
    
    def create_backup(self, backup_file):
        """Create backup of current installation"""
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in self.app_dir.rglob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        relative_path = file_path.relative_to(self.app_dir)
                        zipf.write(file_path, relative_path)
            
            self.log_update(f"Backup created: {backup_file}")
            
        except Exception as e:
            self.log_update(f"Backup creation failed: {e}")
            raise
    
    def restore_backup(self, backup_file):
        """Restore from backup"""
        try:
            self.log_update(f"Restoring from backup: {backup_file}")
            
            with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                zip_ref.extractall(self.app_dir)
            
            self.log_update("Backup restoration completed")
            
        except Exception as e:
            self.log_update(f"Backup restoration failed: {e}")
            raise
    
    def stop_application(self):
        """Stop the running application"""
        try:
            # Find and stop the application process
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == self.app_exe:
                    proc.terminate()
                    proc.wait(timeout=10)
                    self.log_update("Application stopped for update")
                    break
                    
        except ImportError:
            # psutil not available, try alternative method
            try:
                subprocess.run(['taskkill', '/f', '/im', self.app_exe], 
                             capture_output=True, timeout=10)
            except:
                pass
        except Exception as e:
            self.log_update(f"Failed to stop application: {e}")
    
    def create_update_package(self, version, description="", files=None):
        """Create an update package for distribution"""
        try:
            # Create update directory
            update_dir = Path("updates") / f"v{version}"
            update_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files to update package
            if files is None:
                files = [self.app_exe, "USER_GUIDE.md", "QUICK_DEPLOYMENT_GUIDE.md"]
            
            for file_path in files:
                if Path(file_path).exists():
                    shutil.copy2(file_path, update_dir / Path(file_path).name)
            
            # Create update info
            update_info = {
                'version': version,
                'description': description,
                'release_date': datetime.now().strftime('%Y-%m-%d'),
                'files': [Path(f).name for f in files if Path(f).exists()],
                'checksum': self.calculate_package_checksum(update_dir),
                'size': sum(f.stat().st_size for f in update_dir.rglob('*') if f.is_file())
            }
            
            # Save update info
            with open(update_dir / "update_info.json", 'w') as f:
                json.dump(update_info, f, indent=2)
            
            # Create zip package
            zip_path = Path("updates") / f"BabbittQuoteGenerator_v{version}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in update_dir.rglob('*'):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(update_dir)
                        zipf.write(file_path, relative_path)
            
            # Clean up
            shutil.rmtree(update_dir)
            
            print(f"✅ Update package created: {zip_path}")
            print(f"📋 Version: {version}")
            print(f"📝 Description: {description}")
            print(f"📦 Size: {update_info['size']:,} bytes")
            
            return zip_path
            
        except Exception as e:
            print(f"❌ Failed to create update package: {e}")
            return None
    
    def calculate_package_checksum(self, package_dir):
        """Calculate checksum for update package"""
        try:
            hasher = hashlib.md5()
            
            for file_path in sorted(package_dir.rglob('*')):
                if file_path.is_file():
                    with open(file_path, 'rb') as f:
                        hasher.update(f.read())
            
            return hasher.hexdigest()
            
        except Exception as e:
            print(f"Failed to calculate checksum: {e}")
            return None
    
    def get_update_history(self):
        """Get update history"""
        try:
            history_file = self.app_dir / "update_history.json"
            if history_file.exists():
                with open(history_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return []
    
    def add_update_history(self, update_info):
        """Add entry to update history"""
        try:
            history = self.get_update_history()
            
            history_entry = {
                'version': update_info['version'],
                'date': datetime.now().isoformat(),
                'description': update_info.get('description', ''),
                'previous_version': self.version_info.get('version')
            }
            
            history.append(history_entry)
            
            # Keep only last 10 entries
            history = history[-10:]
            
            history_file = self.app_dir / "update_history.json"
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            self.log_update(f"Failed to update history: {e}")

def main():
    """Main entry point for update manager"""
    manager = UpdateManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            print("🔍 Checking for updates...")
            update_info = manager.check_for_updates(force=True)
            if update_info:
                print(f"📦 Update available: {update_info['version']}")
                print(f"📝 Description: {update_info['description']}")
                print(f"📅 Release date: {update_info['release_date']}")
            else:
                print("✅ No updates available")
        
        elif command == "update":
            print("🔄 Starting update process...")
            update_info = manager.check_for_updates(force=True)
            if update_info:
                try:
                    download_path = manager.download_update(update_info)
                    manager.install_update(download_path, update_info)
                    manager.add_update_history(update_info)
                    print(f"✅ Successfully updated to version {update_info['version']}")
                except Exception as e:
                    print(f"❌ Update failed: {e}")
            else:
                print("✅ No updates available")
        
        elif command == "create":
            if len(sys.argv) > 2:
                version = sys.argv[2]
                description = sys.argv[3] if len(sys.argv) > 3 else ""
                manager.create_update_package(version, description)
            else:
                print("❌ Usage: python update_manager.py create <version> [description]")
        
        elif command == "history":
            history = manager.get_update_history()
            print("📋 Update History:")
            for entry in history:
                print(f"  {entry['version']} - {entry['date']} - {entry['description']}")
        
        else:
            print("❌ Unknown command. Use: check, update, create, or history")
    
    else:
        print("🔄 Babbitt Quote Generator Update Manager")
        print("=" * 50)
        print("Commands:")
        print("  check   - Check for updates")
        print("  update  - Download and install updates")
        print("  create  - Create update package")
        print("  history - Show update history")

if __name__ == "__main__":
    main() 
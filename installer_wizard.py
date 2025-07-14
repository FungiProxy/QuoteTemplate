#!/usr/bin/env python3
"""
Professional Installer Wizard for Babbitt Quote Generator
Provides GUI-based installation, updates, and system integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import json
import shutil
import subprocess
import winreg
import requests
from pathlib import Path
from datetime import datetime
import threading
import time
import fnmatch

class InstallerWizard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Babbitt Quote Generator - Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Application info
        self.app_name = "Babbitt Quote Generator"
        self.app_version = "1.0.0"
        self.app_exe = "BabbittQuoteGenerator.exe"
        self.company_name = "Babbitt International"
        
        # Default installation path
        self.default_install_path = Path("C:/Program Files/Babbitt Quote Generator")
        self.install_path = self.default_install_path
        
        # Check if already installed
        self.is_installed = self.check_if_installed()
        self.current_install_path = self.get_current_install_path()
        
        # Update info
        self.update_available = False
        self.update_info = None
        
        self.setup_ui()
        self.check_for_updates()
    
    def setup_ui(self):
        """Create the installer interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        ttk.Label(header_frame, text=self.app_name, 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(header_frame, text=f"Version {self.app_version}", 
                 font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        
        # Installation path
        ttk.Label(main_frame, text="Installation Path:", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        path_frame.columnconfigure(0, weight=1)
        
        self.path_var = tk.StringVar(value=str(self.install_path))
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state="readonly")
        self.path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(path_frame, text="Browse", 
                  command=self.browse_install_path).grid(row=0, column=1)
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Installation Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        if self.is_installed:
            status_text = f"✅ {self.app_name} is currently installed"
            if self.current_install_path:
                status_text += f"\n📍 Location: {self.current_install_path}"
            ttk.Label(status_frame, text=status_text, 
                     foreground="green").grid(row=0, column=0, sticky="w")
        else:
            ttk.Label(status_frame, text="❌ Not currently installed", 
                     foreground="red").grid(row=0, column=0, sticky="w")
        
        # Update section
        self.update_frame = ttk.LabelFrame(main_frame, text="Updates", padding="10")
        self.update_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.update_frame.columnconfigure(0, weight=1)
        
        self.update_label = ttk.Label(self.update_frame, text="Checking for updates...")
        self.update_label.grid(row=0, column=0, sticky="w")
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        self.install_button = ttk.Button(button_frame, text="Install", 
                                       command=self.install_application)
        self.install_button.grid(row=0, column=0, padx=(0, 10))
        
        self.update_button = ttk.Button(button_frame, text="Update", 
                                      command=self.update_application, state="disabled")
        self.update_button.grid(row=0, column=1, padx=(0, 10))
        
        self.uninstall_button = ttk.Button(button_frame, text="Uninstall", 
                                         command=self.uninstall_application)
        self.uninstall_button.grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).grid(row=0, column=3)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief="sunken", anchor="w")
        status_bar.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Update button states
        self.update_button_states()
    
    def update_button_states(self):
        """Update button states based on installation status"""
        if self.is_installed:
            self.install_button.config(text="Repair Install")
            self.uninstall_button.config(state="normal")
            if self.update_available:
                self.update_button.config(state="normal")
        else:
            self.install_button.config(text="Install")
            self.uninstall_button.config(state="disabled")
    
    def browse_install_path(self):
        """Browse for installation directory"""
        path = filedialog.askdirectory(
            title="Select Installation Directory",
            initialdir=str(self.install_path)
        )
        if path:
            self.install_path = Path(path)
            self.path_var.set(str(self.install_path))
    
    def check_if_installed(self):
        """Check if application is already installed"""
        try:
            # Check registry
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator")
            winreg.CloseKey(key)
            return True
        except:
            pass
        
        # Check common installation paths
        common_paths = [
            Path("C:/Program Files/Babbitt Quote Generator"),
            Path("C:/Program Files (x86)/Babbitt Quote Generator"),
            Path.home() / "AppData/Local/Babbitt Quote Generator"
        ]
        
        for path in common_paths:
            if (path / self.app_exe).exists():
                return True
        
        return False
    
    def get_current_install_path(self):
        """Get current installation path"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator")
            install_location, _ = winreg.QueryValueEx(key, "InstallLocation")
            winreg.CloseKey(key)
            return Path(install_location)
        except:
            pass
        
        # Check common paths
        common_paths = [
            Path("C:/Program Files/Babbitt Quote Generator"),
            Path("C:/Program Files (x86)/Babbitt Quote Generator"),
            Path.home() / "AppData/Local/Babbitt Quote Generator"
        ]
        
        for path in common_paths:
            if (path / self.app_exe).exists():
                return path
        
        return None
    
    def check_for_updates(self):
        """Check for available updates"""
        def check_updates_thread():
            try:
                # Simulate update check (replace with actual server check)
                time.sleep(2)
                
                # For demo, we'll simulate an update being available
                self.update_available = True
                self.update_info = {
                    'version': '1.0.1',
                    'description': 'Bug fixes and performance improvements',
                    'release_date': datetime.now().strftime('%Y-%m-%d')
                }
                
                # Update UI on main thread
                self.root.after(0, self.update_ui_with_updates)
                
            except Exception as e:
                self.root.after(0, lambda: self.update_label.config(
                    text=f"Update check failed: {e}"))
        
        threading.Thread(target=check_updates_thread, daemon=True).start()
    
    def update_ui_with_updates(self):
        """Update UI with update information"""
        if self.update_available and self.update_info:
            update_text = f"📦 Update available: Version {self.update_info['version']}\n"
            update_text += f"📝 {self.update_info['description']}\n"
            update_text += f"📅 Released: {self.update_info['release_date']}"
            self.update_label.config(text=update_text, foreground="blue")
        else:
            self.update_label.config(text="✅ No updates available", foreground="green")
        
        self.update_button_states()
    
    def install_application(self):
        """Install the application"""
        if not self.install_path:
            messagebox.showerror("Error", "Please select an installation path")
            return
        
        # Use the directory of the installer as the base for all file lookups
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent / "dist"
        
        # Check if executable exists
        exe_path = base_dir / self.app_exe
        if not exe_path.exists():
            messagebox.showerror("Error", f"Could not find {self.app_exe} in {base_dir}")
            return
        
        def install_thread():
            try:
                self.root.after(0, lambda: self.progress.start())
                self.root.after(0, lambda: self.status_var.set("Installing..."))
                
                # Create installation directory
                self.install_path.mkdir(parents=True, exist_ok=True)
                
                # List all files and folders to copy
                files_to_copy = [
                    "BabbittQuoteGenerator.exe",
                    "launcher.exe",
                    "update_manager.exe",
                    "installer_wizard.exe",
                    "install.bat",
                    "USER_GUIDE.md",
                    "INSTALLER_GUIDE.md",
                    "QUICK_DEPLOYMENT_GUIDE.md"
                ]
                folders_to_copy = [
                    "data",
                    "database",
                    "config",
                    "core",
                    "gui",
                    "utils",
                    "export",
                    "docs"
                ]
                # Copy files
                for file in files_to_copy:
                    src = base_dir / file
                    dst = self.install_path / file
                    if src.exists():
                        shutil.copy2(src, dst)
                # Copy folders (recursively, skip __pycache__ and .pyc)
                def ignore_patterns(dir, files):
                    return [f for f in files if f == '__pycache__' or fnmatch.fnmatch(f, '*.pyc')]
                for folder in folders_to_copy:
                    src_folder = base_dir / folder
                    dst_folder = self.install_path / folder
                    if src_folder.exists():
                        if dst_folder.exists():
                            shutil.rmtree(dst_folder)
                        shutil.copytree(src_folder, dst_folder, ignore=ignore_patterns)
                # Copy export/templates if present
                templates_src = base_dir / "export" / "templates"
                templates_dst = self.install_path / "export" / "templates"
                if templates_src.exists():
                    if templates_dst.exists():
                        shutil.rmtree(templates_dst)
                    shutil.copytree(templates_src, templates_dst, ignore=ignore_patterns)
                # Create desktop shortcut
                self.create_desktop_shortcut()
                # Create start menu shortcut
                self.create_start_menu_shortcut()
                # Add to registry
                self.add_registry_entries()
                # Update installation status
                self.is_installed = True
                self.current_install_path = self.install_path
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.status_var.set("Installation complete"))
                self.root.after(0, self.update_button_states)
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"{self.app_name} has been installed successfully!\n\n"
                    f"Location: {self.install_path}\n"
                    f"Desktop shortcut created.\n"
                    f"Start menu entry created."))
            except Exception as e:
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.status_var.set("Installation failed"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Installation failed: {e}"))
        threading.Thread(target=install_thread, daemon=True).start()
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        try:
            if not self.install_path:
                print("Install path is not set. Cannot create desktop shortcut.")
                return
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / f"{self.app_name}.lnk"
            
            # Use PowerShell to create shortcut
            ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{self.install_path / self.app_exe}"
$Shortcut.WorkingDirectory = "{self.install_path}"
$Shortcut.Description = "{self.app_name}"
$Shortcut.Save()
'''
            
            subprocess.run(["powershell", "-Command", ps_script], 
                         capture_output=True, check=True)
            
        except Exception as e:
            print(f"Failed to create desktop shortcut: {e}")
    
    def create_start_menu_shortcut(self):
        """Create start menu shortcut"""
        try:
            if not self.install_path:
                print("Install path is not set. Cannot create start menu shortcut.")
                return
            start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            app_folder = start_menu / self.app_name
            app_folder.mkdir(exist_ok=True)
            
            shortcut_path = app_folder / f"{self.app_name}.lnk"
            
            # Use PowerShell to create shortcut
            ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{self.install_path / self.app_exe}"
$Shortcut.WorkingDirectory = "{self.install_path}"
$Shortcut.Description = "{self.app_name}"
$Shortcut.Save()
'''
            
            subprocess.run(["powershell", "-Command", ps_script], 
                         capture_output=True, check=True)
            
        except Exception as e:
            print(f"Failed to create start menu shortcut: {e}")
    
    def add_registry_entries(self):
        """Add application to Windows registry"""
        try:
            if not self.install_path:
                print("Install path is not set. Cannot add registry entries.")
                return
            # Add uninstall information
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator"
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, self.app_name)
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, self.app_version)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, self.company_name)
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(self.install_path))
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, 
                            f'"{sys.executable}" "{__file__}" uninstall')
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, 
                            str(self.install_path / self.app_exe))
            
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"Failed to add registry entries: {e}")
    
    def update_application(self):
        """Update the application"""
        if not self.update_available:
            messagebox.showinfo("Info", "No updates available")
            return
        def update_thread():
            try:
                self.root.after(0, lambda: self.progress.start())
                self.root.after(0, lambda: self.status_var.set("Updating..."))
                # For demo, we'll just copy the current executable
                # In production, this would download the new version
                if self.current_install_path and Path(self.app_exe).exists():
                    shutil.copy2(self.app_exe, self.current_install_path / self.app_exe)
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.status_var.set("Update complete"))
                if self.update_info and 'version' in self.update_info:
                    msg = f"{self.app_name} has been updated to version {self.update_info['version']}"
                else:
                    msg = f"{self.app_name} has been updated."
                self.root.after(0, lambda: messagebox.showinfo("Success", msg))
            except Exception as e:
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.status_var.set("Update failed"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Update failed: {e}"))
        threading.Thread(target=update_thread, daemon=True).start()
    
    def uninstall_application(self):
        """Uninstall the application"""
        if not self.is_installed:
            messagebox.showinfo("Info", "Application is not installed")
            return
        
        result = messagebox.askyesno("Confirm Uninstall", 
            f"Are you sure you want to uninstall {self.app_name}?\n\n"
            f"This will remove the application and all its files.")
        
        if not result:
            return
        
        def uninstall_thread():
            try:
                self.root.after(0, lambda: self.progress.start())
                self.root.after(0, lambda: self.status_var.set("Uninstalling..."))
                
                # Remove files
                if self.current_install_path and self.current_install_path.exists():
                    shutil.rmtree(self.current_install_path)
                
                # Remove desktop shortcut
                desktop = Path.home() / "Desktop"
                shortcut_path = desktop / f"{self.app_name}.lnk"
                if shortcut_path.exists():
                    shortcut_path.unlink()
                
                # Remove start menu shortcut
                start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
                app_folder = start_menu / self.app_name
                if app_folder.exists():
                    shutil.rmtree(app_folder)
                
                # Remove registry entries
                try:
                    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BabbittQuoteGenerator"
                    winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                except:
                    pass
                
                # Update status
                self.is_installed = False
                self.current_install_path = None
                
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.status_var.set("Uninstall complete"))
                self.root.after(0, self.update_button_states)
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"{self.app_name} has been uninstalled successfully"))
                
            except Exception as e:
                self.root.after(0, lambda: self.progress.stop())
                self.root.after(0, lambda: self.status_var.set("Uninstall failed"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Uninstall failed: {e}"))
        
        threading.Thread(target=uninstall_thread, daemon=True).start()
    
    def run(self):
        """Run the installer"""
        self.root.mainloop()

def main():
    """Main entry point"""
    # Check if running as administrator
    try:
        if os.name == "nt":
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = False
    
    if not is_admin:
        # Re-run as administrator
        try:
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, 
                                               f'"{__file__}"', None, 1)
            return
        except:
            messagebox.showerror("Error", "This installer requires administrator privileges")
            return
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "uninstall":
            # Silent uninstall
            installer = InstallerWizard()
            installer.uninstall_application()
            return
    
    # Run installer GUI
    installer = InstallerWizard()
    installer.run()

if __name__ == "__main__":
    main() 
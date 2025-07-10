#!/usr/bin/env python3
"""
Launcher for Babbitt Quote Generator
Handles update checking and application startup
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

class ApplicationLauncher:
    def __init__(self):
        self.app_name = "Babbitt Quote Generator"
        self.app_exe = "BabbittQuoteGenerator.exe"
        self.update_manager = None
        
        # Try to import update manager
        try:
            from update_manager import UpdateManager
            self.update_manager = UpdateManager()
        except ImportError:
            pass
    
    def show_splash_screen(self):
        """Show splash screen while checking for updates"""
        splash = tk.Tk()
        splash.title(self.app_name)
        splash.geometry("400x200")
        splash.resizable(False, False)
        
        # Center window
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (400 // 2)
        y = (splash.winfo_screenheight() // 2) - (200 // 2)
        splash.geometry(f"400x200+{x}+{y}")
        
        # Remove window decorations
        splash.overrideredirect(True)
        
        # Create content
        main_frame = ttk.Frame(splash, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        splash.columnconfigure(0, weight=1)
        splash.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # App title
        ttk.Label(main_frame, text=self.app_name, 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(0, 10))
        
        # Status label
        status_var = tk.StringVar(value="Starting...")
        status_label = ttk.Label(main_frame, textvariable=status_var)
        status_label.grid(row=1, column=0, pady=(0, 20))
        
        # Progress bar
        progress = ttk.Progressbar(main_frame, mode='indeterminate')
        progress.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        progress.start()
        
        # Version info
        version_text = f"Version {self.update_manager.current_version if self.update_manager else '1.0.0'}"
        ttk.Label(main_frame, text=version_text, 
                 font=("Arial", 8)).grid(row=3, column=0)
        
        return splash, status_var, progress
    
    def check_for_updates(self, status_var, progress):
        """Check for updates in background"""
        if not self.update_manager:
            status_var.set("Starting application...")
            time.sleep(1)
            return None
        
        try:
            status_var.set("Checking for updates...")
            time.sleep(0.5)
            
            update_info = self.update_manager.check_for_updates()
            
            if update_info:
                status_var.set(f"Update available: {update_info['version']}")
                time.sleep(1)
                return update_info
            else:
                status_var.set("No updates available")
                time.sleep(0.5)
                return None
                
        except Exception as e:
            status_var.set("Update check failed")
            time.sleep(0.5)
            return None
    
    def launch_application(self):
        """Launch the main application"""
        try:
            # Find the executable
            exe_path = None
            
            # Check current directory
            if Path(self.app_exe).exists():
                exe_path = Path(self.app_exe)
            # Check installation directory
            elif self.update_manager and self.update_manager.app_dir:
                potential_path = self.update_manager.app_dir / self.app_exe
                if potential_path.exists():
                    exe_path = potential_path
            
            if not exe_path:
                raise FileNotFoundError(f"Could not find {self.app_exe}")
            
            # Launch application
            subprocess.Popen([str(exe_path)])
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch application: {e}")
            return False
    
    def run(self):
        """Run the launcher"""
        # Show splash screen
        splash, status_var, progress = self.show_splash_screen()
        
        # Check for updates in background
        def update_check():
            update_info = self.check_for_updates(status_var, progress)
            
            # Close splash screen
            splash.after(0, splash.destroy)
            
            # Handle update if available
            if update_info:
                result = messagebox.askyesno("Update Available", 
                    f"Version {update_info['version']} is available.\n\n"
                    f"Description: {update_info['description']}\n\n"
                    f"Would you like to install the update now?")
                
                if result and self.update_manager:
                    try:
                        # Install update
                        messagebox.showinfo("Update", "Update will be installed. The application will restart.")
                        
                        # Download and install update
                        download_path = self.update_manager.download_update(update_info)
                        self.update_manager.install_update(download_path, update_info)
                        self.update_manager.add_update_history(update_info)
                        
                        # Restart launcher
                        os.execv(sys.executable, ['python'] + sys.argv)
                        return
                        
                    except Exception as e:
                        messagebox.showerror("Update Failed", f"Update installation failed: {e}")
            
            # Launch application
            self.launch_application()
        
        # Start update check in background
        threading.Thread(target=update_check, daemon=True).start()
        
        # Run splash screen
        splash.mainloop()

def main():
    """Main entry point"""
    launcher = ApplicationLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 
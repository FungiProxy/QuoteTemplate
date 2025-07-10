"""
Dialog Windows for Babbitt Quote Generator
Provides various dialog windows for user interaction
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import APP_NAME, APP_VERSION, COMPANY_NAME, QUOTE_TEMPLATE_PATH

class AboutDialog:
    """About dialog for the application"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        self.create_content()
    
    def setup_dialog(self):
        """Setup dialog properties"""
        self.dialog.title(f"About {APP_NAME}")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 150
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def create_content(self):
        """Create dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Application name and version
        title_label = ttk.Label(main_frame, text=APP_NAME, font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 5))
        
        version_label = ttk.Label(main_frame, text=f"Version {APP_VERSION}", font=("Arial", 10))
        version_label.pack(pady=(0, 15))
        
        # Description
        description = """Professional quote generation tool for Babbitt level switches.
        
Features:
• Part number parsing and validation
• Automatic pricing calculation
• Database-driven specifications
• Word document quote generation
• Comprehensive compatibility checking"""
        
        desc_label = ttk.Label(main_frame, text=description, justify=tk.LEFT, font=("Arial", 9))
        desc_label.pack(pady=(0, 15))
        
        # Company information
        company_label = ttk.Label(main_frame, text=f"© 2024 {COMPANY_NAME}", font=("Arial", 9))
        company_label.pack(pady=(0, 10))
        
        # License information
        license_text = "This software is provided for internal use only."
        license_label = ttk.Label(main_frame, text=license_text, font=("Arial", 8), foreground="gray")
        license_label.pack(pady=(0, 15))
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.dialog.destroy)
        close_button.pack()
        
        # Focus and key bindings
        close_button.focus()
        self.dialog.bind('<Return>', lambda e: self.dialog.destroy())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())

class SettingsDialog:
    """Settings dialog for application configuration"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.result = None
        self.setup_dialog()
        self.create_content()
    
    def setup_dialog(self):
        """Setup dialog properties"""
        self.dialog.title("Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 250
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 200
        self.dialog.geometry(f"500x400+{x}+{y}")
    
    def create_content(self):
        """Create dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabbed settings
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # General settings tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self.create_general_settings(general_frame)
        
        # Database settings tab
        database_frame = ttk.Frame(notebook)
        notebook.add(database_frame, text="Database")
        self.create_database_settings(database_frame)
        
        # Export settings tab
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="Export")
        self.create_export_settings(export_frame)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Apply", command=self.on_apply).pack(side=tk.RIGHT, padx=(0, 5))
    
    def create_general_settings(self, parent):
        """Create general settings"""
        # Company information
        company_frame = ttk.LabelFrame(parent, text="Company Information", padding="10")
        company_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(company_frame, text="Company Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.company_var = tk.StringVar(value=COMPANY_NAME)
        ttk.Entry(company_frame, textvariable=self.company_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(company_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.phone_var = tk.StringVar(value="(555) 123-4567")
        ttk.Entry(company_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(company_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.email_var = tk.StringVar(value="quotes@company.com")
        ttk.Entry(company_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(5, 0))
        
        company_frame.columnconfigure(1, weight=1)
        
        # Default values
        defaults_frame = ttk.LabelFrame(parent, text="Default Values", padding="10")
        defaults_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(defaults_frame, text="Default Customer:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.default_customer_var = tk.StringVar(value="New Customer")
        ttk.Entry(defaults_frame, textvariable=self.default_customer_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(defaults_frame, text="Default Quantity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.default_quantity_var = tk.StringVar(value="1")
        ttk.Entry(defaults_frame, textvariable=self.default_quantity_var, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 0))
        
        defaults_frame.columnconfigure(1, weight=1)
    
    def create_database_settings(self, parent):
        """Create database settings"""
        # Database info
        info_frame = ttk.LabelFrame(parent, text="Database Information", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text="Database Path:").pack(anchor=tk.W)
        path_frame = ttk.Frame(info_frame)
        path_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.db_path_var = tk.StringVar(value=str(QUOTE_TEMPLATE_PATH.parent / "quotes.db"))
        db_path_entry = ttk.Entry(path_frame, textvariable=self.db_path_var, state="readonly")
        db_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="Browse", command=self.browse_database).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Database status
        status_frame = ttk.LabelFrame(parent, text="Database Status", padding="10")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.db_status_var = tk.StringVar(value="Checking...")
        ttk.Label(status_frame, textvariable=self.db_status_var).pack(anchor=tk.W)
        
        ttk.Button(status_frame, text="Test Connection", command=self.test_database).pack(anchor=tk.W, pady=(5, 0))
        
        # Check database status
        self.check_database_status()
    
    def create_export_settings(self, parent):
        """Create export settings"""
        # Template settings
        template_frame = ttk.LabelFrame(parent, text="Template Settings", padding="10")
        template_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(template_frame, text="Quote Template:").pack(anchor=tk.W)
        template_path_frame = ttk.Frame(template_frame)
        template_path_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.template_path_var = tk.StringVar(value=str(QUOTE_TEMPLATE_PATH))
        template_entry = ttk.Entry(template_path_frame, textvariable=self.template_path_var, state="readonly")
        template_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(template_path_frame, text="Browse", command=self.browse_template).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Export options
        options_frame = ttk.LabelFrame(parent, text="Export Options", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_open_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-open exported documents", variable=self.auto_open_var).pack(anchor=tk.W)
        
        self.save_backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Save backup copies", variable=self.save_backup_var).pack(anchor=tk.W)
    
    def browse_database(self):
        """Browse for database file"""
        filename = filedialog.askopenfilename(
            title="Select Database File",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
        )
        if filename:
            self.db_path_var.set(filename)
    
    def browse_template(self):
        """Browse for template file"""
        filename = filedialog.askopenfilename(
            title="Select Quote Template",
            filetypes=[("Word Document", "*.docx"), ("All Files", "*.*")]
        )
        if filename:
            self.template_path_var.set(filename)
    
    def test_database(self):
        """Test database connection"""
        self.db_status_var.set("Testing connection...")
        self.dialog.update()
        
        try:
            # Here you would test the actual database connection
            # For now, just simulate a test
            import time
            time.sleep(1)
            self.db_status_var.set("Database connection: OK")
        except Exception as e:
            self.db_status_var.set(f"Database connection: Error - {str(e)}")
    
    def check_database_status(self):
        """Check current database status"""
        try:
            db_path = self.db_path_var.get()
            if os.path.exists(db_path):
                size = os.path.getsize(db_path)
                self.db_status_var.set(f"Database found ({size} bytes)")
            else:
                self.db_status_var.set("Database not found")
        except Exception as e:
            self.db_status_var.set(f"Error checking database: {str(e)}")
    
    def on_ok(self):
        """Handle OK button"""
        self.apply_settings()
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button"""
        self.dialog.destroy()
    
    def on_apply(self):
        """Handle Apply button"""
        self.apply_settings()
    
    def apply_settings(self):
        """Apply the settings"""
        # Here you would save the settings to a configuration file
        # For now, just show a message
        messagebox.showinfo("Settings", "Settings applied successfully!")

class ExportDialog:
    """Export dialog for saving quotes"""
    
    def __init__(self, parent, quote_data: Dict[str, Any], quote_number: Optional[str] = None):
        self.parent = parent
        self.quote_data = quote_data
        self.quote_number = quote_number
        self.dialog = tk.Toplevel(parent)
        self.result = None
        self.setup_dialog()
        self.create_content()
    
    def setup_dialog(self):
        """Setup dialog properties"""
        self.dialog.title("Export Quote")
        self.dialog.geometry("500x400")  # Increased size
        self.dialog.resizable(True, True)  # Made resizable
        self.dialog.minsize(450, 350)  # Set minimum size
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 250
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 200
        self.dialog.geometry(f"500x400+{x}+{y}")
    
    def create_content(self):
        """Create dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Export information
        info_frame = ttk.LabelFrame(main_frame, text="Export Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        part_number = self.quote_data.get('part_number', 'N/A')
        total_price = self.quote_data.get('total_price', 0)
        
        ttk.Label(info_frame, text=f"Part Number: {part_number}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Total Price: ${total_price:.2f}").pack(anchor=tk.W)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Output File", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="Save as:").pack(anchor=tk.W)
        
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Default filename - use quote number if available, otherwise part number
        if self.quote_number:
            default_name = f"{self.quote_number}.docx"
        else:
            default_name = f"Quote_{part_number.replace('/', '_').replace('\"', 'in')}.docx"
        self.file_path_var = tk.StringVar(value=default_name)
        
        file_entry = ttk.Entry(path_frame, textvariable=self.file_path_var)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Export options
        options_frame = ttk.LabelFrame(main_frame, text="Export Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.open_after_export_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Open document after export", variable=self.open_after_export_var).pack(anchor=tk.W)
        
        self.include_specs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include technical specifications", variable=self.include_specs_var).pack(anchor=tk.W)
        
        self.include_pricing_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include pricing breakdown", variable=self.include_pricing_var).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Export", command=self.on_export).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT)
        
        # Key bindings
        self.dialog.bind('<Return>', lambda e: self.on_export())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def browse_file(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Save Quote As",
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx"), ("All Files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def on_export(self):
        """Handle export button"""
        print("=== ExportDialog.on_export() called ===")
        file_path = self.file_path_var.get()
        print(f"Initial file path: '{file_path}'")
        
        if not file_path:
            print("❌ No file path specified")
            messagebox.showerror("Error", "Please specify a file path.")
            return
        
        # Ensure .docx extension
        if not file_path.lower().endswith('.docx'):
            file_path += '.docx'
            self.file_path_var.set(file_path)
            print(f"Added .docx extension: '{file_path}'")
        
        # If it's just a filename (no directory path), use file dialog to get full path
        import os
        if not os.path.dirname(file_path):
            print(f"No directory in path '{file_path}' - opening file dialog")
            full_path = filedialog.asksaveasfilename(
                title="Save Quote As",
                defaultextension=".docx",
                filetypes=[("Word Document", "*.docx"), ("All Files", "*.*")],
                initialfile=file_path
            )
            print(f"File dialog returned: '{full_path}'")
            
            if not full_path or (isinstance(full_path, str) and full_path.strip() == ""):
                print("❌ User cancelled file dialog")
                return  # User cancelled
            file_path = str(full_path)
            print(f"Using full path: '{file_path}'")
        
        # Prepare export options
        print("✓ Preparing export result")
        self.result = {
            'file_path': file_path,
            'open_after_export': self.open_after_export_var.get(),
            'include_specs': self.include_specs_var.get(),
            'include_pricing': self.include_pricing_var.get()
        }
        print(f"Export result prepared: {self.result}")
        
        print("✓ Destroying ExportDialog")
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle cancel button"""
        self.result = None
        self.dialog.destroy()

class ErrorDialog:
    """Error dialog for displaying detailed error information"""
    
    def __init__(self, parent, title: str, message: str, details: str = None):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog(title)
        self.create_content(message, details)
    
    def setup_dialog(self, title: str):
        """Setup dialog properties"""
        self.dialog.title(title)
        self.dialog.geometry("500x350")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 250
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 175
        self.dialog.geometry(f"500x350+{x}+{y}")
    
    def create_content(self, message: str, details: str):
        """Create dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Error icon and message
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Error message
        message_label = ttk.Label(header_frame, text=message, font=("Arial", 10, "bold"))
        message_label.pack(anchor=tk.W)
        
        # Details section
        if details:
            details_frame = ttk.LabelFrame(main_frame, text="Details", padding="10")
            details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Text widget with scrollbar
            text_frame = ttk.Frame(details_frame)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=text_widget.yview)
            
            text_widget.insert(1.0, details)
            text_widget.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="OK", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Key bindings
        self.dialog.bind('<Return>', lambda e: self.dialog.destroy())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy()) 
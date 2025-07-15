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
from database.db_manager import DatabaseManager
from utils.helpers import format_phone_number, unformat_phone_number

class PhoneEntry(ttk.Entry):
    """Entry widget that automatically formats phone numbers as user types"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Bind to key release to format as user types
        self.bind('<KeyRelease>', self._on_key_release)
        self.bind('<FocusOut>', self._on_focus_out)
        
        # Store the last formatted value to prevent infinite loops
        self._last_formatted = ""
    
    def _on_key_release(self, event):
        """Format phone number as user types"""
        # Skip formatting for navigation keys
        if event.keysym in ['BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Home', 'End']:
            return
        
        current_value = self.get()
        
        # Don't format if it's the same as last formatted value
        if current_value == self._last_formatted:
            return
        
        # Get cursor position before formatting
        cursor_pos = self.index(tk.INSERT)
        
        # Format the phone number
        formatted = format_phone_number(current_value)
        
        # Only update if formatting changed something
        if formatted != current_value:
            self.delete(0, tk.END)
            self.insert(0, formatted)
            
            # Try to maintain cursor position as best as possible
            # For phone formatting, cursor usually moves forward
            if len(formatted) > len(current_value):
                new_cursor_pos = min(cursor_pos + 1, len(formatted))
            else:
                new_cursor_pos = min(cursor_pos, len(formatted))
            
            self.icursor(new_cursor_pos)
        
        self._last_formatted = formatted
    
    def _on_focus_out(self, event):
        """Final formatting when user leaves the field"""
        current_value = self.get()
        formatted = format_phone_number(current_value)
        
        if formatted != current_value:
            self.delete(0, tk.END)
            self.insert(0, formatted)
            self._last_formatted = formatted
    
    def get_unformatted(self) -> str:
        """Get the phone number without formatting (digits only)"""
        return unformat_phone_number(self.get())
    
    def set_value(self, value: str):
        """Set the value with proper formatting"""
        formatted = format_phone_number(value)
        self.delete(0, tk.END)
        self.insert(0, formatted)
        self._last_formatted = formatted

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


class ShortcutManagerDialog:
    """Dialog for managing part number shortcuts"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.db_manager = DatabaseManager()
        self.selected_shortcut = None
        self.setup_dialog()
        self.create_content()
        self.load_shortcuts()
    
    def setup_dialog(self):
        """Setup dialog properties"""
        self.dialog.title("Manage Part Number Shortcuts")
        self.dialog.geometry("800x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 400
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 250
        self.dialog.geometry(f"800x500+{x}+{y}")
    
    def create_content(self):
        """Create dialog content"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Part Number Shortcuts", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Instructions
        instructions = "Create shortcuts for frequently used part numbers. Use only letters and numbers for shortcuts."
        inst_label = ttk.Label(main_frame, text=instructions, font=("Arial", 9), foreground="gray")
        inst_label.pack(pady=(0, 15))
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=0)
        content_frame.rowconfigure(0, weight=1)
        
        # Left side - List of shortcuts
        list_frame = ttk.LabelFrame(content_frame, text="Existing Shortcuts", padding="10")
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for shortcuts
        columns = ("Shortcut", "Part Number", "Description")
        self.shortcuts_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.shortcuts_tree.heading("Shortcut", text="Shortcut")
        self.shortcuts_tree.heading("Part Number", text="Part Number")
        self.shortcuts_tree.heading("Description", text="Description")
        
        self.shortcuts_tree.column("Shortcut", width=100, minwidth=80)
        self.shortcuts_tree.column("Part Number", width=200, minwidth=150)
        self.shortcuts_tree.column("Description", width=250, minwidth=200)
        
        # Scrollbars for treeview
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.shortcuts_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.shortcuts_tree.xview)
        self.shortcuts_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.shortcuts_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind selection event
        self.shortcuts_tree.bind("<<TreeviewSelect>>", self.on_shortcut_select)
        
        # Right side - Add/Edit form
        form_frame = ttk.LabelFrame(content_frame, text="Add/Edit Shortcut", padding="10")
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)
        
        # Shortcut entry
        ttk.Label(form_frame, text="Shortcut:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 5))
        self.shortcut_var = tk.StringVar()
        self.shortcut_entry = ttk.Entry(form_frame, textvariable=self.shortcut_var, width=20)
        self.shortcut_entry.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        
        # Add validation for alphanumeric only and autocapitalization
        def validate_shortcut(*args):
            current = self.shortcut_var.get()
            # Only allow letters and numbers
            filtered = ''.join(c for c in current if c.isalnum())
            if current != filtered:
                self.shortcut_var.set(filtered)
            # Auto-capitalize
            if current != current.upper():
                self.shortcut_var.set(current.upper())
        
        self.shortcut_var.trace('w', validate_shortcut)
        
        # Part number entry
        ttk.Label(form_frame, text="Part Number:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 5))
        self.part_number_var = tk.StringVar()
        self.part_number_entry = ttk.Entry(form_frame, textvariable=self.part_number_var, width=30)
        self.part_number_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5))
        
        # Add autocapitalization for part number
        def autocapitalize_part_number(*args):
            current = self.part_number_var.get()
            if current != current.upper():
                self.part_number_var.set(current.upper())
        
        self.part_number_var.trace('w', autocapitalize_part_number)
        
        # Description entry
        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 15))
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(form_frame, textvariable=self.description_var, width=30)
        self.description_entry.grid(row=2, column=1, sticky="ew", pady=(0, 15))
        
        # Add autocapitalization for description
        def autocapitalize_description(*args):
            current = self.description_var.get()
            if current != current.upper():
                self.description_var.set(current.upper())
        
        self.description_var.trace('w', autocapitalize_description)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        button_frame.columnconfigure(0, weight=1)
        
        self.add_button = ttk.Button(button_frame, text="Add", command=self.add_shortcut)
        self.add_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.update_button = ttk.Button(button_frame, text="Update", command=self.update_shortcut, state="disabled")
        self.update_button.grid(row=0, column=1, padx=(0, 5), sticky="ew")
        
        self.delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_shortcut, state="disabled")
        self.delete_button.grid(row=0, column=2, sticky="ew")
        
        # Clear form button
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_form)
        clear_button.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        
        # Key bindings
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
        self.shortcut_entry.bind('<Return>', lambda e: self.add_shortcut())
        self.part_number_entry.bind('<Return>', lambda e: self.add_shortcut())
        self.description_entry.bind('<Return>', lambda e: self.add_shortcut())
    
    def load_shortcuts(self):
        """Load shortcuts from database"""
        try:
            # Clear existing items
            for item in self.shortcuts_tree.get_children():
                self.shortcuts_tree.delete(item)
            
            # Get shortcuts from database
            shortcuts = self.db_manager.get_part_number_shortcuts()
            
            for shortcut_data in shortcuts:
                self.shortcuts_tree.insert("", tk.END, values=(
                    shortcut_data['shortcut'],
                    shortcut_data['part_number'],
                    shortcut_data.get('description', '')
                ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load shortcuts: {str(e)}")
    
    def on_shortcut_select(self, event):
        """Handle shortcut selection"""
        selection = self.shortcuts_tree.selection()
        if selection:
            item = self.shortcuts_tree.item(selection[0])
            values = item['values']
            
            # Fill form with selected values
            self.shortcut_var.set(values[0])
            self.part_number_var.set(values[1])
            self.description_var.set(values[2] if len(values) > 2 else '')
            
            # Enable update/delete buttons
            self.update_button.config(state="normal")
            self.delete_button.config(state="normal")
            self.add_button.config(state="disabled")
            
            self.selected_shortcut = values[0]
        else:
            self.clear_form()
    
    def clear_form(self):
        """Clear the form"""
        self.shortcut_var.set('')
        self.part_number_var.set('')
        self.description_var.set('')
        self.selected_shortcut = None
        
        # Reset button states
        self.add_button.config(state="normal")
        self.update_button.config(state="disabled")
        self.delete_button.config(state="disabled")
        
        # Clear selection
        self.shortcuts_tree.selection_remove(self.shortcuts_tree.selection())
    
    def add_shortcut(self):
        """Add a new shortcut"""
        shortcut = self.shortcut_var.get().strip()
        part_number = self.part_number_var.get().strip()
        description = self.description_var.get().strip()
        
        if not shortcut:
            messagebox.showerror("Error", "Shortcut cannot be empty")
            return
        
        if not part_number:
            messagebox.showerror("Error", "Part number cannot be empty")
            return
        
        # Validate shortcut format
        if not shortcut.isalnum():
            messagebox.showerror("Error", "Shortcut must contain only letters and numbers")
            return
        
        try:
            self.db_manager.add_part_number_shortcut(shortcut, part_number, description)
            self.load_shortcuts()
            self.clear_form()
            messagebox.showinfo("Success", f"Shortcut '{shortcut}' added successfully")
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", f"Shortcut '{shortcut}' already exists")
            else:
                messagebox.showerror("Error", f"Failed to add shortcut: {str(e)}")
    
    def update_shortcut(self):
        """Update the selected shortcut"""
        if not self.selected_shortcut:
            return
        
        shortcut = self.shortcut_var.get().strip()
        part_number = self.part_number_var.get().strip()
        description = self.description_var.get().strip()
        
        if not shortcut:
            messagebox.showerror("Error", "Shortcut cannot be empty")
            return
        
        if not part_number:
            messagebox.showerror("Error", "Part number cannot be empty")
            return
        
        # Validate shortcut format
        if not shortcut.isalnum():
            messagebox.showerror("Error", "Shortcut must contain only letters and numbers")
            return
        
        try:
            self.db_manager.update_part_number_shortcut(self.selected_shortcut, shortcut, part_number, description)
            self.load_shortcuts()
            self.clear_form()
            messagebox.showinfo("Success", f"Shortcut updated successfully")
        
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Error", f"Shortcut '{shortcut}' already exists")
            else:
                messagebox.showerror("Error", f"Failed to update shortcut: {str(e)}")
    
    def delete_shortcut(self):
        """Delete the selected shortcut"""
        if not self.selected_shortcut:
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the shortcut '{self.selected_shortcut}'?"):
            try:
                self.db_manager.delete_part_number_shortcut(self.selected_shortcut)
                self.load_shortcuts()
                self.clear_form()
                messagebox.showinfo("Success", "Shortcut deleted successfully")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete shortcut: {str(e)}")

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
        ttk.Entry(company_frame, textvariable=self.company_var, width=30).grid(row=0, column=1, sticky="we")
        
        ttk.Label(company_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.phone_var = tk.StringVar(value="(555) 123-4567")
        self.phone_entry = PhoneEntry(company_frame, textvariable=self.phone_var, width=30)
        self.phone_entry.grid(row=1, column=1, sticky="we", pady=(5, 0))
        
        ttk.Label(company_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.email_var = tk.StringVar(value="quotes@company.com")
        ttk.Entry(company_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, sticky="we", pady=(5, 0))
        
        company_frame.columnconfigure(1, weight=1)
        
        # Default values
        defaults_frame = ttk.LabelFrame(parent, text="Default Values", padding="10")
        defaults_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(defaults_frame, text="Default Customer:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.default_customer_var = tk.StringVar(value="New Customer")
        ttk.Entry(defaults_frame, textvariable=self.default_customer_var, width=30).grid(row=0, column=1, sticky="we")
        
        ttk.Label(defaults_frame, text="Default Quantity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.default_quantity_var = tk.StringVar(value="1")
        ttk.Entry(defaults_frame, textvariable=self.default_quantity_var, width=30).grid(row=1, column=1, sticky="we", pady=(5, 0))
        
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
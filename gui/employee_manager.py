"""
Employee Management Dialog
Provides interface for managing employee information
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, Callable
import re
from gui.dialogs import PhoneEntry
from utils.helpers import format_phone_number, unformat_phone_number

class EmployeeManagerDialog:
    """Dialog for managing employee information"""
    
    def __init__(self, parent, db_manager, on_employee_selected: Optional[Callable] = None):
        self.parent = parent
        self.db_manager = db_manager
        self.on_employee_selected = on_employee_selected
        self.selected_employee_id = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Employee Management")
        self.dialog.geometry("1000x600")
        self.dialog.resizable(True, True)
        
        # Center dialog on parent
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center window
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"1000x600+{x}+{y}")
        
        self.create_widgets()
        self.load_employees()
        
    def create_widgets(self):
        """Create the dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Employee Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Employee list frame (left side)
        list_frame = ttk.LabelFrame(main_frame, text="Employees", padding="10")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_employees)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")
        
        # Employee list
        columns = ('name', 'email', 'phone', 'status')
        self.employee_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.employee_tree.heading('name', text='Name')
        self.employee_tree.heading('email', text='Email')
        self.employee_tree.heading('phone', text='Phone')
        self.employee_tree.heading('status', text='Status')
        
        self.employee_tree.column('name', width=150)
        self.employee_tree.column('email', width=200)
        self.employee_tree.column('phone', width=120)
        self.employee_tree.column('status', width=80)
        
        # Scrollbar for tree
        tree_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.employee_tree.yview)
        self.employee_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.employee_tree.grid(row=1, column=0, sticky="nsew")
        tree_scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Bind selection event
        self.employee_tree.bind('<<TreeviewSelect>>', self.on_employee_select)
        
        # Employee details frame (right side)
        details_frame = ttk.LabelFrame(main_frame, text="Employee Details", padding="10")
        details_frame.grid(row=1, column=1, sticky="nsew")
        details_frame.columnconfigure(1, weight=1)
        details_frame.config(width=350)
        
        # Form fields
        ttk.Label(details_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(details_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        ttk.Label(details_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=2)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(details_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        ttk.Label(details_frame, text="Work Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(details_frame, textvariable=self.email_var)
        self.email_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        ttk.Label(details_frame, text="Work Phone:").grid(row=3, column=0, sticky="w", pady=2)
        self.phone_var = tk.StringVar()
        self.phone_entry = PhoneEntry(details_frame, textvariable=self.phone_var)
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        # Active status
        self.active_var = tk.BooleanVar(value=True)
        active_check = ttk.Checkbutton(details_frame, text="Active", variable=self.active_var)
        active_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        # Buttons frame (custom layout)
        buttons_frame = ttk.Frame(details_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        for i in range(2):
            buttons_frame.columnconfigure(i, weight=1, uniform="btn")

        btn_width = 18
        pad = 3

        # Row 0: New Employee
        self.new_button = ttk.Button(buttons_frame, text="New Employee", command=self.new_employee, width=btn_width)
        self.new_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=pad, pady=(0, pad))

        # Row 1: Select for Quote
        if self.on_employee_selected:
            self.select_button = ttk.Button(buttons_frame, text="Select for Quote", command=self.select_employee, width=btn_width)
            self.select_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=pad, pady=(0, pad))
        else:
            self.select_button = None

        # Row 2: Edit (left), Delete (right)
        self.edit_button = ttk.Button(buttons_frame, text="Edit", command=self.edit_employee, width=btn_width)
        self.edit_button.grid(row=2, column=0, sticky="ew", padx=(pad, pad//2), pady=(0, pad))
        self.delete_perm_button = ttk.Button(buttons_frame, text="Delete", command=self.delete_employee_permanently, width=btn_width)
        self.delete_perm_button.grid(row=2, column=1, sticky="ew", padx=(pad//2, pad), pady=(0, pad))

        # Row 3: Spacer
        buttons_frame.grid_rowconfigure(3, minsize=10)

        # Row 4: Save
        self.save_button = ttk.Button(buttons_frame, text="Save", command=self.save_employee, width=btn_width)
        self.save_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=pad, pady=(0, pad))

        # Row 5: Close
        self.close_button = ttk.Button(buttons_frame, text="Close", command=self.dialog.destroy, width=btn_width)
        self.close_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=pad, pady=(0, 0))

        # Initially disable form fields
        self.set_form_enabled(False)
        
    def load_employees(self):
        """Load employees from database"""
        try:
            # Clear existing items
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)
            
            # Get employees from database
            employees = self.db_manager.get_all_employees(active_only=False)
            
            for employee in employees:
                name = f"{employee['last_name']}, {employee['first_name']}"
                status = "Active" if employee['is_active'] else "Inactive"
                # Format phone number for display
                phone_display = format_phone_number(employee['work_phone']) if employee['work_phone'] else ''
                
                self.employee_tree.insert('', 'end', 
                                        values=(name, employee['work_email'], 
                                               phone_display, status),
                                        tags=(employee['id'],))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {str(e)}")
    
    def filter_employees(self, *args):
        """Filter employees based on search term"""
        search_term = self.search_var.get().lower()
        
        # Show/hide items based on search
        for item in self.employee_tree.get_children():
            values = self.employee_tree.item(item)['values']
            name = values[0].lower()
            email = values[1].lower()
            
            if search_term in name or search_term in email:
                self.employee_tree.reattach(item, '', 'end')
            else:
                self.employee_tree.detach(item)
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selection = self.employee_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        employee_id = self.employee_tree.item(item)['tags'][0]
        
        # Load employee details
        employee = self.db_manager.get_employee_by_id(employee_id)
        if employee:
            self.selected_employee_id = employee_id
            self.first_name_var.set(employee['first_name'])
            self.last_name_var.set(employee['last_name'])
            self.email_var.set(employee['work_email'])
            # Format phone number for display
            if employee['work_phone']:
                self.phone_entry.set_value(employee['work_phone'])
            else:
                self.phone_var.set('')
            self.active_var.set(employee['is_active'])
            
            self.set_form_enabled(True)
    
    def set_form_enabled(self, enabled: bool):
        """Enable or disable action buttons based on selection. Entry fields are always enabled."""
        # Entry fields always enabled
        self.first_name_entry.config(state='normal')
        self.last_name_entry.config(state='normal')
        self.email_entry.config(state='normal')
        self.phone_entry.config(state='normal')
        # Save is always enabled
        self.save_button.config(state='normal')
        # Edit, Delete, Select for Quote only enabled if an employee is selected
        edit_state = 'normal' if enabled else 'disabled'
        self.edit_button.config(state=edit_state)
        self.delete_perm_button.config(state=edit_state)
        if self.select_button:
            self.select_button.config(state=edit_state)
        # New Employee and Close always enabled
        self.new_button.config(state='normal')
        self.close_button.config(state='normal')

    def clear_form(self):
        """Clear all form fields"""
        self.selected_employee_id = None
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.email_var.set('')
        self.phone_var.set('')
        self.active_var.set(True)
        # Clear selection
        self.employee_tree.selection_remove(self.employee_tree.selection())
        self.set_form_enabled(False)

    def validate_form(self) -> bool:
        """Validate form data"""
        errors = []
        
        if not self.first_name_var.get().strip():
            errors.append("First name is required")
        
        if not self.last_name_var.get().strip():
            errors.append("Last name is required")
        
        email = self.email_var.get().strip()
        if not email:
            errors.append("Email is required")
        elif not self.is_valid_email(email):
            errors.append("Invalid email format")
        
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False
        
        return True
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def new_employee(self):
        """Create new employee"""
        self.clear_form()
        self.set_form_enabled(False)
    
    def save_employee(self):
        """Save employee data"""
        if not self.validate_form():
            return
        
        try:
            first_name = self.first_name_var.get().strip()
            last_name = self.last_name_var.get().strip()
            email = self.email_var.get().strip()
            phone = self.phone_entry.get_unformatted() or None
            is_active = self.active_var.get()
            
            if self.selected_employee_id:
                # Update existing employee
                success = self.db_manager.update_employee(
                    self.selected_employee_id, first_name, last_name, email, phone, is_active
                )
                if success:
                    messagebox.showinfo("Success", "Employee updated successfully")
                else:
                    messagebox.showerror("Error", "Failed to update employee")
            else:
                # Add new employee
                success = self.db_manager.add_employee(first_name, last_name, email, phone)
                if success:
                    messagebox.showinfo("Success", "Employee added successfully")
                    self.clear_form()
                else:
                    messagebox.showerror("Error", "Failed to add employee")
            
            # Reload employee list
            self.load_employees()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save employee: {str(e)}")
    
    def delete_employee_permanently(self):
        """Permanently delete employee from the database"""
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Please select an employee to delete permanently")
            return
        result = messagebox.askyesno(
            "Confirm Permanent Delete",
            "Are you absolutely sure you want to permanently delete this employee?\n\n"
            "This cannot be undone and will remove the employee from the database.\n\n"
            "Click Yes to permanently delete, or No to cancel."
        )
        if not result:
            return
        try:
            success = self.db_manager.delete_employee_permanently(self.selected_employee_id)
            if success:
                messagebox.showinfo("Success", "Employee permanently deleted.")
                self.clear_form()
                self.load_employees()
            else:
                messagebox.showerror("Error", "Failed to permanently delete employee.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to permanently delete employee: {str(e)}")
    
    def select_employee(self):
        """Select employee for quote attribution"""
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Please select an employee")
            return
        
        if self.on_employee_selected:
            employee = self.db_manager.get_employee_by_id(self.selected_employee_id)
            if employee:
                self.on_employee_selected(employee)
                self.dialog.destroy()
    
    def edit_employee(self):
        """Edit the selected employee (load info into form)"""
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Please select an employee to edit")
            return
        employee = self.db_manager.get_employee_by_id(self.selected_employee_id)
        if employee:
            self.first_name_var.set(employee['first_name'])
            self.last_name_var.set(employee['last_name'])
            self.email_var.set(employee['work_email'])
            # Format phone number for display
            if employee['work_phone']:
                self.phone_entry.set_value(employee['work_phone'])
            else:
                self.phone_var.set('')
            self.active_var.set(employee['is_active'])
            self.set_form_enabled(True)
    
    def run(self):
        """Run the dialog"""
        self.dialog.wait_window()
        return self.dialog 
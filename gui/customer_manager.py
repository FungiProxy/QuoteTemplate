"""
Simple Customer Management Dialog
Provides interface for managing basic customer information: company, contact, email, phone
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, Callable
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.customer_db_manager import CustomerDBManager
from gui.dialogs import PhoneEntry
from utils.helpers import format_phone_number, unformat_phone_number

class CustomerManagerDialog:
    """Dialog for managing simple customer information"""
    
    def __init__(self, parent, on_customer_selected: Optional[Callable] = None):
        self.parent = parent
        self.customer_db = CustomerDBManager()
        self.on_customer_selected = on_customer_selected
        self.selected_customer_id = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Customer Management")
        self.dialog.geometry("1200x500")
        self.dialog.resizable(True, True)
        
        # Center dialog on parent
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center window
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"1200x500+{x}+{y}")
        
        self.create_widgets()
        self.load_customers()
        
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
        title_label = ttk.Label(main_frame, text="Customer Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left side - Customer list
        list_frame = ttk.LabelFrame(main_frame, text="Customers", padding="10")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_customers)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")
        
        # Customer list
        columns = ('customer', 'contact', 'email', 'phone')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.customer_tree.heading('customer', text='Customer (Company)')
        self.customer_tree.heading('contact', text='Contact Name')
        self.customer_tree.heading('email', text='Email')
        self.customer_tree.heading('phone', text='Phone')
        
        self.customer_tree.column('customer', width=200)
        self.customer_tree.column('contact', width=150)
        self.customer_tree.column('email', width=200)
        self.customer_tree.column('phone', width=120)
        
        # Scrollbar for tree
        tree_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.customer_tree.grid(row=1, column=0, sticky="nsew")
        tree_scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Bind selection event
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # Right side - Customer form
        form_frame = ttk.LabelFrame(main_frame, text="Customer Details", padding="10")
        form_frame.grid(row=1, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)
        
        # Customer Name (Company)
        ttk.Label(form_frame, text="Customer (Company):").grid(row=0, column=0, sticky="w", pady=2)
        self.customer_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.customer_name_var).grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        # Contact Name
        ttk.Label(form_frame, text="Contact Name:").grid(row=1, column=0, sticky="w", pady=2)
        self.contact_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.contact_name_var).grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=3, column=0, sticky="w", pady=2)
        self.phone_var = tk.StringVar()
        self.phone_entry = PhoneEntry(form_frame, textvariable=self.phone_var)
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=2)
        
        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        ttk.Button(buttons_frame, text="New Customer", command=self.new_customer).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete Customer", command=self.delete_customer).grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        ttk.Button(buttons_frame, text="Save", command=self.save_customer).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        if self.on_customer_selected:
            ttk.Button(buttons_frame, text="Select Customer", command=self.select_customer).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Close", command=self.dialog.destroy).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
    def load_customers(self):
        """Load customers from database"""
        try:
            # Clear existing items
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Get customers from database
            customers = self.customer_db.get_all_customers()
            
            for customer in customers:
                # Format phone number for display
                phone_display = format_phone_number(customer['phone']) if customer['phone'] else ''
                self.customer_tree.insert('', 'end', 
                                        values=(customer['customer_name'], 
                                               customer['contact_name'] or '',
                                               customer['email'] or '',
                                               phone_display),
                                        tags=(customer['id'],))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def filter_customers(self, *args):
        """Filter customers based on search term"""
        search_term = self.search_var.get().lower()
        
        # Show/hide items based on search
        for item in self.customer_tree.get_children():
            values = self.customer_tree.item(item)['values']
            customer_name = values[0].lower()
            contact_name = values[1].lower()
            
            if search_term in customer_name or search_term in contact_name:
                self.customer_tree.reattach(item, '', len(self.customer_tree.get_children()))
            else:
                self.customer_tree.detach(item)
    
    def on_customer_select(self, event):
        """Handle customer selection"""
        selection = self.customer_tree.selection()
        if selection:
            item = selection[0]
            customer_id = self.customer_tree.item(item)['tags'][0]
            self.load_customer_details(customer_id)
        else:
            self.clear_form()
    
    def load_customer_details(self, customer_id):
        """Load customer details into form"""
        try:
            customer = self.customer_db.get_customer(customer_id)
            if customer:
                self.customer_name_var.set(customer['customer_name'])
                self.contact_name_var.set(customer['contact_name'] or '')
                self.email_var.set(customer['email'] or '')
                # Format phone number for display
                if customer['phone']:
                    self.phone_entry.set_value(customer['phone'])
                else:
                    self.phone_var.set('')
                self.selected_customer_id = customer_id
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customer details: {str(e)}")
    
    def clear_form(self):
        """Clear the form"""
        self.customer_name_var.set('')
        self.contact_name_var.set('')
        self.email_var.set('')
        self.phone_var.set('')
        self.selected_customer_id = None
    
    def new_customer(self):
        """Create a new customer"""
        self.selected_customer_id = None
        self.clear_form()
    
    def save_customer(self):
        """Save customer data"""
        try:
            if not self.customer_name_var.get().strip():
                messagebox.showwarning("Warning", "Customer name is required.")
                return
            
            if self.selected_customer_id:
                # Update existing customer
                success = self.customer_db.update_customer(
                    self.selected_customer_id,
                    customer_name=self.customer_name_var.get().strip(),
                    contact_name=self.contact_name_var.get().strip() or None,
                    email=self.email_var.get().strip() or None,
                    phone=self.phone_entry.get_unformatted() or None
                )
                if success:
                    messagebox.showinfo("Success", "Customer updated successfully.")
                else:
                    messagebox.showerror("Error", "Failed to update customer.")
            else:
                # Create new customer
                customer_id = self.customer_db.add_customer(
                    customer_name=self.customer_name_var.get().strip(),
                    contact_name=self.contact_name_var.get().strip() or None,
                    email=self.email_var.get().strip() or None,
                    phone=self.phone_entry.get_unformatted() or None
                )
                self.selected_customer_id = customer_id
                messagebox.showinfo("Success", "Customer created successfully.")
            
            self.load_customers()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {str(e)}")
    
    def delete_customer(self):
        """Delete the selected customer"""
        if not self.selected_customer_id:
            messagebox.showwarning("Warning", "Please select a customer to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
            try:
                success = self.customer_db.delete_customer(self.selected_customer_id)
                if success:
                    messagebox.showinfo("Success", "Customer deleted successfully.")
                    self.selected_customer_id = None
                    self.clear_form()
                    self.load_customers()
                else:
                    messagebox.showerror("Error", "Failed to delete customer.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")
    
    def select_customer(self):
        """Select the current customer for quote generation"""
        if not self.selected_customer_id:
            messagebox.showwarning("Warning", "Please select a customer first.")
            return
        
        if self.on_customer_selected:
            customer = self.customer_db.get_customer(self.selected_customer_id)
            self.on_customer_selected(customer)
            self.dialog.destroy()
    
    def run(self):
        """Run the dialog"""
        self.dialog.wait_window()
        return self.selected_customer_id 
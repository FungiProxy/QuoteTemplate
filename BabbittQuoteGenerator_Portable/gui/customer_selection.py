"""
Simple Customer Selection Dialog
Provides quick customer search and selection for quote generation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, Callable
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.customer_db_manager import CustomerDBManager

class CustomerSelectionDialog:
    """Dialog for quick customer selection"""
    
    def __init__(self, parent, on_customer_selected: Optional[Callable] = None):
        self.parent = parent
        self.customer_db = CustomerDBManager()
        self.on_customer_selected = on_customer_selected
        self.selected_customer = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Customer")
        self.dialog.geometry("700x400")
        self.dialog.resizable(True, True)
        
        # Center dialog on parent
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center window
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"700x400+{x}+{y}")
        
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
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Select Customer", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_customers)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 10))
        search_entry.grid(row=0, column=1, sticky="ew")
        search_entry.focus()
        
        # Customer list frame
        list_frame = ttk.LabelFrame(main_frame, text="Customers", padding="10")
        list_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Customer list
        columns = ('customer', 'contact', 'email', 'phone')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
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
        
        self.customer_tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind selection event
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        self.customer_tree.bind('<Double-1>', self.on_customer_double_click)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, pady=(10, 0), sticky="ew")
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        
        ttk.Button(buttons_frame, text="New Customer", command=self.new_customer).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(buttons_frame, text="Select Customer", command=self.select_customer).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=2, sticky="ew", padx=(5, 0))
        
        # Bind Enter key to select customer
        self.dialog.bind('<Return>', lambda e: self.select_customer())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
        
    def load_customers(self):
        """Load customers from database"""
        try:
            # Clear existing items
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Get customers from database
            customers = self.customer_db.get_all_customers()
            
            for customer in customers:
                self.customer_tree.insert('', 'end', 
                                        values=(customer['customer_name'], 
                                               customer['contact_name'] or '',
                                               customer['email'] or '',
                                               customer['phone'] or ''),
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
            self.selected_customer = self.customer_db.get_customer(int(customer_id))
        else:
            self.selected_customer = None
    
    def on_customer_double_click(self, event):
        """Handle customer double-click"""
        self.select_customer()
    
    def new_customer(self):
        """Open customer manager to create a new customer"""
        from .customer_manager import CustomerManagerDialog
        
        def on_customer_created(customer):
            self.load_customers()
            # Select the newly created customer
            for item in self.customer_tree.get_children():
                if self.customer_tree.item(item)['tags'][0] == customer['id']:
                    self.customer_tree.selection_set(item)
                    self.customer_tree.see(item)
                    self.selected_customer = customer
                    break
        
        customer_manager = CustomerManagerDialog(self.dialog, on_customer_created)
        customer_manager.run()
    
    def select_customer(self):
        """Select the current customer"""
        if not self.selected_customer:
            messagebox.showwarning("Warning", "Please select a customer first.")
            return
        
        if self.on_customer_selected:
            self.on_customer_selected(self.selected_customer)
        
        self.dialog.destroy()
    
    def run(self):
        """Run the dialog"""
        self.dialog.wait_window()
        return self.selected_customer 
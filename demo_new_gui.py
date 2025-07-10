import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json

# Sample data for comprehensive demo
SAMPLE_CUSTOMERS = [
    {"id": 1, "name": "Acme Industrial Corp", "email": "orders@acme.com", "phone": "555-0123", "address": "123 Industrial Ave, Detroit, MI"},
    {"id": 2, "name": "PowerGrid Solutions", "email": "procurement@powergrid.com", "phone": "555-0456", "address": "456 Electric Blvd, Chicago, IL"},
    {"id": 3, "name": "Utility Services Inc", "email": "supplies@utility.com", "phone": "555-0789", "address": "789 Service St, Houston, TX"},
    {"id": 4, "name": "New Customer", "email": "", "phone": "", "address": ""}
]

SAMPLE_PARTS_CATALOG = [
    {"pn": "PN-1001", "type": "Model", "description": "High Voltage Probe Assembly", "unit_price": 250.0, "category": "Probes", "stock": 45},
    {"pn": "PN-1002", "type": "Model", "description": "Medium Voltage Probe Assembly", "unit_price": 180.0, "category": "Probes", "stock": 32},
    {"pn": "PN-2001", "type": "Spare", "description": "Insulator Kit - Standard", "unit_price": 45.0, "category": "Insulators", "stock": 120},
    {"pn": "PN-2002", "type": "Spare", "description": "Insulator Kit - Heavy Duty", "unit_price": 65.0, "category": "Insulators", "stock": 78},
    {"pn": "PN-3001", "type": "Spare", "description": "Contact Assembly Kit", "unit_price": 35.0, "category": "Contacts", "stock": 95},
    {"pn": "PN-3002", "type": "Spare", "description": "Spring Mechanism Kit", "unit_price": 28.0, "category": "Mechanisms", "stock": 150},
    {"pn": "PN-4001", "type": "Model", "description": "Transformer Assembly", "unit_price": 420.0, "category": "Transformers", "stock": 18},
    {"pn": "PN-4002", "type": "Spare", "description": "Bushing Kit", "unit_price": 85.0, "category": "Bushings", "stock": 65},
]

class ModernQuoteGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Babbitt Quote Generator - Professional Edition")
        self.geometry("1600x1000")
        self.minsize(1400, 900)
        self.configure(bg="#f8f9fa")
        
        # Application state
        self.customers = SAMPLE_CUSTOMERS.copy()
        self.parts_catalog = SAMPLE_PARTS_CATALOG.copy()
        self.current_quote_items = []
        
        # Configure styles
        self._setup_styles()
        
        # Create main interface
        self._create_interface()
        
    def _setup_styles(self):
        """Configure modern styling"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Define color palette
        self.colors = {
            "primary": "#2563eb",
            "secondary": "#64748b", 
            "success": "#16a34a",
            "warning": "#ea580c",
            "danger": "#dc2626",
            "white": "#ffffff",
            "gray50": "#f8fafc",
            "gray100": "#f1f5f9",
            "gray200": "#e2e8f0",
            "gray300": "#cbd5e1",
            "gray400": "#94a3b8",
            "gray500": "#64748b",
            "gray600": "#475569",
            "gray700": "#334155",
            "gray800": "#1e293b",
            "gray900": "#0f172a"
        }
        
        # Configure custom styles
        self.style.configure("Header.TLabel",
                           font=("Segoe UI", 24, "bold"),
                           foreground=self.colors["gray800"],
                           background=self.colors["white"])
        
        self.style.configure("Subheader.TLabel",
                           font=("Segoe UI", 14, "bold"),
                           foreground=self.colors["gray700"],
                           background=self.colors["white"])
        
        self.style.configure("Card.TFrame",
                           background=self.colors["white"],
                           relief="solid",
                           borderwidth=1)
        
        self.style.configure("Primary.TButton",
                           background=self.colors["primary"],
                           foreground=self.colors["white"],
                           font=("Segoe UI", 10, "bold"),
                           borderwidth=0,
                           focuscolor="none",
                           padding=(12, 8))
        
        self.style.configure("Secondary.TButton", 
                           background=self.colors["gray200"],
                           foreground=self.colors["gray700"],
                           font=("Segoe UI", 10),
                           borderwidth=0,
                           focuscolor="none",
                           padding=(12, 8))
        
        self.style.configure("Success.TButton",
                           background=self.colors["success"],
                           foreground=self.colors["white"],
                           font=("Segoe UI", 10, "bold"),
                           borderwidth=0,
                           focuscolor="none",
                           padding=(12, 8))
        
        self.style.configure("Warning.TButton",
                           background=self.colors["warning"],
                           foreground=self.colors["white"],
                           font=("Segoe UI", 10, "bold"),
                           borderwidth=0,
                           focuscolor="none",
                           padding=(12, 8))
        
    def _create_interface(self):
        """Create the main single-view interface"""
        # Main container with padding
        main_container = ttk.Frame(self, padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Header section
        self._create_header(main_container)
        
        # Content area - using grid for better control
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Configure grid weights
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Top section - Customer and Quote Info
        self._create_top_section(content_frame)
        
        # Middle section - Parts Catalog and Quote Items (side by side)
        self._create_middle_section(content_frame)
        
        # Bottom section - Summary and Actions
        self._create_bottom_section(content_frame)
        
        # Status bar
        self._create_status_bar()
        
    def _create_header(self, parent):
        """Create header with title and quote info"""
        header_frame = ttk.Frame(parent, style="Card.TFrame", padding="20")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Left side - Title
        title_frame = ttk.Frame(header_frame, style="Card.TFrame")
        title_frame.pack(side="left", fill="both", expand=True)
        
        title_label = ttk.Label(title_frame, text="🏭 Babbitt Quote Generator", 
                               style="Header.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(title_frame, text="Professional Industrial Parts Quoting System",
                                  font=("Segoe UI", 12),
                                  foreground=self.colors["gray500"],
                                  background=self.colors["white"])
        subtitle_label.pack(anchor="w")
        
        # Right side - Quote metadata
        metadata_frame = ttk.Frame(header_frame, style="Card.TFrame")
        metadata_frame.pack(side="right")
        
        # Quote ID
        quote_id_frame = ttk.Frame(metadata_frame, style="Card.TFrame")
        quote_id_frame.pack(anchor="e", pady=(0, 5))
        
        ttk.Label(quote_id_frame, text="Quote ID:", font=("Segoe UI", 10, "bold"),
                 foreground=self.colors["gray600"], background=self.colors["white"]).pack(side="left")
        
        self.quote_id_var = tk.StringVar(value=f"Q{datetime.now().strftime('%Y%m%d')}-001")
        quote_id_entry = ttk.Entry(quote_id_frame, textvariable=self.quote_id_var, 
                                  width=15, font=("Segoe UI", 10, "bold"))
        quote_id_entry.pack(side="left", padx=(5, 0))
        
        # Date
        date_frame = ttk.Frame(metadata_frame, style="Card.TFrame")
        date_frame.pack(anchor="e", pady=(0, 5))
        
        ttk.Label(date_frame, text="Date:", font=("Segoe UI", 10, "bold"),
                 foreground=self.colors["gray600"], background=self.colors["white"]).pack(side="left")
        ttk.Label(date_frame, text=datetime.now().strftime("%m/%d/%Y"),
                 font=("Segoe UI", 10), foreground=self.colors["gray700"],
                 background=self.colors["white"]).pack(side="left", padx=(5, 0))
        
        # Valid until
        valid_frame = ttk.Frame(metadata_frame, style="Card.TFrame")
        valid_frame.pack(anchor="e")
        
        ttk.Label(valid_frame, text="Valid Until:", font=("Segoe UI", 10, "bold"),
                 foreground=self.colors["gray600"], background=self.colors["white"]).pack(side="left")
        
        self.valid_until_var = tk.StringVar(value=(datetime.now() + timedelta(days=30)).strftime("%m/%d/%Y"))
        valid_entry = ttk.Entry(valid_frame, textvariable=self.valid_until_var, 
                               width=12, font=("Segoe UI", 10))
        valid_entry.pack(side="left", padx=(5, 0))
        
    def _create_top_section(self, parent):
        """Create customer selection and info section"""
        top_frame = ttk.Frame(parent, style="Card.TFrame", padding="20")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Customer selection
        customer_frame = ttk.Frame(top_frame, style="Card.TFrame")
        customer_frame.pack(fill="x")
        
        ttk.Label(customer_frame, text="👤 Customer Information", 
                 style="Subheader.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Customer selection row
        selection_frame = ttk.Frame(customer_frame, style="Card.TFrame")
        selection_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(selection_frame, text="Customer:", font=("Segoe UI", 11, "bold"),
                 foreground=self.colors["gray700"], background=self.colors["white"]).pack(side="left")
        
        self.customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(selection_frame, textvariable=self.customer_var,
                                     values=[c["name"] for c in self.customers if c["name"] != "New Customer"],
                                     font=("Segoe UI", 11), width=35, state="readonly")
        customer_combo.pack(side="left", padx=(10, 20))
        customer_combo.bind("<<ComboboxSelected>>", self._on_customer_selected)
        
        ttk.Button(selection_frame, text="➕ New Customer", 
                  style="Secondary.TButton",
                  command=self._add_new_customer).pack(side="left", padx=(0, 10))
        
        ttk.Button(selection_frame, text="✏️ Edit Customer", 
                  style="Secondary.TButton",
                  command=self._edit_customer).pack(side="left")
        
        # Customer details display
        self.customer_details_frame = ttk.Frame(customer_frame, style="Card.TFrame")
        self.customer_details_frame.pack(fill="x")
        
    def _create_middle_section(self, parent):
        """Create parts catalog and quote items section"""
        # Left side - Parts Catalog
        catalog_frame = ttk.Frame(parent, style="Card.TFrame", padding="20")
        catalog_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Parts catalog header
        catalog_header = ttk.Frame(catalog_frame, style="Card.TFrame")
        catalog_header.pack(fill="x", pady=(0, 15))
        
        ttk.Label(catalog_header, text="🔧 Parts Catalog", 
                 style="Subheader.TLabel").pack(side="left")
        
        # Search and filter controls
        search_frame = ttk.Frame(catalog_frame, style="Card.TFrame")
        search_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(search_frame, text="Search:", font=("Segoe UI", 10),
                 foreground=self.colors["gray600"], background=self.colors["white"]).pack(side="left")
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                width=20, font=("Segoe UI", 10))
        search_entry.pack(side="left", padx=(5, 10))
        search_entry.bind("<KeyRelease>", self._filter_parts)
        
        ttk.Label(search_frame, text="Category:", font=("Segoe UI", 10),
                 foreground=self.colors["gray600"], background=self.colors["white"]).pack(side="left")
        
        self.category_var = tk.StringVar()
        categories = ["All"] + list(set(part["category"] for part in self.parts_catalog))
        category_combo = ttk.Combobox(search_frame, textvariable=self.category_var,
                                     values=categories, width=12, state="readonly")
        category_combo.set("All")
        category_combo.pack(side="left", padx=(5, 0))
        category_combo.bind("<<ComboboxSelected>>", self._filter_parts)
        
        # Parts table
        parts_columns = ("Part#", "Type", "Description", "Price", "Stock")
        self.parts_tree = ttk.Treeview(catalog_frame, columns=parts_columns, 
                                      show="headings", height=12)
        
        # Configure columns
        column_widths = {"Part#": 80, "Type": 60, "Description": 200, "Price": 80, "Stock": 60}
        for col in parts_columns:
            self.parts_tree.heading(col, text=col)
            self.parts_tree.column(col, width=column_widths[col], anchor="center")
        
        # Populate parts
        self._populate_parts_catalog()
        
        # Parts tree with scrollbar
        parts_scroll = ttk.Scrollbar(catalog_frame, orient="vertical", command=self.parts_tree.yview)
        self.parts_tree.configure(yscrollcommand=parts_scroll.set)
        
        parts_tree_frame = ttk.Frame(catalog_frame, style="Card.TFrame")
        parts_tree_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.parts_tree.pack(side="left", fill="both", expand=True)
        parts_scroll.pack(side="right", fill="y")
        
        # Add to quote button
        add_button_frame = ttk.Frame(catalog_frame, style="Card.TFrame")
        add_button_frame.pack(fill="x")
        
        ttk.Button(add_button_frame, text="➤ Add to Quote", 
                  style="Primary.TButton",
                  command=self._add_to_quote).pack(side="left")
        
        ttk.Button(add_button_frame, text="➕ Custom Part", 
                  style="Secondary.TButton",
                  command=self._add_custom_part).pack(side="left", padx=(10, 0))
        
        # Right side - Quote Items
        quote_frame = ttk.Frame(parent, style="Card.TFrame", padding="20")
        quote_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        # Quote items header
        quote_header = ttk.Frame(quote_frame, style="Card.TFrame")
        quote_header.pack(fill="x", pady=(0, 15))
        
        ttk.Label(quote_header, text="📋 Quote Items", 
                 style="Subheader.TLabel").pack(side="left")
        
        # Quote items count
        self.items_count_var = tk.StringVar(value="0 items")
        ttk.Label(quote_header, textvariable=self.items_count_var,
                 font=("Segoe UI", 10), foreground=self.colors["gray500"],
                 background=self.colors["white"]).pack(side="right")
        
        # Quote items table
        quote_columns = ("Part#", "Description", "Qty", "Unit Price", "Total")
        self.quote_tree = ttk.Treeview(quote_frame, columns=quote_columns, 
                                      show="headings", height=12)
        
        # Configure quote columns
        quote_widths = {"Part#": 80, "Description": 180, "Qty": 50, "Unit Price": 80, "Total": 80}
        for col in quote_columns:
            self.quote_tree.heading(col, text=col)
            self.quote_tree.column(col, width=quote_widths[col], anchor="center")
        
        # Quote tree with scrollbar
        quote_scroll = ttk.Scrollbar(quote_frame, orient="vertical", command=self.quote_tree.yview)
        self.quote_tree.configure(yscrollcommand=quote_scroll.set)
        
        quote_tree_frame = ttk.Frame(quote_frame, style="Card.TFrame")
        quote_tree_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.quote_tree.pack(side="left", fill="both", expand=True)
        quote_scroll.pack(side="right", fill="y")
        
        # Quote controls
        controls_frame = ttk.Frame(quote_frame, style="Card.TFrame")
        controls_frame.pack(fill="x")
        
        ttk.Button(controls_frame, text="✏️ Edit Qty", 
                  style="Secondary.TButton",
                  command=self._edit_quantity).pack(side="left")
        
        ttk.Button(controls_frame, text="🗑️ Remove", 
                  style="Secondary.TButton",
                  command=self._remove_item).pack(side="left", padx=(10, 0))
        
        ttk.Button(controls_frame, text="🔄 Clear All", 
                  style="Secondary.TButton",
                  command=self._clear_quote).pack(side="left", padx=(10, 0))
        
    def _create_bottom_section(self, parent):
        """Create summary and actions section"""
        bottom_frame = ttk.Frame(parent, style="Card.TFrame", padding="20")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        # Left side - Summary
        summary_frame = ttk.Frame(bottom_frame, style="Card.TFrame")
        summary_frame.pack(side="left", fill="both", expand=True)
        
        ttk.Label(summary_frame, text="💰 Quote Summary", 
                 style="Subheader.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Summary details
        summary_details = ttk.Frame(summary_frame, style="Card.TFrame")
        summary_details.pack(fill="x")
        
        # Initialize summary variables
        self.subtotal_var = tk.StringVar(value="$0.00")
        self.tax_var = tk.StringVar(value="$0.00") 
        self.total_var = tk.StringVar(value="$0.00")
        
        # Summary rows
        for i, (label, var, weight) in enumerate([
            ("Subtotal:", self.subtotal_var, "normal"),
            ("Tax (8.5%):", self.tax_var, "normal"),
            ("Total:", self.total_var, "bold")
        ]):
            row_frame = ttk.Frame(summary_details, style="Card.TFrame")
            row_frame.pack(fill="x", pady=2)
            
            ttk.Label(row_frame, text=label, font=("Segoe UI", 12, weight),
                     foreground=self.colors["gray700"], background=self.colors["white"]).pack(side="left")
            
            font_size = 14 if weight == "bold" else 12
            ttk.Label(row_frame, textvariable=var, font=("Segoe UI", font_size, weight),
                     foreground=self.colors["gray800"], background=self.colors["white"]).pack(side="right")
        
        # Right side - Actions
        actions_frame = ttk.Frame(bottom_frame, style="Card.TFrame")
        actions_frame.pack(side="right", padx=(40, 0))
        
        ttk.Label(actions_frame, text="🚀 Actions", 
                 style="Subheader.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Action buttons in a grid
        buttons_grid = ttk.Frame(actions_frame, style="Card.TFrame")
        buttons_grid.pack()
        
        # Row 1
        ttk.Button(buttons_grid, text="💾 Save Draft", 
                  style="Secondary.TButton",
                  command=self._save_draft).grid(row=0, column=0, padx=(0, 10), pady=(0, 10))
        
        ttk.Button(buttons_grid, text="👁️ Preview", 
                  style="Secondary.TButton",
                  command=self._preview_quote).grid(row=0, column=1, pady=(0, 10))
        
        # Row 2
        ttk.Button(buttons_grid, text="📧 Send Quote", 
                  style="Success.TButton",
                  command=self._send_quote).grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
        
        ttk.Button(buttons_grid, text="🖨️ Print", 
                  style="Secondary.TButton",
                  command=self._print_quote).grid(row=1, column=1, pady=(0, 10))
        
        # Row 3
        ttk.Button(buttons_grid, text="📄 Export PDF", 
                  style="Warning.TButton",
                  command=self._export_pdf).grid(row=2, column=0, padx=(0, 10))
        
        ttk.Button(buttons_grid, text="🔄 New Quote", 
                  style="Primary.TButton",
                  command=self._new_quote).grid(row=2, column=1)
        
    def _create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self, style="Card.TFrame")
        self.status_frame.pack(fill="x", side="bottom", padx=20, pady=(10, 20))
        
        self.status_var = tk.StringVar(value="Ready - Select customer to begin")
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var,
                                font=("Segoe UI", 10), foreground=self.colors["gray600"],
                                background=self.colors["white"])
        status_label.pack(side="left", padx=10, pady=5)
        
        # Connection status
        connection_label = ttk.Label(self.status_frame, text="🟢 System Ready",
                                   font=("Segoe UI", 10), foreground=self.colors["success"],
                                   background=self.colors["white"])
        connection_label.pack(side="right", padx=10, pady=5)
        
    # Event handlers and utility methods
    def _on_customer_selected(self, event):
        """Handle customer selection"""
        selected_customer = self.customer_var.get()
        customer_data = next((c for c in self.customers if c["name"] == selected_customer), None)
        
        # Clear previous customer details
        for widget in self.customer_details_frame.winfo_children():
            widget.destroy()
        
        if customer_data:
            details_grid = ttk.Frame(self.customer_details_frame, style="Card.TFrame")
            details_grid.pack(fill="x", pady=(10, 0))
            
            # Customer details in a nice layout
            ttk.Label(details_grid, text="📧", font=("Segoe UI", 12)).grid(row=0, column=0, padx=(0, 5))
            ttk.Label(details_grid, text=customer_data["email"], font=("Segoe UI", 11),
                     foreground=self.colors["gray700"], background=self.colors["white"]).grid(row=0, column=1, sticky="w")
            
            ttk.Label(details_grid, text="📞", font=("Segoe UI", 12)).grid(row=0, column=2, padx=(20, 5))
            ttk.Label(details_grid, text=customer_data["phone"], font=("Segoe UI", 11),
                     foreground=self.colors["gray700"], background=self.colors["white"]).grid(row=0, column=3, sticky="w")
            
            ttk.Label(details_grid, text="📍", font=("Segoe UI", 12)).grid(row=1, column=0, padx=(0, 5), pady=(5, 0))
            ttk.Label(details_grid, text=customer_data["address"], font=("Segoe UI", 11),
                     foreground=self.colors["gray700"], background=self.colors["white"]).grid(row=1, column=1, columnspan=3, sticky="w", pady=(5, 0))
            
            self.status_var.set(f"Customer selected: {selected_customer}")
    
    def _populate_parts_catalog(self):
        """Populate the parts catalog tree"""
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
            
        for part in self.parts_catalog:
            self.parts_tree.insert("", "end", values=(
                part["pn"], part["type"], part["description"], 
                f"${part['unit_price']:.2f}", part["stock"]
            ))
    
    def _filter_parts(self, event=None):
        """Filter parts based on search and category"""
        search_text = self.search_var.get().lower()
        category = self.category_var.get()
        
        # Clear tree
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        # Filter and populate
        for part in self.parts_catalog:
            # Check category filter
            if category != "All" and part["category"] != category:
                continue
                
            # Check search filter
            if search_text and not any(search_text in str(part[key]).lower() 
                                     for key in ["pn", "description", "type"]):
                continue
                
            self.parts_tree.insert("", "end", values=(
                part["pn"], part["type"], part["description"], 
                f"${part['unit_price']:.2f}", part["stock"]
            ))
    
    def _add_to_quote(self):
        """Add selected part to quote"""
        selection = self.parts_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part to add to the quote.")
            return
        
        item = self.parts_tree.item(selection[0])
        values = item["values"]
        
        # Get quantity
        qty = simpledialog.askinteger("Quantity", f"Enter quantity for {values[0]}:", 
                                     minvalue=1, initialvalue=1)
        if not qty:
            return
        
        # Find the full part data
        part_data = next((p for p in self.parts_catalog if p["pn"] == values[0]), None)
        if not part_data:
            return
        
        # Add to quote
        quote_item = {
            "pn": part_data["pn"],
            "description": part_data["description"],
            "qty": qty,
            "unit_price": part_data["unit_price"],
            "total": qty * part_data["unit_price"]
        }
        
        self.current_quote_items.append(quote_item)
        self._update_quote_display()
        
        self.status_var.set(f"Added {qty}x {part_data['pn']} to quote")
    
    def _update_quote_display(self):
        """Update the quote items display and totals"""
        # Clear quote tree
        for item in self.quote_tree.get_children():
            self.quote_tree.delete(item)
        
        # Populate quote tree
        subtotal = 0
        for item in self.current_quote_items:
            self.quote_tree.insert("", "end", values=(
                item["pn"], item["description"], item["qty"],
                f"${item['unit_price']:.2f}", f"${item['total']:.2f}"
            ))
            subtotal += item["total"]
        
        # Update totals
        tax = subtotal * 0.085
        total = subtotal + tax
        
        self.subtotal_var.set(f"${subtotal:.2f}")
        self.tax_var.set(f"${tax:.2f}")
        self.total_var.set(f"${total:.2f}")
        
        # Update items count
        self.items_count_var.set(f"{len(self.current_quote_items)} items")
    
    def _edit_quantity(self):
        """Edit quantity of selected quote item"""
        selection = self.quote_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to edit.")
            return
        
        item_idx = self.quote_tree.index(selection[0])
        current_item = self.current_quote_items[item_idx]
        
        new_qty = simpledialog.askinteger("Edit Quantity", 
                                         f"Enter new quantity for {current_item['pn']}:",
                                         minvalue=1, initialvalue=current_item["qty"])
        if new_qty:
            current_item["qty"] = new_qty
            current_item["total"] = new_qty * current_item["unit_price"]
            self._update_quote_display()
            self.status_var.set(f"Updated quantity for {current_item['pn']}")
    
    def _remove_item(self):
        """Remove selected item from quote"""
        selection = self.quote_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return
        
        item_idx = self.quote_tree.index(selection[0])
        removed_item = self.current_quote_items.pop(item_idx)
        self._update_quote_display()
        self.status_var.set(f"Removed {removed_item['pn']} from quote")
    
    def _clear_quote(self):
        """Clear all quote items"""
        if self.current_quote_items:
            if messagebox.askyesno("Clear Quote", "Are you sure you want to clear all quote items?"):
                self.current_quote_items.clear()
                self._update_quote_display()
                self.status_var.set("Quote cleared")
    
    def _add_new_customer(self):
        """Add new customer dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Add New Customer")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["white"])
        
        # Center the dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Dialog content
        content_frame = ttk.Frame(dialog, style="Card.TFrame", padding="30")
        content_frame.pack(fill="both", expand=True)
        
        ttk.Label(content_frame, text="👤 Add New Customer", 
                 style="Subheader.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Form fields
        fields = [
            ("Company Name:", "name"),
            ("Email Address:", "email"),
            ("Phone Number:", "phone"),
            ("Address:", "address")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(content_frame, text=label, font=("Segoe UI", 11, "bold"),
                     foreground=self.colors["gray700"], background=self.colors["white"]).pack(anchor="w", pady=(10, 5))
            
            if key == "address":
                entry = tk.Text(content_frame, height=3, width=40, font=("Segoe UI", 11))
            else:
                entry = ttk.Entry(content_frame, width=40, font=("Segoe UI", 11))
            
            entry.pack(anchor="w", pady=(0, 10))
            entries[key] = entry
        
        # Buttons
        button_frame = ttk.Frame(content_frame, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(20, 0))
        
        def save_customer():
            new_customer = {
                "id": len(self.customers) + 1,
                "name": entries["name"].get(),
                "email": entries["email"].get(),
                "phone": entries["phone"].get(),
                "address": entries["address"].get("1.0", tk.END).strip() if hasattr(entries["address"], "get") else entries["address"].get()
            }
            
            if not new_customer["name"]:
                messagebox.showerror("Error", "Company name is required.")
                return
            
            self.customers.append(new_customer)
            
            # Update customer combobox
            customer_combo = None
            for widget in self.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ttk.Combobox):
                                    customer_combo = grandchild
                                    break
            
            if customer_combo:
                customer_combo.configure(values=[c["name"] for c in self.customers if c["name"] != "New Customer"])
                customer_combo.set(new_customer["name"])
                self._on_customer_selected(None)
            
            dialog.destroy()
            self.status_var.set(f"Added new customer: {new_customer['name']}")
        
        ttk.Button(button_frame, text="💾 Save Customer", 
                  style="Primary.TButton", command=save_customer).pack(side="right")
        ttk.Button(button_frame, text="❌ Cancel", 
                  style="Secondary.TButton", command=dialog.destroy).pack(side="right", padx=(0, 10))
    
    def _edit_customer(self):
        """Edit selected customer"""
        if not self.customer_var.get():
            messagebox.showwarning("No Customer", "Please select a customer to edit.")
            return
        messagebox.showinfo("Edit Customer", "Customer editing functionality would be implemented here.")
    
    def _add_custom_part(self):
        """Add custom part dialog"""
        messagebox.showinfo("Custom Part", "Custom part creation dialog would be implemented here.")
    
    def _save_draft(self):
        """Save quote as draft"""
        if not self.current_quote_items:
            messagebox.showwarning("Empty Quote", "Please add items to the quote before saving.")
            return
        messagebox.showinfo("Draft Saved", f"Quote {self.quote_id_var.get()} saved as draft.")
        self.status_var.set("Quote saved as draft")
    
    def _preview_quote(self):
        """Preview quote"""
        if not self.current_quote_items:
            messagebox.showwarning("Empty Quote", "Please add items to the quote before previewing.")
            return
        messagebox.showinfo("Preview", "Quote preview window would open here.")
    
    def _send_quote(self):
        """Send quote to customer"""
        if not self.customer_var.get():
            messagebox.showwarning("No Customer", "Please select a customer before sending.")
            return
        if not self.current_quote_items:
            messagebox.showwarning("Empty Quote", "Please add items to the quote before sending.")
            return
        messagebox.showinfo("Quote Sent", f"Quote sent to {self.customer_var.get()}!")
        self.status_var.set("Quote sent successfully")
    
    def _print_quote(self):
        """Print quote"""
        if not self.current_quote_items:
            messagebox.showwarning("Empty Quote", "Please add items to the quote before printing.")
            return
        messagebox.showinfo("Print", "Quote would be sent to printer.")
    
    def _export_pdf(self):
        """Export quote as PDF"""
        if not self.current_quote_items:
            messagebox.showwarning("Empty Quote", "Please add items to the quote before exporting.")
            return
        messagebox.showinfo("Export PDF", "Quote would be exported as PDF.")
    
    def _new_quote(self):
        """Start new quote"""
        if self.current_quote_items:
            if messagebox.askyesno("New Quote", "This will clear the current quote. Continue?"):
                self.current_quote_items.clear()
                self.customer_var.set("")
                self.quote_id_var.set(f"Q{datetime.now().strftime('%Y%m%d')}-{len(self.current_quote_items)+1:03d}")
                self._update_quote_display()
                self._on_customer_selected(None)
                self.status_var.set("New quote started")

if __name__ == "__main__":
    app = ModernQuoteGenerator()
    app.mainloop() 
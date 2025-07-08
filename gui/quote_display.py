"""
Quote Display Widget for Babbitt Quote Generator
Displays parsed part number information and pricing details
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional

class QuoteDisplayWidget:
    """Widget for displaying quote information"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_data = None
        self.create_widgets()
        self.setup_layout()
    
    def create_widgets(self):
        """Create the display widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.parent)
        
        # Create notebook for tabbed display
        self.notebook = ttk.Notebook(self.main_frame)
        
        # Part Details tab
        self.part_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.part_frame, text="Part Details")
        self.create_part_details_tab()
        
        # Pricing tab
        self.pricing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pricing_frame, text="Pricing")
        self.create_pricing_tab()
        
        # Specifications tab
        self.specs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.specs_frame, text="Specifications")
        self.create_specifications_tab()
        
        # Validation tab
        self.validation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.validation_frame, text="Validation")
        self.create_validation_tab()
    
    def create_part_details_tab(self):
        """Create part details display"""
        # Scrollable frame
        canvas = tk.Canvas(self.part_frame)
        scrollbar = ttk.Scrollbar(self.part_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main info frame
        info_frame = ttk.LabelFrame(scrollable_frame, text="Part Number Information", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Part number display
        self.part_number_label = ttk.Label(info_frame, text="Part Number: ", font=("Consolas", 12, "bold"))
        self.part_number_label.pack(anchor=tk.W)
        
        # Component breakdown
        components_frame = ttk.LabelFrame(scrollable_frame, text="Component Breakdown", padding="10")
        components_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create labels for each component
        self.model_label = ttk.Label(components_frame, text="Model: ")
        self.model_label.pack(anchor=tk.W)
        
        self.voltage_label = ttk.Label(components_frame, text="Voltage: ")
        self.voltage_label.pack(anchor=tk.W)
        
        self.material_label = ttk.Label(components_frame, text="Probe Material: ")
        self.material_label.pack(anchor=tk.W)
        
        self.length_label = ttk.Label(components_frame, text="Probe Length: ")
        self.length_label.pack(anchor=tk.W)
        
        self.connection_label = ttk.Label(components_frame, text="Process Connection: ")
        self.connection_label.pack(anchor=tk.W)
        
        self.insulator_label = ttk.Label(components_frame, text="Insulator: ")
        self.insulator_label.pack(anchor=tk.W)
        
        # Options frame
        options_frame = ttk.LabelFrame(scrollable_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Options listbox
        self.options_listbox = tk.Listbox(options_frame, height=4)
        self.options_listbox.pack(fill=tk.X)
        
        # Pack scrollable elements
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_pricing_tab(self):
        """Create pricing display"""
        # Scrollable frame
        canvas = tk.Canvas(self.pricing_frame)
        scrollbar = ttk.Scrollbar(self.pricing_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Price breakdown frame
        breakdown_frame = ttk.LabelFrame(scrollable_frame, text="Price Breakdown", padding="10")
        breakdown_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Price components
        self.base_price_label = ttk.Label(breakdown_frame, text="Base Price: $0.00")
        self.base_price_label.pack(anchor=tk.W)
        
        self.length_cost_label = ttk.Label(breakdown_frame, text="Length Cost: $0.00")
        self.length_cost_label.pack(anchor=tk.W)
        
        self.length_surcharge_label = ttk.Label(breakdown_frame, text="Length Surcharge: $0.00")
        self.length_surcharge_label.pack(anchor=tk.W)
        
        self.option_cost_label = ttk.Label(breakdown_frame, text="Option Cost: $0.00")
        self.option_cost_label.pack(anchor=tk.W)
        
        self.insulator_cost_label = ttk.Label(breakdown_frame, text="Insulator Cost: $0.00")
        self.insulator_cost_label.pack(anchor=tk.W)
        
        # Separator
        separator = ttk.Separator(breakdown_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=5)
        
        # Total price
        self.total_price_label = ttk.Label(breakdown_frame, text="Total Price: $0.00", font=("Arial", 12, "bold"))
        self.total_price_label.pack(anchor=tk.W)
        
        # Detailed breakdown
        details_frame = ttk.LabelFrame(scrollable_frame, text="Detailed Breakdown", padding="10")
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Treeview for detailed breakdown
        self.breakdown_tree = ttk.Treeview(details_frame, columns=("Description", "Cost"), show="tree headings", height=8)
        self.breakdown_tree.heading("#0", text="Item")
        self.breakdown_tree.heading("Description", text="Description")
        self.breakdown_tree.heading("Cost", text="Cost")
        
        self.breakdown_tree.column("#0", width=150)
        self.breakdown_tree.column("Description", width=300)
        self.breakdown_tree.column("Cost", width=100)
        
        self.breakdown_tree.pack(fill=tk.X)
        
        # Pack scrollable elements
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_specifications_tab(self):
        """Create specifications display"""
        # Scrollable frame
        canvas = tk.Canvas(self.specs_frame)
        scrollbar = ttk.Scrollbar(self.specs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Technical specifications
        tech_frame = ttk.LabelFrame(scrollable_frame, text="Technical Specifications", padding="10")
        tech_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.housing_label = ttk.Label(tech_frame, text="Housing: ")
        self.housing_label.pack(anchor=tk.W)
        
        self.output_label = ttk.Label(tech_frame, text="Output: ")
        self.output_label.pack(anchor=tk.W)
        
        self.max_temp_label = ttk.Label(tech_frame, text="Max Temperature: ")
        self.max_temp_label.pack(anchor=tk.W)
        
        self.max_pressure_label = ttk.Label(tech_frame, text="Max Pressure: ")
        self.max_pressure_label.pack(anchor=tk.W)
        
        # Application notes
        notes_frame = ttk.LabelFrame(scrollable_frame, text="Application Notes", padding="10")
        notes_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.notes_text = tk.Text(notes_frame, height=6, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X)
        
        # Pack scrollable elements
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_validation_tab(self):
        """Create validation display"""
        # Scrollable frame
        canvas = tk.Canvas(self.validation_frame)
        scrollbar = ttk.Scrollbar(self.validation_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Validation status
        status_frame = ttk.LabelFrame(scrollable_frame, text="Validation Status", padding="10")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.validation_status_label = ttk.Label(status_frame, text="Status: Not validated", font=("Arial", 10, "bold"))
        self.validation_status_label.pack(anchor=tk.W)
        
        # Errors
        errors_frame = ttk.LabelFrame(scrollable_frame, text="Errors", padding="10")
        errors_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.errors_listbox = tk.Listbox(errors_frame, height=4, fg="red")
        self.errors_listbox.pack(fill=tk.X)
        
        # Warnings
        warnings_frame = ttk.LabelFrame(scrollable_frame, text="Warnings", padding="10")
        warnings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.warnings_listbox = tk.Listbox(warnings_frame, height=4, fg="orange")
        self.warnings_listbox.pack(fill=tk.X)
        
        # Pack scrollable elements
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_layout(self):
        """Setup widget layout"""
        self.notebook.pack(fill=tk.BOTH, expand=True)
    
    def grid(self, **kwargs):
        """Grid the main frame"""
        self.main_frame.grid(**kwargs)
    
    def pack(self, **kwargs):
        """Pack the main frame"""
        self.main_frame.pack(**kwargs)
    
    def update_display(self, quote_data: Dict[str, Any]):
        """Update the display with new quote data"""
        self.current_data = quote_data
        
        # Update part details
        self.update_part_details()
        
        # Update pricing
        self.update_pricing()
        
        # Update specifications
        self.update_specifications()
        
        # Update validation
        self.update_validation()
    
    def update_part_details(self):
        """Update part details tab"""
        if not self.current_data:
            return
        
        # Update part number
        part_number = self.current_data.get('part_number', '')
        self.part_number_label.config(text=f"Part Number: {part_number}")
        
        # Update components
        self.model_label.config(text=f"Model: {self.current_data.get('model', 'N/A')}")
        self.voltage_label.config(text=f"Voltage: {self.current_data.get('voltage', 'N/A')}")
        self.material_label.config(text=f"Probe Material: {self.current_data.get('probe_material', 'N/A')}")
        self.length_label.config(text=f"Probe Length: {self.current_data.get('probe_length', 'N/A')}\"")
        self.connection_label.config(text=f"Process Connection: {self.current_data.get('process_connection', 'N/A')}")
        self.insulator_label.config(text=f"Insulator: {self.current_data.get('insulator', 'N/A')}")
        
        # Update options
        self.options_listbox.delete(0, tk.END)
        options = self.current_data.get('options', [])
        if options:
            for option in options:
                self.options_listbox.insert(tk.END, option)
        else:
            self.options_listbox.insert(tk.END, "No options selected")
    
    def update_pricing(self):
        """Update pricing tab"""
        if not self.current_data:
            return
        
        # Update price components
        base_price = self.current_data.get('base_price', 0)
        length_cost = self.current_data.get('length_cost', 0)
        length_surcharge = self.current_data.get('length_surcharge', 0)
        option_cost = self.current_data.get('option_cost', 0)
        insulator_cost = self.current_data.get('insulator_cost', 0)
        total_price = self.current_data.get('total_price', 0)
        
        self.base_price_label.config(text=f"Base Price: ${base_price:.2f}")
        self.length_cost_label.config(text=f"Length Cost: ${length_cost:.2f}")
        self.length_surcharge_label.config(text=f"Length Surcharge: ${length_surcharge:.2f}")
        self.option_cost_label.config(text=f"Option Cost: ${option_cost:.2f}")
        self.insulator_cost_label.config(text=f"Insulator Cost: ${insulator_cost:.2f}")
        self.total_price_label.config(text=f"Total Price: ${total_price:.2f}")
        
        # Update detailed breakdown
        self.breakdown_tree.delete(*self.breakdown_tree.get_children())
        
        # Add pricing components
        if base_price > 0:
            self.breakdown_tree.insert("", tk.END, text="Base Price", values=(f"Model {self.current_data.get('model', '')}", f"${base_price:.2f}"))
        
        if length_cost > 0:
            length = self.current_data.get('probe_length', 0)
            self.breakdown_tree.insert("", tk.END, text="Length Cost", values=(f"Additional length beyond base ({length}\")", f"${length_cost:.2f}"))
        
        if length_surcharge > 0:
            self.breakdown_tree.insert("", tk.END, text="Length Surcharge", values=("Non-standard length surcharge", f"${length_surcharge:.2f}"))
        
        if option_cost > 0:
            options = self.current_data.get('options', [])
            option_str = ", ".join(options) if options else "Various options"
            self.breakdown_tree.insert("", tk.END, text="Options", values=(option_str, f"${option_cost:.2f}"))
        
        if insulator_cost > 0:
            insulator = self.current_data.get('insulator', 'N/A')
            self.breakdown_tree.insert("", tk.END, text="Insulator", values=(f"Insulator: {insulator}", f"${insulator_cost:.2f}"))
    
    def update_specifications(self):
        """Update specifications tab"""
        if not self.current_data:
            return
        
        # Update technical specifications
        self.housing_label.config(text=f"Housing: {self.current_data.get('housing', 'N/A')}")
        self.output_label.config(text=f"Output: {self.current_data.get('output', 'N/A')}")
        self.max_temp_label.config(text=f"Max Temperature: {self.current_data.get('max_temperature', 'N/A')}")
        self.max_pressure_label.config(text=f"Max Pressure: {self.current_data.get('max_pressure', 'N/A')}")
        
        # Update application notes
        self.notes_text.delete(1.0, tk.END)
        notes = self.current_data.get('application_notes', 'No specific application notes available.')
        self.notes_text.insert(1.0, notes)
        self.notes_text.config(state=tk.DISABLED)
    
    def update_validation(self):
        """Update validation tab"""
        if not self.current_data:
            return
        
        # Get validation results
        errors = self.current_data.get('errors', [])
        warnings = self.current_data.get('warnings', [])
        
        # Update status
        if errors:
            self.validation_status_label.config(text="Status: Errors found")
        elif warnings:
            self.validation_status_label.config(text="Status: Warnings found")
        else:
            self.validation_status_label.config(text="Status: Valid")
        
        # Update errors
        self.errors_listbox.delete(0, tk.END)
        if errors:
            for error in errors:
                self.errors_listbox.insert(tk.END, error)
        else:
            self.errors_listbox.insert(tk.END, "No errors found")
        
        # Update warnings
        self.warnings_listbox.delete(0, tk.END)
        if warnings:
            for warning in warnings:
                self.warnings_listbox.insert(tk.END, warning)
        else:
            self.warnings_listbox.insert(tk.END, "No warnings found")
    
    def clear_display(self):
        """Clear all displayed data"""
        self.current_data = None
        
        # Clear part details
        self.part_number_label.config(text="Part Number: ")
        self.model_label.config(text="Model: ")
        self.voltage_label.config(text="Voltage: ")
        self.material_label.config(text="Probe Material: ")
        self.length_label.config(text="Probe Length: ")
        self.connection_label.config(text="Process Connection: ")
        self.insulator_label.config(text="Insulator: ")
        
        self.options_listbox.delete(0, tk.END)
        
        # Clear pricing
        self.base_price_label.config(text="Base Price: $0.00")
        self.length_cost_label.config(text="Length Cost: $0.00")
        self.length_surcharge_label.config(text="Length Surcharge: $0.00")
        self.option_cost_label.config(text="Option Cost: $0.00")
        self.insulator_cost_label.config(text="Insulator Cost: $0.00")
        self.total_price_label.config(text="Total Price: $0.00")
        
        self.breakdown_tree.delete(*self.breakdown_tree.get_children())
        
        # Clear specifications
        self.housing_label.config(text="Housing: ")
        self.output_label.config(text="Output: ")
        self.max_temp_label.config(text="Max Temperature: ")
        self.max_pressure_label.config(text="Max Pressure: ")
        
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.config(state=tk.DISABLED)
        
        # Clear validation
        self.validation_status_label.config(text="Status: Not validated")
        self.errors_listbox.delete(0, tk.END)
        self.warnings_listbox.delete(0, tk.END) 
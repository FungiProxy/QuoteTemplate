"""
Main Application Window for Babbitt Quote Generator
Provides the primary user interface for the application
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any, Union
import sys
import os
import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, 
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, SAMPLE_PART_NUMBERS,
    ERROR_MESSAGES, SUCCESS_MESSAGES
)
from core.part_parser import PartNumberParser
from core.quote_generator import QuoteGenerator
from core.spare_parts_manager import SparePartsManager

from .dialogs import AboutDialog, SettingsDialog, ExportDialog, ShortcutManagerDialog

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.parser = PartNumberParser()
        self.quote_generator = QuoteGenerator()
        self.spare_parts_manager = SparePartsManager()
        self.current_quote_data = None
        self.spare_parts_list = []  # List to store added spare parts
        self.quote_items = []  # List to store all quote items (main parts + spare parts)
        self.current_quote_number = None  # Track current quote number
        self.selected_employee_info = None  # Store selected employee for template use
        
        # Import database manager for quote functionality
        from database.db_manager import DatabaseManager
        self.db_manager = DatabaseManager()
        
        self.setup_window()
        self.create_menu()
        self.create_widgets()
        self.setup_layout()
        self.setup_bindings()
        
    def setup_window(self):
        """Configure main window properties"""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
        # Set window icon (if available)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  # Ignore if icon not found
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Quote", command=self.new_quote, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Quote", command=self.open_quote, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Quote", command=self.save_quote, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Export to Word", command=self.export_quote, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Part Number", command=self.clear_part_number)
        edit_menu.add_command(label="Clear Results", command=self.clear_results)
        edit_menu.add_separator()
        edit_menu.add_command(label="Settings", command=self.show_settings)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Employee Management", command=self.show_employee_manager)
        tools_menu.add_separator()
        tools_menu.add_command(label="Validate Database", command=self.validate_database)
        tools_menu.add_command(label="Sample Part Numbers", command=self.show_samples)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="wens")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Quote summary area will be expandable
        
        # Customer Information section (TOP)
        customer_frame = ttk.LabelFrame(main_frame, text="Customer Information", padding="10")
        customer_frame.grid(row=0, column=0, sticky="we", pady=(0, 10))
        customer_frame.columnconfigure(1, weight=1)
        customer_frame.columnconfigure(3, weight=1)
        
        # Row 1: Company and Contact Person
        ttk.Label(customer_frame, text="Company:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.company_var = tk.StringVar(value="")
        company_entry = ttk.Entry(customer_frame, textvariable=self.company_var)
        company_entry.grid(row=0, column=1, sticky="we", padx=(0, 20))
        
        ttk.Label(customer_frame, text="Contact Person:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.contact_person_var = tk.StringVar(value="")
        contact_entry = ttk.Entry(customer_frame, textvariable=self.contact_person_var)
        contact_entry.grid(row=0, column=3, sticky="we")
        
        # Row 2: Phone and Email
        ttk.Label(customer_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.phone_var = tk.StringVar(value="")
        phone_entry = ttk.Entry(customer_frame, textvariable=self.phone_var)
        phone_entry.grid(row=1, column=1, sticky="we", padx=(0, 20), pady=(5, 0))
        
        ttk.Label(customer_frame, text="Email:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.email_var = tk.StringVar(value="")
        email_entry = ttk.Entry(customer_frame, textvariable=self.email_var)
        email_entry.grid(row=1, column=3, sticky="we", pady=(5, 0))
        
        # Row 3: Initials for quote numbering
        ttk.Label(customer_frame, text="Your Initials:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.initials_var = tk.StringVar(value="")
        self.initials_entry = ttk.Entry(customer_frame, textvariable=self.initials_var, width=5)
        self.initials_entry.grid(row=2, column=1, sticky=tk.W, pady=(5, 0))
        
        # Add validation for uppercase initials
        def uppercase_initials(*args):
            current = self.initials_var.get()
            if current != current.upper():
                self.initials_var.set(current.upper())
        
        self.initials_var.trace('w', uppercase_initials)
        
        # Part Number Input section
        input_frame = ttk.LabelFrame(main_frame, text="Part Number Input", padding="10")
        input_frame.grid(row=1, column=0, sticky="we", pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Part number entry (row 1)
        ttk.Label(input_frame, text="Part Number:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.part_number_var = tk.StringVar()
        self.part_number_entry = ttk.Entry(input_frame, textvariable=self.part_number_var, font=("Consolas", 12), width=50)
        self.part_number_entry.grid(row=0, column=1, sticky="we", columnspan=4, padx=(0, 10))
        
        # Quantity and buttons (row 2)
        ttk.Label(input_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.main_qty_var = tk.StringVar(value="1")
        main_qty_entry = ttk.Entry(input_frame, textvariable=self.main_qty_var, width=10)
        main_qty_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(0, 20))
        
        self.parse_button = ttk.Button(input_frame, text="Parse & Price", command=self.parse_part_number)
        self.parse_button.grid(row=1, column=2, padx=(0, 10), pady=(10, 0))
        
        self.add_to_quote_button = ttk.Button(input_frame, text="Add to Quote", command=self.add_main_part_to_quote)
        self.add_to_quote_button.grid(row=1, column=3, padx=(0, 10), pady=(10, 0))
        
        # Custom Shortcuts button
        self.shortcuts_button = ttk.Button(input_frame, text="Custom Shortcuts", command=self.show_shortcut_manager)
        self.shortcuts_button.grid(row=1, column=4, pady=(10, 0))
        
        # Spare Parts section (same layout as part number section)
        spare_frame = ttk.LabelFrame(main_frame, text="Spare Parts", padding="10")
        spare_frame.grid(row=2, column=0, sticky="we", pady=(0, 10))
        spare_frame.columnconfigure(1, weight=1)
        
        # Spare parts entry (row 1)
        ttk.Label(spare_frame, text="Spare Part:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.spare_part_var = tk.StringVar()
        self.spare_part_entry = ttk.Entry(spare_frame, textvariable=self.spare_part_var, font=("Consolas", 12), width=50)
        self.spare_part_entry.grid(row=0, column=1, sticky="we", columnspan=4, padx=(0, 10))
        
        # Quantity and buttons (row 2)
        ttk.Label(spare_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.spare_qty_var = tk.StringVar(value="1")
        spare_qty_entry = ttk.Entry(spare_frame, textvariable=self.spare_qty_var, width=10)
        spare_qty_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(0, 20))
        
        self.parse_spare_button = ttk.Button(spare_frame, text="Parse & Price", command=self.parse_spare_part)
        self.parse_spare_button.grid(row=1, column=2, padx=(0, 10), pady=(10, 0))
        
        self.add_spare_button = ttk.Button(spare_frame, text="Add to Quote", command=self.add_spare_part)
        self.add_spare_button.grid(row=1, column=3, padx=(0, 10), pady=(10, 0))
        
        # Common spare parts button
        self.common_spare_button = ttk.Button(spare_frame, text="Common P/N", command=self.show_spare_parts_help)
        self.common_spare_button.grid(row=1, column=4, pady=(10, 0))
        

        
        # Quote Summary section (NEW)
        quote_summary_frame = ttk.LabelFrame(main_frame, text="Quote Summary", padding="10")
        quote_summary_frame.grid(row=3, column=0, sticky="wens", pady=(0, 10))
        quote_summary_frame.columnconfigure(0, weight=1)
        quote_summary_frame.rowconfigure(0, weight=1)
        
        # Quote items treeview
        columns = ("Type", "Part Number", "Description", "Qty", "Unit Price", "Total Price")
        self.quote_tree = ttk.Treeview(quote_summary_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.quote_tree.heading("Type", text="Type")
        self.quote_tree.heading("Part Number", text="Part Number")
        self.quote_tree.heading("Description", text="Description")
        self.quote_tree.heading("Qty", text="Qty")
        self.quote_tree.heading("Unit Price", text="Unit Price")
        self.quote_tree.heading("Total Price", text="Total Price")
        
        self.quote_tree.column("Type", width=80)
        self.quote_tree.column("Part Number", width=200)
        self.quote_tree.column("Description", width=250)
        self.quote_tree.column("Qty", width=50)
        self.quote_tree.column("Unit Price", width=100)
        self.quote_tree.column("Total Price", width=100)
        
        # Scrollbar for quote summary
        quote_scrollbar = ttk.Scrollbar(quote_summary_frame, orient=tk.VERTICAL, command=self.quote_tree.yview)
        self.quote_tree.configure(yscrollcommand=quote_scrollbar.set)
        
        # Add right-click context menu to main quote tree
        def show_main_tree_details(event):
            """Show detailed information for selected item in main tree"""
            item_id = self.quote_tree.identify_row(event.y)
            if item_id:
                item_index = self.quote_tree.index(item_id)
                if 0 <= item_index < len(self.quote_items):
                    selected_item = self.quote_items[item_index]
                    self.show_part_details_popup(selected_item, self.root)
        
        self.quote_tree.bind("<Button-3>", show_main_tree_details)  # Right-click
        
        self.quote_tree.grid(row=0, column=0, sticky="wens")
        quote_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Quote summary buttons
        quote_buttons_frame = ttk.Frame(quote_summary_frame)
        quote_buttons_frame.grid(row=1, column=0, columnspan=2, sticky="we", pady=(10, 0))
        
        self.export_button = ttk.Button(quote_buttons_frame, text="Export", command=self.export_quote)
        self.export_button.grid(row=0, column=0, padx=(0, 10))
        
        self.edit_item_button = ttk.Button(quote_buttons_frame, text="Edit Selected", command=self.edit_quote_item)
        self.edit_item_button.grid(row=0, column=1, padx=(0, 10))
        
        self.remove_item_button = ttk.Button(quote_buttons_frame, text="Remove Selected", command=self.remove_quote_item)
        self.remove_item_button.grid(row=0, column=2, padx=(0, 10))
        
        self.clear_quote_button = ttk.Button(quote_buttons_frame, text="Clear Quote", command=self.clear_quote)
        self.clear_quote_button.grid(row=0, column=3, padx=(0, 10))
        
        # Total value display
        self.total_label = ttk.Label(quote_buttons_frame, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.grid(row=0, column=4, padx=(20, 0))
        
        # Quote number display
        self.quote_number_label = ttk.Label(quote_buttons_frame, text="Quote #: Not Generated", font=("Arial", 10))
        self.quote_number_label.grid(row=0, column=5, padx=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, sticky="we", pady=(10, 0))
        
        # Store references to main widgets
        self.main_frame = main_frame
        self.input_frame = input_frame
        self.customer_frame = customer_frame
        self.spare_frame = spare_frame
        self.quote_summary_frame = quote_summary_frame
    
    def setup_layout(self):
        """Configure layout and grid weights"""
        pass  # Already configured in create_widgets
    
    def setup_bindings(self):
        """Setup keyboard bindings and events"""
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_quote())
        self.root.bind('<Control-o>', lambda e: self.open_quote())
        self.root.bind('<Control-s>', lambda e: self.save_quote())
        self.root.bind('<Control-e>', lambda e: self.export_quote())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        
        # Enter key for intelligent part number handling
        self.part_number_entry.bind('<Return>', lambda e: self.handle_part_number_enter())
        
        # Enter key to add spare part
        self.spare_part_entry.bind('<Return>', lambda e: self.add_spare_part())
        
        # Window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def handle_part_number_enter(self):
        """Handle Enter key press in part number field - Parse first time, Add to Quote second time"""
        current_input = self.part_number_var.get().strip()
        
        if not current_input:
            messagebox.showwarning("Input Required", "Please enter a part number.")
            return
        
        # Process shortcuts first
        expanded_input = self.process_shortcut_input(current_input)
        if expanded_input != current_input:
            self.part_number_var.set(expanded_input)
            current_input = expanded_input
        
        # Check if we have parsed data and if the current input matches the parsed part number
        if (self.current_quote_data and 
            current_input == self.current_quote_data.get('part_number')):
            # Second Enter - Input matches already parsed data, so add to quote
            self.add_main_part_to_quote()
            # Clear the field and reset data
            self.part_number_var.set("")
            self.current_quote_data = None
            self.status_var.set("Part added to quote. Enter new part number.")
        else:
            # First Enter or different part number - Parse and price
            self.parse_part_number()
    
    def parse_part_number(self):
        """Parse the entered part number and display results"""
        part_number = self.part_number_var.get().strip()
        
        if not part_number:
            messagebox.showwarning("Input Required", "Please enter a part number to parse.")
            return
        
        try:
            self.status_var.set("Parsing part number...")
            self.root.update()
            
            # Parse the part number (shortcut processing is handled in handle_part_number_enter)
            parsed_result = self.parser.parse_part_number(part_number)
            
            if parsed_result.get('error'):
                self.status_var.set("Parse failed")
                messagebox.showerror("Parse Error", f"Failed to parse part number:\n{parsed_result['error']}")
                # Clear quote data on parse failure
                self.current_quote_data = None
                return
            
            # Generate quote data
            self.current_quote_data = self.parser.get_quote_data(parsed_result)
            
            # Update status with hint about second Enter
            total_price = self.current_quote_data.get('total_price', 0)
            self.status_var.set(f"Part parsed successfully - Total: ${total_price:.2f} (Press Enter again to add to quote)")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred while parsing:\n{str(e)}")
            # Clear quote data on error
            self.current_quote_data = None
    
    def export_quote(self):
        """Export current quote to Word document"""
        print("=== EXPORT_QUOTE FUNCTION CALLED ===")
        print(f"Quote items: {self.quote_items}")
        
        if not self.quote_items:
            print("No quote items - showing warning")
            messagebox.showwarning("No Quote", "Please add items to the quote first.")
            return
        
        print("✓ Quote items validation passed")
        
        # Validate initials are entered
        user_initials = self.initials_var.get().strip()
        print(f"User initials retrieved: '{user_initials}'")
        
        if not user_initials:
            print("❌ No initials entered - showing error")
            messagebox.showerror("Initials Required", 
                "You must enter your initials before exporting a quote.\n\n"
                "This is required for quote number generation and tracking.")
            return
        
        if len(user_initials) < 2:
            print(f"❌ Initials too short: '{user_initials}' - showing error")
            messagebox.showerror("Invalid Initials", "Please enter at least 2 characters for your initials.")
            return
        
        print(f"✓ Initials validation passed: '{user_initials}'")
        
        # Generate quote number if not already generated
        if not self.current_quote_number:
            print("Generating new quote number...")
            if not self.generate_new_quote_number():
                print("❌ Quote number generation failed")
                return  # Failed to generate quote number
        
        print(f"✓ Quote number available: {self.current_quote_number}")
        
        try:
            # Use quote number as default filename
            default_filename = f"{self.current_quote_number}.docx"
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word documents", "*.docx"), ("All files", "*.*")],
                title="Export Quote",
                initialfile=default_filename
            )
            
            if filename:
                print(f"Export filename selected: {filename}")
                
                # Try to use Word template system for the first main item
                success = False
                main_items = [item for item in self.quote_items if item.get('type') == 'main']
                
                if main_items:
                    # Use the first main item for template export
                    main_item = main_items[0]
                    part_number = main_item.get('part_number', '')
                    print(f"Using main item for template: {part_number}")
                    
                    # Extract data properly from the quote item
                    quote_data = main_item.get('data', {})
                    print(f"Quote data keys: {list(quote_data.keys()) if quote_data else 'None'}")
                    
                    # Set current_quote_data temporarily for the export
                    original_quote_data = self.current_quote_data
                    self.current_quote_data = quote_data
                    
                    # Try Word template export first
                    try:
                        from export.word_template_processor import generate_word_quote
                        
                        # Extract base model from part number (e.g., LS2000-115VAC-S-10" -> LS2000)
                        model = part_number.split('-')[0] if '-' in part_number else part_number[:6]
                        print(f"🔧 Extracted model: '{model}' from part: '{part_number}'")
                        
                        # Get customer information
                        customer_name = self.company_var.get() or "Customer Name"
                        contact_name = self.contact_person_var.get() or "Contact Person"
                        
                        # Get employee information for template
                        employee_name = ""
                        employee_phone = ""
                        employee_email = ""
                        if hasattr(self, 'selected_employee_info') and self.selected_employee_info:
                            emp = self.selected_employee_info
                            employee_name = f"{emp['first_name']} {emp['last_name']}"
                            employee_phone = emp.get('work_phone', '')
                            employee_email = emp.get('work_email', '')
                            print(f"🔧 Using employee: {employee_name} ({employee_phone}, {employee_email})")
                        else:
                            print("⚠ No employee selected, using default contact info")
                        
                        # Use the generated quote number (guaranteed to exist at this point)
                        assert self.current_quote_number is not None
                        quote_number = self.current_quote_number
                        
                        # Get pricing info
                        unit_price = quote_data.get('total_price') or quote_data.get('base_price') or 0.0
                        if unit_price and unit_price > 0:
                            unit_price = f"{unit_price:.2f}"
                        else:
                            unit_price = "Please Contact"
                        
                        print(f"🚀 Word template export with:")
                        print(f"   Model: '{model}'")
                        print(f"   Part Number: '{part_number}'")
                        print(f"   Customer: '{customer_name}'")
                        print(f"   Unit Price: '{unit_price}'")
                        
                        # Generate the quote using Word template system
                        success = generate_word_quote(
                            model=model,
                            customer_name=customer_name,
                            attention_name=contact_name,
                            quote_number=quote_number,
                            part_number=part_number,
                            unit_price=unit_price,
                            supply_voltage=quote_data.get('voltage', '115VAC'),
                            probe_length=str(quote_data.get('probe_length', 12)),
                            output_path=filename,
                            # Additional specs from parsed data
                            insulator=quote_data.get('insulator', ''),
                            insulator_material=self._extract_insulator_material_name(quote_data),
                            insulator_length=f"{quote_data.get('base_insulator_length', 4)}\"",
                            probe_material=quote_data.get('probe_material_name', '316SS'),
                            max_temperature=f"{quote_data.get('max_temperature', 450)}°F",
                            max_pressure=f"{quote_data.get('max_pressure', 300)} PSI",
                            output_type=quote_data.get('output_type', '10 Amp SPDT Relay'),
                            process_connection_size=f"{quote_data.get('pc_size', '¾')}\"",
                            pc_type=quote_data.get('pc_type', 'NPT'),
                            pc_size=quote_data.get('pc_size', '¾"'),
                            pc_matt=quote_data.get('pc_matt', 'SS'),
                            pc_rate=quote_data.get('pc_rate'),
                            length_adder=quote_data.get('length_adder', 0.0),
                            adder_per=quote_data.get('adder_per', 'none'),
                            # Employee information
                            employee_name=employee_name,
                            employee_phone=employee_phone,
                            employee_email=employee_email
                        )
                        print(f"✅ Word template export success: {success}")
                        
                    except Exception as e:
                        print(f"❌ Word template export failed: {e}")
                        import traceback
                        traceback.print_exc()
                        success = False
                    
                    # If Word template failed, try RTF fallback
                    if not success:
                        print("📄 Trying RTF template fallback...")
                        success = self._try_rtf_template_export(filename)
                    
                    # Restore original quote data
                    self.current_quote_data = original_quote_data
                
                if not success:
                    print("❌ Template export failed, using old quote generator...")
                    # Create combined data for export
                    combined_data = {
                        'type': 'multi_item_quote',
                        'items': self.quote_items,
                        'total_items': len(self.quote_items),
                        'total_price': sum(item.get('total_price', 0) for item in self.quote_items),
                        'export_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Export to Word using old system
                    output_path = self.quote_generator.generate_quote(combined_data, output_path=filename)
                    success = bool(output_path)
                
                if success:
                    # Save quote to database after successful export
                    try:
                        # Calculate total for database save
                        customer_name = self.company_var.get().strip()
                        if customer_name and self.current_quote_number:
                            if self.db_manager.connect():
                                # At this point current_quote_number is guaranteed to be set
                                assert self.current_quote_number is not None
                                
                                total_quote_value = sum(item.get('total_price', 0) for item in self.quote_items)
                                
                                db_save_success = self.db_manager.save_quote(
                                    quote_number=self.current_quote_number,
                                    customer_name=customer_name,
                                    customer_email=self.email_var.get().strip(),
                                    quote_items=self.quote_items,
                                    total_price=total_quote_value,
                                    user_initials=user_initials
                                )
                                
                                if db_save_success:
                                    self.status_var.set(f"Quote {self.current_quote_number} exported and saved to database")
                                else:
                                    self.status_var.set(f"Quote {self.current_quote_number} exported (database save failed)")
                                
                                self.db_manager.disconnect()
                    except Exception as db_error:
                        print(f"Database save error: {db_error}")
                        # Don't show error to user since export was successful
                    
                    self.status_var.set(f"Quote exported to {filename}")
                    messagebox.showinfo("Export Success", f"Quote exported successfully to:\n{filename}\n\nQuote Number: {self.current_quote_number}")
                else:
                    print("❌ Export failed - all methods unsuccessful")
                    self.status_var.set("Export failed")
                    messagebox.showerror("Export Error", "Failed to export quote using all available methods.")
                
        except Exception as e:
            print(f"❌ Exception in export_quote: {e}")
            import traceback
            traceback.print_exc()
            self.status_var.set("Export failed")
            messagebox.showerror("Export Error", f"Failed to export quote:\n{str(e)}")
    
    def _get_insulator_material_name(self) -> str:
        """Get the proper insulator material display name from parsed quote data"""
        if not self.current_quote_data:
            return 'UHMWPE'
        
        # First try to extract from the formatted insulator string
        insulator_display = self.current_quote_data.get('insulator', '')
        if insulator_display and '"' in insulator_display:
            # Extract material from strings like "4.0\" Teflon"
            parts = insulator_display.split('"')
            if len(parts) > 1:
                material = parts[1].strip()
                if material:
                    return material
        
        # Fallback: translate material code to display name
        material_code = self.current_quote_data.get('insulator_material', 'U')
        material_codes = {
            'TEF': 'Teflon',
            'U': 'UHMWPE', 
            'UHMWPE': 'UHMWPE',
            'DEL': 'DELRIN',
            'PEEK': 'PEEK',
            'CER': 'Ceramic'
        }
        return material_codes.get(material_code, 'UHMWPE')

    @staticmethod
    def _extract_insulator_material_name(quote_data: dict) -> str:
        """Extract proper insulator material display name from any quote data dictionary"""
        if not quote_data:
            return 'UHMWPE'
        
        # First try to extract from the formatted insulator string
        insulator_display = quote_data.get('insulator', '')
        if insulator_display and '"' in insulator_display:
            # Extract material from strings like "4.0\" Teflon"
            parts = insulator_display.split('"')
            if len(parts) > 1:
                material = parts[1].strip()
                if material:
                    return material
        
        # Fallback: translate material code to display name
        material_code = quote_data.get('insulator_material', 'U')
        material_codes = {
            'TEF': 'Teflon',
            'U': 'UHMWPE', 
            'UHMWPE': 'UHMWPE',
            'DEL': 'DELRIN',
            'PEEK': 'PEEK',
            'CER': 'Ceramic'
        }
        return material_codes.get(material_code, 'UHMWPE')

    def _try_rtf_template_export(self, export_path: str) -> bool:
        """Try exporting using the new Word template system"""
        try:
            # Check if we have quote data
            if not self.current_quote_data:
                print("No quote data available")
                return False
                
            # Import the new template systems
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            
            # Try Word template system first (preferred)
            try:
                from export.word_template_processor import generate_word_quote
                print("✓ Word template processor imported successfully")
                print("Attempting Word template export...")
                success = self._try_word_template_export(export_path)
                print(f"Word template export returned: {success}")
                if success:
                    print("✓ Word template export successful - returning True")
                    return True
                print("⚠ Word template export failed, trying RTF fallback...")
            except ImportError as e:
                print(f"❌ Word template system import failed: {e}")
            except Exception as e:
                print(f"❌ Word template system error: {e}")
                import traceback
                traceback.print_exc()
            
            # Fallback to RTF template system
            print("📄 Falling back to RTF template system...")
            from export.word_exporter import generate_quote
            
            # Extract base model from part number (e.g., LS2000-115VAC-S-10" -> LS2000)
            part_number = self.current_quote_data.get('original_part_number', '')
            model = part_number.split('-')[0] if '-' in part_number else part_number[:6]
            
            # Get customer information
            customer_name = self.company_var.get() or "Customer Name"
            contact_name = self.contact_person_var.get() or "Contact Person"
            
            # Generate quote number
            from datetime import datetime
            quote_number = f"Q-{datetime.now().strftime('%Y%m%d-%H%M')}"
            
            # Get pricing info
            unit_price = self.current_quote_data.get('total_price') or self.current_quote_data.get('base_price') or 0.0
            if unit_price and unit_price > 0:
                unit_price = f"{unit_price:.2f}"
            else:
                unit_price = "Please Contact"
            
            # Debug output
            print(f"RTF Export Debug:")
            print(f"  Model: {model}")
            print(f"  Part Number: {part_number}")
            print(f"  Customer: {customer_name}")
            print(f"  Export Path: {export_path}")
            print(f"  Unit Price: {unit_price}")
            
            # Generate the quote using RTF template system
            success = generate_quote(
                model=model,
                customer_name=customer_name,
                attention_name=contact_name,
                quote_number=quote_number,
                part_number=part_number,
                unit_price=unit_price,
                supply_voltage=self.current_quote_data.get('voltage', '115VAC'),
                probe_length=str(self.current_quote_data.get('probe_length', 12)),
                output_path=export_path,
                # Additional specs from parsed data
                insulator_material=self._get_insulator_material_name(),
                probe_material=self.current_quote_data.get('probe_material_name', '316SS'),
                max_temperature=f"{self.current_quote_data.get('max_temperature', 450)} F",
                max_pressure=f"{self.current_quote_data.get('max_pressure', 300)} PSI"
            )
            
            print(f"RTF export success: {success}")
            if success and os.path.exists(export_path):
                print(f"File created successfully: {os.path.getsize(export_path)} bytes")
            else:
                print(f"File not found after export: {export_path}")
            
            return success
            
        except Exception as e:
            print(f"RTF template export failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _try_word_template_export(self, export_path: str) -> bool:
        """Try exporting using the Word template system with template variables"""
        try:
            print("🔧 Starting Word template export...")
            from export.word_template_processor import generate_word_quote
            print("✓ generate_word_quote imported successfully")
            
            # Ensure we have quote data
            if not self.current_quote_data:
                print("❌ No quote data available")
                return False
            print("✓ Quote data available")
            
            # Extract base model from part number (e.g., LS2000-115VAC-S-10" -> LS2000)
            part_number = self.current_quote_data.get('original_part_number', '')
            model = part_number.split('-')[0] if '-' in part_number else part_number[:6]
            
            # Get customer information
            customer_name = self.company_var.get() or "Customer Name"
            contact_name = self.contact_person_var.get() or "Contact Person"
            
            # Employee info for template
            employee_name = ""
            employee_phone = ""
            employee_email = ""
            if hasattr(self, 'selected_employee_info') and self.selected_employee_info:
                emp = self.selected_employee_info
                employee_name = f"{emp['first_name']} {emp['last_name']}"
                employee_phone = emp.get('work_phone', '')
                employee_email = emp.get('work_email', '')
            
            # Generate quote number
            from datetime import datetime
            quote_number = f"Q-{datetime.now().strftime('%Y%m%d-%H%M')}"
            
            # Get pricing info
            unit_price = self.current_quote_data.get('total_price') or self.current_quote_data.get('base_price') or 0.0
            if unit_price and unit_price > 0:
                unit_price = f"{unit_price:.2f}"
            else:
                unit_price = "Please Contact"
            
            # Debug output
            print(f"Word Template Export Debug:")
            print(f"  Model: {model}")
            print(f"  Part Number: {part_number}")
            print(f"  Customer: {customer_name}")
            print(f"  Export Path: {export_path}")
            print(f"  Unit Price: {unit_price}")
            print(f"  Employee Name: {employee_name}")
            print(f"  Employee Phone: {employee_phone}")
            
            # Generate the quote using Word template system
            print("🚀 Calling generate_word_quote with parameters:")
            print(f"   Model: {model}")
            print(f"   Customer: {customer_name}")
            print(f"   Part Number: {part_number}")
            print(f"   Output Path: {export_path}")
            
            success = generate_word_quote(
                model=model,
                customer_name=customer_name,
                attention_name=contact_name,
                quote_number=quote_number,
                part_number=part_number,
                unit_price=unit_price,
                supply_voltage=self.current_quote_data.get('voltage', '115VAC'),
                probe_length=str(self.current_quote_data.get('probe_length', 12)),
                output_path=export_path,
                # Additional specs from parsed data
                insulator=self.current_quote_data.get('insulator', ''),
                insulator_material=self._get_insulator_material_name(),
                insulator_length=f"{self.current_quote_data.get('base_insulator_length', 4)}\"",
                probe_material=self.current_quote_data.get('probe_material_name', '316SS'),
                probe_material_name=self.current_quote_data.get('probe_material_name', '316 Stainless Steel'),
                probe_diameter=self.current_quote_data.get('probe_diameter', '½"'),
                max_temperature=f"{self.current_quote_data.get('max_temperature', 450)}°F",
                max_pressure=f"{self.current_quote_data.get('max_pressure', 300)} PSI",
                # Employee info
                employee_name=employee_name,
                employee_phone=employee_phone,
                employee_email=employee_email,
            )
            
            print(f"Word template export success: {success}")
            if success and os.path.exists(export_path):
                print(f"File created successfully: {os.path.getsize(export_path)} bytes")
            else:
                print(f"File not found after export: {export_path}")
            
            return success
        except Exception as e:
            print(f"RTF template export failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def new_quote(self):
        """Start a new quote"""
        self.part_number_var.set("")
        self.company_var.set("New Customer") # Changed from self.customer_var.set("New Customer")
        self.main_qty_var.set("1")
        self.current_quote_data = None
        self.current_quote_number = None
        
        # Clear quote items
        self.quote_items = []
        
        # Clear quote tree display
        for item in self.quote_tree.get_children():
            self.quote_tree.delete(item)
        
        # Update total and quote number display
        self.update_quote_total()
        self.update_quote_number_display()
        
        self.status_var.set("Ready for new quote")
    
    def open_quote(self):
        """Open an existing quote"""
        # Show dialog to select a quote to open
        recent_quotes = []
        try:
            if not self.db_manager.connect():
                messagebox.showerror("Database Error", "Could not connect to database.")
                return
            
            # Get recent quotes for this user or all quotes
            user_initials = self.initials_var.get().strip()
            recent_quotes = self.db_manager.get_recent_quotes(limit=20, user_initials=user_initials)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load quotes: {str(e)}")
            return
        finally:
            self.db_manager.disconnect()
        
        if not recent_quotes:
            messagebox.showinfo("No Quotes", "No quotes found to open.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Open Quote")
        selection_window.geometry("600x400")
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        # Center the window
        selection_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        selection_window.geometry(f"600x400+{x}+{y}")
        
        main_frame = ttk.Frame(selection_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Select a quote to open:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Create listbox with quotes
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        quote_listbox = tk.Listbox(listbox_frame, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=quote_listbox.yview)
        quote_listbox.configure(yscrollcommand=scrollbar.set)
        
        quote_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate listbox
        for quote in recent_quotes:
            date_str = quote['created_at'][:10] if quote['created_at'] else 'Unknown'
            display_text = f"{quote['quote_number']} - {quote['customer_name']} - ${quote['total_price']:.2f} - {date_str}"
            quote_listbox.insert(tk.END, display_text)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def open_selected():
            selection = quote_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a quote to open.")
                return
            
            selected_quote = recent_quotes[selection[0]]
            quote_number = selected_quote['quote_number']
            
            # Load the complete quote data
            try:
                if not self.db_manager.connect():
                    messagebox.showerror("Database Error", "Could not connect to database.")
                    return
                
                quote_data = self.db_manager.load_quote(quote_number)
                if not quote_data:
                    messagebox.showerror("Error", f"Could not load quote {quote_number}")
                    return
                
                # Clear current quote
                self.new_quote()
                
                # Load customer information
                self.company_var.set(quote_data['customer_name'] or '')
                self.email_var.set(quote_data['customer_email'] or '')
                
                # Set quote number
                self.current_quote_number = quote_data['quote_number']
                self.update_quote_number_display()
                
                # Note: Loading quote items would require more complex logic
                # to rebuild the original quote items structure
                messagebox.showinfo("Quote Loaded", f"Quote {quote_number} basic information loaded.\nNote: Individual quote items would need additional implementation to fully restore.")
                
                selection_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load quote: {str(e)}")
            finally:
                self.db_manager.disconnect()
        
        ttk.Button(button_frame, text="Open", command=open_selected).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=selection_window.destroy).pack(side=tk.RIGHT)
    
    def save_quote(self):
        """Save current quote to database"""
        if not self.quote_items:
            messagebox.showwarning("No Quote", "Please add items to the quote first.")
            return
        
        # Validate required fields
        customer_name = self.company_var.get().strip()
        if not customer_name:
            messagebox.showerror("Customer Required", "Please enter a customer name before saving.")
            return
        
        user_initials = self.initials_var.get().strip()
        if not user_initials:
            messagebox.showerror("Initials Required", "Please enter your initials before saving.")
            return
        
        # Generate quote number if not already generated
        if not self.current_quote_number:
            if not self.generate_new_quote_number():
                return
        
        # Calculate total
        total_value = 0.0
        for item in self.quote_items:
            if item['type'] == 'main':
                unit_price = item['data'].get('total_price', 0.0)
            else:  # spare part
                unit_price = item['data'].get('pricing', {}).get('total_price', 0.0)
            quantity = item.get('quantity', 1)
            total_value += unit_price * quantity
        
        # Save to database
        try:
            if not self.db_manager.connect():
                messagebox.showerror("Database Error", "Could not connect to database.")
                return
            
            # At this point current_quote_number is guaranteed to be set
            assert self.current_quote_number is not None
            
            success = self.db_manager.save_quote(
                quote_number=self.current_quote_number,
                customer_name=customer_name,
                customer_email=self.email_var.get().strip(),
                quote_items=self.quote_items,
                total_price=total_value,
                user_initials=user_initials
            )
            
            if success:
                messagebox.showinfo("Quote Saved", f"Quote {self.current_quote_number} saved successfully!")
                self.status_var.set(f"Quote {self.current_quote_number} saved to database")
            else:
                messagebox.showerror("Save Failed", "Failed to save quote to database.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save quote: {str(e)}")
        finally:
            self.db_manager.disconnect()
    
    def clear_part_number(self):
        """Clear part number entry and reset parsed data"""
        self.part_number_var.set("")
        self.current_quote_data = None
        self.status_var.set("Ready")
        self.part_number_entry.focus()
    
    def clear_results(self):
        """Clear results display"""
        self.current_quote_data = None
        self.status_var.set("Results cleared")
    
    def show_samples(self):
        """Show sample part numbers"""
        sample_window = tk.Toplevel(self.root)
        sample_window.title("Sample Part Numbers")
        sample_window.geometry("500x400")
        sample_window.transient(self.root)
        sample_window.grab_set()
        
        # Center the window
        sample_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 250
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 200
        sample_window.geometry(f"500x400+{x}+{y}")
        
        # Create content
        frame = ttk.Frame(sample_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Sample Part Numbers:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Listbox with samples
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Consolas", 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Add sample part numbers
        for sample in SAMPLE_PART_NUMBERS:
            listbox.insert(tk.END, sample)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        def use_selected():
            selection = listbox.curselection()
            if selection:
                selected_part = listbox.get(selection[0])
                self.part_number_var.set(selected_part)
                sample_window.destroy()
                self.parse_part_number()
        
        ttk.Button(button_frame, text="Use Selected", command=use_selected).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Close", command=sample_window.destroy).pack(side=tk.RIGHT)
        
        # Double-click to select
        listbox.bind('<Double-Button-1>', lambda e: use_selected())
    
    def validate_database(self):
        """Validate database connection"""
        try:
            if self.parser.db.test_connection():
                messagebox.showinfo("Database Valid", "Database connection and structure are valid.")
            else:
                messagebox.showerror("Database Error", "Database validation failed.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Database validation error:\n{str(e)}")
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.root)
    
    def show_help(self):
        """Show help/user guide"""
        try:
            import webbrowser
            help_path = os.path.join(os.path.dirname(__file__), '..', 'USER_GUIDE.md')
            if os.path.exists(help_path):
                webbrowser.open(f"file://{os.path.abspath(help_path)}")
            else:
                messagebox.showinfo("Help", "User guide not found. Please refer to the documentation.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open help:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        dialog = AboutDialog(self.root)
    
    def show_shortcut_manager(self):
        """Show the shortcut manager dialog"""
        try:
            ShortcutManagerDialog(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open shortcut manager: {str(e)}")

    def show_employee_manager(self):
        """Show the employee manager dialog"""
        try:
            from .employee_manager import EmployeeManagerDialog
            
            def on_employee_selected(employee):
                """Handle employee selection for quote attribution"""
                # Set the initials field with employee initials
                initials = f"{employee['first_name'][0]}{employee['last_name'][0]}".upper()
                self.initials_var.set(initials)
                # Store the selected employee info for template use
                self.selected_employee_info = employee
                # Optionally show a message
                messagebox.showinfo("Employee Selected", 
                                  f"Employee {employee['first_name']} {employee['last_name']} selected.\n"
                                  f"Initials set to: {initials}")
            
            dialog = EmployeeManagerDialog(self.root, self.db_manager, on_employee_selected)
            dialog.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open employee manager: {str(e)}")
    
    def process_shortcut_input(self, text: str) -> str:
        """
        Process input text and expand shortcuts if found.
        Returns the expanded part number or original text if no shortcut found.
        """
        # Check if the input looks like a shortcut (alphanumeric only, no hyphens)
        if text and text.isalnum():
            try:
                # Try to get part number from shortcut
                expanded_pn = self.db_manager.get_part_number_by_shortcut(text)
                if expanded_pn:
                    return expanded_pn
            except Exception as e:
                print(f"Error processing shortcut: {e}")
        
        # Return original text if not a shortcut or expansion failed
        return text
    
    def add_spare_part(self):
        """Add a spare part to the list"""
        part_number = self.spare_part_var.get().strip()
        
        if not part_number:
            messagebox.showwarning("Input Required", "Please enter a spare part number.")
            return
        
        try:
            quantity = int(self.spare_qty_var.get() or 1)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please enter a valid positive quantity.")
            return
        
        try:
            self.status_var.set("Adding spare part...")
            self.root.update()
            
            # Parse and quote the spare part
            result = self.spare_parts_manager.parse_and_quote_spare_part(part_number, quantity)
            
            if result.get('success'):
                # Add to our list
                spare_part_info = {
                    'original_part_number': part_number,
                    'description': result['line_item_description'],
                    'quantity': quantity,
                    'unit_price': result['unit_price'],
                    'total_price': result['total_price'],
                    'parsed_result': result['parsed_part']
                }
                
                self.spare_parts_list.append(spare_part_info)
                
                # Also add to quote items list
                quote_item = {
                    'type': 'spare',
                    'part_number': part_number,
                    'customer_name': self.company_var.get().strip(), # Changed from self.customer_var.get()
                    'quantity': quantity,
                    'data': {
                        'description': result['line_item_description'],
                        'pricing': {
                            'total_price': result['unit_price']
                        }
                    },
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.quote_items.append(quote_item)
                
                # Add to quote tree
                self.add_to_quote_tree("spare", part_number, result['line_item_description'], 
                                     quantity, result['unit_price'], result['total_price'])
                
                # Clear input fields
                self.spare_part_var.set("")
                self.spare_qty_var.set("1")
                
                # Update status
                self.status_var.set(f"Added spare part: {part_number} - Total quote items: {len(self.quote_items)}")
                
            else:
                self.status_var.set("Failed to add spare part")
                error_msg = result.get('error', 'Unknown error')
                details = result.get('details', [])
                suggestions = result.get('suggestions', [])
                
                msg = f"Failed to add spare part:\n{error_msg}"
                if details:
                    msg += f"\n\nDetails: {', '.join(details)}"
                if suggestions:
                    msg += f"\n\nSuggestions: {', '.join(suggestions)}"
                
                messagebox.showerror("Add Spare Part Failed", msg)
        
        except Exception as e:
            self.status_var.set("Error adding spare part")
            messagebox.showerror("Error", f"An error occurred while adding spare part:\n{str(e)}")
    

    
    def show_spare_parts_help(self):
        """Show help for spare parts format"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Spare Parts Format Help")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center the window
        help_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        help_window.geometry(f"600x500+{x}+{y}")
        
        # Create content
        frame = ttk.Frame(help_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text="Spare Parts Format Guide", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Add help content
        help_content = """SPARE PARTS FORMAT GUIDE

Electronics:
Format: {MODEL}-{VOLTAGE}-E
Examples:
  LS2000-115VAC-E   → LS2000 Electronics (115VAC)
  LS7000-24VDC-E    → LS7000 Electronics (24VDC)
  LS8000-230VAC-E   → LS8000 Electronics (230VAC)

Probe Assemblies:
Format: {MODEL}-{MATERIAL}-{LENGTH}"
Examples:
  LS2000-S-10"      → LS2000 Stainless Steel Probe 10"
  LS7000-H-12"      → LS7000 Halar Coated Probe 12"
  LS6000-U-4"       → LS6000 UHMWPE Probe 4"

Power Supplies:
Format: {MODEL}-{VOLTAGE}-PS
Examples:
  LS7000-115VAC-PS  → LS7000 Power Supply (115VAC)
  LT9000-24VDC-BB   → LT9000 BB Power Supply (24VDC)

Receiver Cards:
Format: {MODEL}-{VOLTAGE}-R
Examples:
  LS8000-115VAC-R   → LS8000 Receiver Card (115VAC)
  LS8000/2-24VDC-R  → LS8000/2 Receiver Card (24VDC)

Transmitters:
Format: {MODEL}-{SPECS}-T
Examples:
  LS8000-HIGH-T     → LS8000 Transmitter (HIGH)
  LS8000-SIZE-SENS-T → LS8000 Transmitter (SIZE-SENS)

Cards:
Sensing Card:    {MODEL}-SC     → LS7000-SC
Dual Point:      {MODEL}-DP     → LS7000/2-DP
Plugin Card:     {MODEL}-MA     → LT9000-MA

Fuses:
Format: {MODEL}-FUSE
Examples:
  LS7000-FUSE       → LS7000 Fuse ($10.00)
  LT9000-FUSE       → LT9000 Fuse ($20.00)

Housing:
Format: {MODEL}-HOUSING
Examples:
  LS2000-HOUSING    → LS2000 Housing
  FS10000-HOUSING   → FS10000 Housing

Valid Voltages: 115VAC, 24VDC, 230VAC, 12VDC
Valid Materials: S, H, U, T, TS, CPVC, C

Length pricing is automatically calculated for probe assemblies.
"""
        
        text_widget.insert(tk.END, help_content)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(frame, text="Close", command=help_window.destroy).pack(anchor=tk.E)
    
    def add_main_part_to_quote(self):
        """Add the current main part to the quote"""
        if not self.current_quote_data:
            messagebox.showwarning("No Part Data", "Please parse a part number first.")
            return
        
        try:
            # Get customer info
            customer_name = self.company_var.get().strip() # Changed from self.customer_var.get()
            if not customer_name:
                messagebox.showwarning("Customer Required", "Please enter a customer name.")
                return
            
            quantity = int(self.main_qty_var.get() or 1)
            if quantity <= 0:
                messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity (greater than 0).")
                return

            # Ensure the raw data reflects the correct quantity
            self.current_quote_data['quantity'] = quantity

            # Create quote item
            quote_item = {
                'type': 'main',
                'part_number': self.part_number_var.get().strip(),
                'customer_name': customer_name,
                'quantity': quantity,
                'data': self.current_quote_data.copy(),
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add to quote items list
            self.quote_items.append(quote_item)
            
            # Add to quote tree display
            description = f"{self.current_quote_data.get('model', 'N/A')} - {self.current_quote_data.get('voltage', 'N/A')}"
            unit_price = self.current_quote_data.get('total_price', 0)
            total_price = unit_price * quantity
            
            self.add_to_quote_tree("main", quote_item['part_number'], description, 
                                 quantity, unit_price, total_price)
            
            self.status_var.set(f"Added to quote: {quote_item['part_number']} (Qty: {quantity}) - Total items: {len(self.quote_items)}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid quantity (number).")
        except Exception as e:
            self.status_var.set("Error adding to quote")
            messagebox.showerror("Error", f"Failed to add to quote:\n{str(e)}")
    
    def view_quote(self):
        """Display all items currently in the quote"""
        if not self.quote_items:
            messagebox.showinfo("Empty Quote", "No items in quote yet.\n\nAdd main parts using 'Add to Quote' button and spare parts using 'Add Spare Part' button.")
            return
        
        # Create quote summary window
        quote_window = tk.Toplevel(self.root)
        quote_window.title("Quote Summary")
        quote_window.geometry("800x600")
        quote_window.transient(self.root)
        quote_window.grab_set()
        
        # Center the window
        quote_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 400
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 300
        quote_window.geometry(f"800x600+{x}+{y}")
        
        # Create content
        frame = ttk.Frame(quote_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = ttk.Frame(frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="Quote Summary", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Label(title_frame, text=f"Total Items: {len(self.quote_items)}", font=("Arial", 10)).pack(side=tk.RIGHT)
        
        # Create notebook for different views
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Summary tab
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary")
        
        # Summary treeview
        summary_columns = ("Type", "Part Number", "Customer", "Quantity", "Unit Price", "Total Price", "Added")
        summary_tree = ttk.Treeview(summary_frame, columns=summary_columns, show="headings", height=15)
        
        # Configure columns
        summary_tree.heading("Type", text="Type")
        summary_tree.heading("Part Number", text="Part Number")
        summary_tree.heading("Customer", text="Customer")
        summary_tree.heading("Quantity", text="Qty")
        summary_tree.heading("Unit Price", text="Unit Price")
        summary_tree.heading("Total Price", text="Total Price")
        summary_tree.heading("Added", text="Added")
        
        summary_tree.column("Type", width=80)
        summary_tree.column("Part Number", width=200)
        summary_tree.column("Customer", width=120)
        summary_tree.column("Quantity", width=60)
        summary_tree.column("Unit Price", width=100)
        summary_tree.column("Total Price", width=100)
        summary_tree.column("Added", width=120)
        
        # Add items to tree
        total_quote_value = 0.0
        for i, item in enumerate(self.quote_items, 1):
            item_type = item['type'].upper()
            part_number = item['part_number']
            customer = item.get('customer_name', 'N/A')
            quantity = item.get('quantity', 1)
            
            # Get pricing info
            if item['type'] == 'main':
                unit_price = item['data'].get('total_price', 0.0)
            else:  # spare part
                unit_price = item['data'].get('pricing', {}).get('total_price', 0.0)
            
            total_price = unit_price * quantity
            total_quote_value += total_price
            timestamp = item['timestamp']
            
            summary_tree.insert("", "end", values=(
                item_type, part_number, customer, quantity, 
                f"${unit_price:.2f}", f"${total_price:.2f}", timestamp
            ))
        
        # Add scrollbar
        summary_scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=summary_tree.yview)
        summary_tree.configure(yscrollcommand=summary_scrollbar.set)
        
        # Add right-click context menu
        def show_item_details(event):
            """Show detailed information for selected item"""
            item_id = summary_tree.identify_row(event.y)
            if item_id:
                item_index = summary_tree.index(item_id)
                if 0 <= item_index < len(self.quote_items):
                    selected_item = self.quote_items[item_index]
                    self.show_part_details_popup(selected_item, quote_window)
        
        summary_tree.bind("<Button-3>", show_item_details)  # Right-click
        
        summary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Details tab
        details_frame = ttk.Frame(notebook)
        notebook.add(details_frame, text="Details")
        
        # Details text widget
        details_text = tk.Text(details_frame, wrap=tk.WORD, font=("Consolas", 9))
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=details_text.yview)
        details_text.configure(yscrollcommand=details_scrollbar.set)
        
        details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add detailed information
        details_text.insert(tk.END, "DETAILED QUOTE BREAKDOWN\n")
        details_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, item in enumerate(self.quote_items, 1):
            details_text.insert(tk.END, f"ITEM {i}: {item['type'].upper()} PART\n")
            details_text.insert(tk.END, "-" * 30 + "\n")
            details_text.insert(tk.END, f"Part Number: {item['part_number']}\n")
            details_text.insert(tk.END, f"Customer: {item.get('customer_name', 'N/A')}\n")
            details_text.insert(tk.END, f"Quantity: {item.get('quantity', 1)}\n")
            details_text.insert(tk.END, f"Added: {item['timestamp']}\n")
            
            if item['type'] == 'main':
                data = item['data']
                details_text.insert(tk.END, f"Model: {data.get('model', 'N/A')}\n")
                details_text.insert(tk.END, f"Voltage: {data.get('voltage', 'N/A')}\n")
                details_text.insert(tk.END, f"Probe Length: {data.get('probe_length', 'N/A')}\"\n")
                details_text.insert(tk.END, f"Process Connection: {data.get('process_connection_type', 'N/A')}\n")
                details_text.insert(tk.END, f"Unit Price: ${data.get('total_price', 0):.2f}\n")
            else:  # spare part
                data = item['data']
                details_text.insert(tk.END, f"Description: {data.get('description', 'N/A')}\n")
                details_text.insert(tk.END, f"Unit Price: ${data.get('pricing', {}).get('total_price', 0):.2f}\n")
            
            details_text.insert(tk.END, "\n")
        
        details_text.config(state=tk.DISABLED)
        
        # Summary frame at bottom
        summary_bottom_frame = ttk.Frame(frame)
        summary_bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Total value
        ttk.Label(summary_bottom_frame, text=f"Total Quote Value: ${total_quote_value:.2f}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def remove_selected_item():
            selection = summary_tree.selection()
            if selection:
                item_id = selection[0]
                item_index = summary_tree.index(item_id)
                if 0 <= item_index < len(self.quote_items):
                    removed_item = self.quote_items.pop(item_index)
                    messagebox.showinfo("Item Removed", f"Removed from quote:\n{removed_item['part_number']}")
                    quote_window.destroy()
                    self.view_quote()  # Refresh the view
        
        def clear_quote():
            if messagebox.askyesno("Clear Quote", "Are you sure you want to clear all items from the quote?"):
                self.quote_items.clear()
                messagebox.showinfo("Quote Cleared", "All items removed from quote.")
                quote_window.destroy()
        
        def export_full_quote():
            print("=== EXPORT_FULL_QUOTE FUNCTION CALLED ===")
            
            if not self.quote_items:
                messagebox.showwarning("Empty Quote", "No items to export.")
                return
            
            # Validate initials are entered (same logic as main export)
            user_initials = self.initials_var.get().strip()
            if not user_initials:
                messagebox.showerror("Initials Required", 
                    "You must enter your initials before exporting a quote.\n\n"
                    "This is required for quote number generation and tracking.")
                return
            
            if len(user_initials) < 2:
                messagebox.showerror("Invalid Initials", "Please enter at least 2 characters for your initials.")
                return
            
            # Generate quote number if not already generated
            if not self.current_quote_number:
                if not self.generate_new_quote_number():
                    return  # Failed to generate quote number
            
            try:
                # Use quote number as default filename
                default_filename = f"{self.current_quote_number}.docx"
                
                filename = filedialog.asksaveasfilename(
                    defaultextension=".docx",
                    filetypes=[("Word documents", "*.docx"), ("All files", "*.*")],
                    title="Export Complete Quote",
                    initialfile=default_filename
                )
                
                if filename:
                    print(f"Export filename selected: {filename}")
                    
                    # Try to use Word template system for the first main item
                    success = False
                    main_items = [item for item in self.quote_items if item.get('type') == 'main']
                    
                    if main_items:
                        # Use the first main item for template export
                        main_item = main_items[0]
                        part_number = main_item.get('part_number', '')
                        print(f"Using main item for template: {part_number}")
                        
                        # Extract data properly from the quote item
                        quote_data = main_item.get('data', {})
                        print(f"Quote data keys: {list(quote_data.keys()) if quote_data else 'None'}")
                        
                        # Set current_quote_data temporarily for the export
                        original_quote_data = self.current_quote_data
                        self.current_quote_data = quote_data
                        
                        # Try Word template export first
                        try:
                            from export.word_template_processor import generate_word_quote
                            
                            # Extract base model from part number (e.g., LS2000-115VAC-S-10" -> LS2000)
                            model = part_number.split('-')[0] if '-' in part_number else part_number[:6]
                            print(f"🔧 Extracted model: '{model}' from part: '{part_number}'")
                            
                            # Get customer information
                            customer_name = self.company_var.get() or "Customer Name"
                            contact_name = self.contact_person_var.get() or "Contact Person"
                            
                            # Get employee information for template
                            employee_name = ""
                            employee_phone = ""
                            employee_email = ""
                            if hasattr(self, 'selected_employee_info') and self.selected_employee_info:
                                emp = self.selected_employee_info
                                employee_name = f"{emp['first_name']} {emp['last_name']}"
                                employee_phone = emp.get('work_phone', '')
                                employee_email = emp.get('work_email', '')
                                print(f"🔧 Using employee: {employee_name} ({employee_phone}, {employee_email})")
                            else:
                                print("⚠ No employee selected, using default contact info")
                            
                            # Use the generated quote number (guaranteed to exist at this point)
                            assert self.current_quote_number is not None
                            quote_number = self.current_quote_number
                            
                            # Get pricing info
                            unit_price = quote_data.get('total_price') or quote_data.get('base_price') or 0.0
                            if unit_price and unit_price > 0:
                                unit_price = f"{unit_price:.2f}"
                            else:
                                unit_price = "Please Contact"
                            
                            print(f"🚀 Word template export with:")
                            print(f"   Model: '{model}'")
                            print(f"   Part Number: '{part_number}'")
                            print(f"   Customer: '{customer_name}'")
                            print(f"   Unit Price: '{unit_price}'")
                            
                            # Generate the quote using Word template system
                            success = generate_word_quote(
                                model=model,
                                customer_name=customer_name,
                                attention_name=contact_name,
                                quote_number=quote_number,
                                part_number=part_number,
                                unit_price=unit_price,
                                supply_voltage=quote_data.get('voltage', '115VAC'),
                                probe_length=str(quote_data.get('probe_length', 12)),
                                output_path=filename,
                                # Additional specs from parsed data
                                insulator=quote_data.get('insulator', ''),
                                insulator_material=self._extract_insulator_material_name(quote_data),
                                insulator_length=f"{quote_data.get('base_insulator_length', 4)}\"",
                                probe_material=quote_data.get('probe_material_name', '316SS'),
                                max_temperature=f"{quote_data.get('max_temperature', 450)}°F",
                                max_pressure=f"{quote_data.get('max_pressure', 300)} PSI",
                                output_type=quote_data.get('output_type', '10 Amp SPDT Relay'),
                                process_connection_size=f"{quote_data.get('pc_size', '¾')}\"",
                                pc_type=quote_data.get('pc_type', 'NPT'),
                                pc_size=quote_data.get('pc_size', '¾"'),
                                pc_matt=quote_data.get('pc_matt', 'SS'),
                                pc_rate=quote_data.get('pc_rate'),
                                length_adder=quote_data.get('length_adder', 0.0),
                                adder_per=quote_data.get('adder_per', 'none'),
                                # Employee information
                                employee_name=employee_name,
                                employee_phone=employee_phone,
                                employee_email=employee_email
                            )
                            print(f"✅ Word template export success: {success}")
                            
                        except Exception as e:
                            print(f"❌ Word template export failed: {e}")
                            import traceback
                            traceback.print_exc()
                            success = False
                        
                        # If Word template failed, try RTF fallback
                        if not success:
                            print("📄 Trying RTF template fallback...")
                            success = self._try_rtf_template_export(filename)
                        
                        # Restore original quote data
                        self.current_quote_data = original_quote_data
                    
                    if not success:
                        print("❌ Template export failed, using old quote generator...")
                        # Create combined data for export
                        combined_data = {
                            'type': 'multi_item_quote',
                            'items': self.quote_items,
                            'total_items': len(self.quote_items),
                            'total_price': total_quote_value,
                            'export_timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Export to Word using old system
                        output_path = self.quote_generator.generate_quote(combined_data, output_path=filename)
                        success = bool(output_path)
                    
                    if success:
                        # Save quote to database after successful export
                        try:
                            # Calculate total for database save
                            customer_name = self.company_var.get().strip()
                            if customer_name and self.current_quote_number:
                                if self.db_manager.connect():
                                    # At this point current_quote_number is guaranteed to be set
                                    assert self.current_quote_number is not None
                                    
                                    db_save_success = self.db_manager.save_quote(
                                        quote_number=self.current_quote_number,
                                        customer_name=customer_name,
                                        customer_email=self.email_var.get().strip(),
                                        quote_items=self.quote_items,
                                        total_price=total_quote_value,
                                        user_initials=user_initials
                                    )
                                    
                                    if db_save_success:
                                        self.status_var.set(f"Quote {self.current_quote_number} exported and saved to database")
                                    else:
                                        self.status_var.set(f"Quote {self.current_quote_number} exported (database save failed)")
                                    
                                    self.db_manager.disconnect()
                        except Exception as db_error:
                            print(f"Database save error: {db_error}")
                            # Don't show error to user since export was successful
                        
                        messagebox.showinfo("Export Success", f"Complete quote exported to:\n{filename}\n\nQuote Number: {self.current_quote_number}")
                        quote_window.destroy()
                    else:
                        messagebox.showerror("Export Error", "Failed to export quote using all available methods.")
                    
            except Exception as e:
                print(f"Export error: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Export Error", f"Failed to export quote:\n{str(e)}")
        
        ttk.Button(button_frame, text="Remove Selected", command=remove_selected_item).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Clear Quote", command=clear_quote).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export Quote", command=export_full_quote).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", command=quote_window.destroy).pack(side=tk.RIGHT)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

    def parse_spare_part(self):
        """Parse spare part number and show information"""
        spare_part_number = self.spare_part_var.get().strip()
        
        if not spare_part_number:
            messagebox.showwarning("Input Required", "Please enter a spare part number to parse.")
            return
        
        try:
            self.status_var.set("Parsing spare part...")
            self.root.update()
            
            # First, try to process as a shortcut
            expanded_spare_part = self.process_shortcut_input(spare_part_number)
            if expanded_spare_part != spare_part_number:
                # Shortcut was expanded, update the input field to show the full part number
                self.spare_part_var.set(expanded_spare_part)
                self.status_var.set(f"Expanded shortcut '{spare_part_number}' to '{expanded_spare_part}'")
                self.root.update()
                spare_part_number = expanded_spare_part
            
            # Use spare parts manager to parse the part (original or expanded)
            result = self.spare_parts_manager.parse_and_quote_spare_part(spare_part_number)
            
            if result.get('error'):
                self.status_var.set("Parse failed")
                messagebox.showerror("Parse Error", f"Failed to parse spare part:\n{result['error']}")
                return
            
            self.status_var.set(f"Spare part parsed successfully: {result.get('description', 'N/A')}")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred while parsing spare part:\n{str(e)}")
    
    def edit_quote_item(self):
        """Edit selected quote item"""
        selection = self.quote_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to edit.")
            return
        
        # Get selected item
        item_id = selection[0]
        item_values = self.quote_tree.item(item_id, 'values')
        
        if not item_values:
            return
        
        # For now, just show a message - detailed editing can be implemented later
        messagebox.showinfo("Edit Item", f"Editing functionality for {item_values[1]} will be implemented in a future version.")
    
    def remove_quote_item(self):
        """Remove selected quote item"""
        selection = self.quote_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return
        
        # Get selected item
        item_id = selection[0]
        item_values = self.quote_tree.item(item_id, 'values')
        
        if not item_values:
            return
        
        # Confirm removal
        if messagebox.askyesno("Remove Item", f"Remove {item_values[1]} from quote?"):
            # Remove from treeview
            self.quote_tree.delete(item_id)
            
            # Remove from quote_items list (find by part number)
            part_number = item_values[1]
            self.quote_items = [item for item in self.quote_items if item.get('part_number') != part_number]
            
            # Update total
            self.update_quote_total()
            
            self.status_var.set(f"Removed {part_number} from quote")
    
    def clear_quote(self):
        """Clear all items from quote"""
        if not self.quote_items:
            messagebox.showinfo("Empty Quote", "Quote is already empty.")
            return
        
        if messagebox.askyesno("Clear Quote", "Are you sure you want to clear all items from the quote?"):
            # Clear treeview
            for item in self.quote_tree.get_children():
                self.quote_tree.delete(item)
            
            # Clear quote items list
            self.quote_items.clear()
            
            # Update total
            self.update_quote_total()
            
            self.status_var.set("Quote cleared")
    
    def update_quote_total(self):
        """Update the total quote value display"""
        total_value = 0.0
        
        for item in self.quote_items:
            if item['type'] == 'main':
                unit_price = item['data'].get('total_price', 0.0)
            else:  # spare part
                unit_price = item['data'].get('pricing', {}).get('total_price', 0.0)
            
            quantity = item.get('quantity', 1)
            total_value += unit_price * quantity
        
        self.total_label.config(text=f"Total: ${total_value:.2f}")
    
    def update_quote_number_display(self):
        """Update the quote number display"""
        if self.current_quote_number:
            self.quote_number_label.config(text=f"Quote #: {self.current_quote_number}")
        else:
            self.quote_number_label.config(text="Quote #: Not Generated")
    
    def generate_new_quote_number(self) -> bool:
        """Generate a new quote number based on user initials. Returns True if successful."""
        user_initials = self.initials_var.get().strip()
        
        if not user_initials:
            messagebox.showerror("Initials Required", "Please enter your initials before generating a quote number.")
            return False
        
        if len(user_initials) < 2:
            messagebox.showerror("Invalid Initials", "Please enter at least 2 characters for your initials.")
            return False
        
        try:
            # Connect to database and generate quote number
            if not self.db_manager.connect():
                messagebox.showerror("Database Error", "Could not connect to database to generate quote number.")
                return False
            
            self.current_quote_number = self.db_manager.generate_quote_number(user_initials)
            self.update_quote_number_display()
            
            self.status_var.set(f"Generated quote number: {self.current_quote_number}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate quote number: {str(e)}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def add_to_quote_tree(self, item_type, part_number, description, quantity, unit_price, total_price):
        """Add an item to the quote tree display"""
        self.quote_tree.insert("", "end", values=(
            item_type.upper(),
            part_number,
            description,
            quantity,
            f"${unit_price:.2f}",
            f"${total_price:.2f}"
        ))
        
        # Update total
        self.update_quote_total()

    def show_part_details_popup(self, quote_item: Dict[str, Any], parent_window: Union[tk.Tk, tk.Toplevel]):
        """Show detailed part information in a popup window"""
        # Create details popup window
        details_window = tk.Toplevel(parent_window)
        details_window.title(f"Part Details - {quote_item['part_number']}")
        details_window.geometry("800x700")
        details_window.transient(parent_window)
        details_window.grab_set()
        
        # Center the window
        details_window.update_idletasks()
        x = parent_window.winfo_x() + (parent_window.winfo_width() // 2) - 400
        y = parent_window.winfo_y() + (parent_window.winfo_height() // 2) - 350
        details_window.geometry(f"800x700+{x}+{y}")
        
        # Create content frame
        main_frame = ttk.Frame(details_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Detailed Information: {quote_item['part_number']}", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Create notebook for different data categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Basic Info Tab
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Basic Info")
        self._create_basic_info_tab(basic_frame, quote_item)
        
        # Technical Specs Tab
        specs_frame = ttk.Frame(notebook)
        notebook.add(specs_frame, text="Technical Specs")
        self._create_technical_specs_tab(specs_frame, quote_item)
        
        # Pricing Breakdown Tab
        pricing_frame = ttk.Frame(notebook)
        notebook.add(pricing_frame, text="Pricing Breakdown")
        self._create_pricing_breakdown_tab(pricing_frame, quote_item)
        
        # Raw Data Tab
        raw_data_frame = ttk.Frame(notebook)
        notebook.add(raw_data_frame, text="Raw Data")
        self._create_raw_data_tab(raw_data_frame, quote_item)
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=details_window.destroy)
        close_button.pack(pady=(10, 0))
    
    def _create_basic_info_tab(self, parent: ttk.Frame, quote_item: Dict[str, Any]):
        """Create basic information tab"""
        data = quote_item.get('data', {})
        
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add basic information
        ttk.Label(scrollable_frame, text="Quote Item Information", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        basic_info = [
            ("Part Number:", quote_item.get('part_number', 'N/A')),
            ("Item Type:", quote_item.get('type', 'N/A').upper()),
            ("Customer:", quote_item.get('customer_name', 'N/A')),
            ("Quantity:", str(quote_item.get('quantity', 1))),
            ("Added to Quote:", quote_item.get('timestamp', 'N/A')),
            ("", ""),  # Spacer
            ("Product Information", ""),
            ("Model:", data.get('model', 'N/A')),
            ("Voltage:", data.get('voltage', 'N/A')),
            ("Probe Material:", data.get('probe_material_name', data.get('probe_material', 'N/A'))),
            ("Probe Length:", f"{data.get('probe_length', 'N/A')}\"" if data.get('probe_length') else 'N/A'),
            ("Probe Diameter:", data.get('probe_diameter', 'N/A')),
            ("Process Connection:", data.get('process_connection', 'N/A')),
            ("Housing:", data.get('housing', 'N/A')),
            ("Output:", data.get('output', 'N/A')),
        ]
        
        row = 1
        for label, value in basic_info:
            if label == "":  # Spacer
                row += 1
                continue
            elif value == "":  # Section header
                ttk.Label(scrollable_frame, text=label, font=("Arial", 11, "bold")).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
            else:
                ttk.Label(scrollable_frame, text=label, font=("Arial", 9, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 10))
                ttk.Label(scrollable_frame, text=str(value), font=("Arial", 9)).grid(row=row, column=1, sticky="w")
            row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_technical_specs_tab(self, parent: ttk.Frame, quote_item: Dict[str, Any]):
        """Create technical specifications tab"""
        data = quote_item.get('data', {})
        
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add technical specifications
        ttk.Label(scrollable_frame, text="Technical Specifications", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        specs = [
            ("Operating Limits", ""),
            ("Max Temperature:", f"{data.get('max_temperature', 'N/A')}°F" if data.get('max_temperature') else 'N/A'),
            ("Max Pressure:", f"{data.get('max_pressure', 'N/A')} PSI" if data.get('max_pressure') else 'N/A'),
            ("", ""),
            ("Insulator Information", ""),
            ("Insulator Display:", data.get('insulator', 'N/A')),
            ("Base Insulator Length:", f"{data.get('base_insulator_length', 'N/A')}\"" if data.get('base_insulator_length') else 'N/A'),
            ("Insulator Material:", data.get('insulator_material', 'N/A')),
            ("", ""),
            ("Options & Warnings", ""),
        ]
        
        # Add options
        options = data.get('options', [])
        if options:
            for option in options:
                specs.append((f"Option:", option))
        else:
            specs.append(("Options:", "None"))
        
        specs.append(("", ""))
        
        # Add warnings
        warnings = data.get('warnings', [])
        if warnings:
            for warning in warnings:
                specs.append((f"Warning:", warning))
        else:
            specs.append(("Warnings:", "None"))
        
        # Add errors
        errors = data.get('errors', [])
        if errors:
            specs.append(("", ""))
            for error in errors:
                specs.append((f"Error:", error))
        
        row = 1
        for label, value in specs:
            if label == "":  # Spacer
                row += 1
                continue
            elif value == "":  # Section header
                ttk.Label(scrollable_frame, text=label, font=("Arial", 11, "bold")).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
            else:
                ttk.Label(scrollable_frame, text=label, font=("Arial", 9, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 10))
                ttk.Label(scrollable_frame, text=str(value), font=("Arial", 9)).grid(row=row, column=1, sticky="w")
            row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_pricing_breakdown_tab(self, parent: ttk.Frame, quote_item: Dict[str, Any]):
        """Create pricing breakdown tab"""
        data = quote_item.get('data', {})
        
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add pricing information
        ttk.Label(scrollable_frame, text="Pricing Breakdown", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        pricing = [
            ("Base Price:", f"${data.get('base_price', 0):.2f}"),
            ("Length Cost:", f"${data.get('length_cost', 0):.2f}"),
            ("Length Surcharge:", f"${data.get('length_surcharge', 0):.2f}"),
            ("Option Cost:", f"${data.get('option_cost', 0):.2f}"),
            ("Insulator Cost:", f"${data.get('insulator_cost', 0):.2f}"),
            ("Connection Cost:", f"${data.get('connection_cost', 0):.2f}"),
            ("", ""),
            ("Unit Total:", f"${data.get('total_price', 0):.2f}"),
            ("Quantity:", str(quote_item.get('quantity', 1))),
            ("Line Total:", f"${data.get('total_price', 0) * quote_item.get('quantity', 1):.2f}"),
        ]
        
        row = 1
        for label, value in pricing:
            if label == "":  # Spacer
                row += 1
                continue
            elif label in ["Unit Total:", "Line Total:"]:  # Highlight totals
                ttk.Label(scrollable_frame, text=label, font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 10))
                ttk.Label(scrollable_frame, text=str(value), font=("Arial", 10, "bold")).grid(row=row, column=1, sticky="w")
            else:
                ttk.Label(scrollable_frame, text=label, font=("Arial", 9, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 10))
                ttk.Label(scrollable_frame, text=str(value), font=("Arial", 9)).grid(row=row, column=1, sticky="w")
            row += 1
        
        # Add price breakdown if available
        price_breakdown = data.get('price_breakdown', [])
        if price_breakdown:
            ttk.Label(scrollable_frame, text="Detailed Breakdown:", font=("Arial", 11, "bold")).grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="w")
            row += 1
            for item in price_breakdown:
                ttk.Label(scrollable_frame, text=str(item), font=("Arial", 9)).grid(row=row, column=0, columnspan=2, sticky="w", padx=(10, 0))
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_raw_data_tab(self, parent: ttk.Frame, quote_item: Dict[str, Any]):
        """Create raw data tab showing all parsed data"""
        # Create text widget with scrollbar
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 9))
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        # Add raw data
        import json
        raw_data_text = "QUOTE ITEM RAW DATA\n"
        raw_data_text += "=" * 50 + "\n\n"
        raw_data_text += json.dumps(quote_item, indent=2, default=str)
        
        text_widget.insert(tk.END, raw_data_text)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

if __name__ == "__main__":
    app = MainWindow()
    app.run() 
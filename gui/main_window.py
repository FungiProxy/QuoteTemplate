"""
Main Application Window for Babbitt Quote Generator
Provides the primary user interface for the application
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, 
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, SAMPLE_PART_NUMBERS,
    ERROR_MESSAGES, SUCCESS_MESSAGES
)
from core.part_parser import PartNumberParser
from core.quote_generator import QuoteGenerator
from .quote_display import QuoteDisplayWidget
from .dialogs import AboutDialog, SettingsDialog, ExportDialog

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.parser = PartNumberParser()
        self.quote_generator = QuoteGenerator()
        self.current_quote_data = None
        
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
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Part Number Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Part number entry
        ttk.Label(input_frame, text="Part Number:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.part_number_var = tk.StringVar()
        self.part_number_entry = ttk.Entry(input_frame, textvariable=self.part_number_var, font=("Consolas", 12))
        self.part_number_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Parse button
        self.parse_button = ttk.Button(input_frame, text="Parse & Price", command=self.parse_part_number)
        self.parse_button.grid(row=0, column=2, padx=(0, 10))
        
        # Sample button
        self.sample_button = ttk.Button(input_frame, text="Samples", command=self.show_samples)
        self.sample_button.grid(row=0, column=3)
        
        # Customer info section
        customer_frame = ttk.LabelFrame(main_frame, text="Customer Information", padding="10")
        customer_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        customer_frame.columnconfigure(1, weight=1)
        customer_frame.columnconfigure(3, weight=1)
        
        # Customer name
        ttk.Label(customer_frame, text="Customer:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.customer_var = tk.StringVar(value="New Customer")
        customer_entry = ttk.Entry(customer_frame, textvariable=self.customer_var)
        customer_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Quantity
        ttk.Label(customer_frame, text="Quantity:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(customer_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Results section
        self.quote_display = QuoteDisplayWidget(main_frame)
        self.quote_display.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Store references to main widgets
        self.main_frame = main_frame
        self.input_frame = input_frame
        self.customer_frame = customer_frame
    
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
        
        # Enter key to parse part number
        self.part_number_entry.bind('<Return>', lambda e: self.parse_part_number())
        
        # Window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def parse_part_number(self):
        """Parse the entered part number and display results"""
        part_number = self.part_number_var.get().strip()
        
        if not part_number:
            messagebox.showwarning("Input Required", "Please enter a part number to parse.")
            return
        
        try:
            self.status_var.set("Parsing part number...")
            self.root.update()
            
            # Parse the part number
            parsed_result = self.parser.parse_part_number(part_number)
            
            if parsed_result.get('error'):
                self.status_var.set("Parse failed")
                messagebox.showerror("Parse Error", f"Failed to parse part number:\n{parsed_result['error']}")
                return
            
            # Generate quote data
            self.current_quote_data = self.parser.get_quote_data(parsed_result)
            
            # Update display
            self.quote_display.update_display(self.current_quote_data)
            
            # Update status
            total_price = self.current_quote_data.get('total_price', 0)
            self.status_var.set(f"Part parsed successfully - Total: ${total_price:.2f}")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred while parsing:\n{str(e)}")
    
    def export_quote(self):
        """Export current quote to Word document"""
        if not self.current_quote_data:
            messagebox.showwarning("No Quote", "Please parse a part number first.")
            return
        
        try:
            # Show export dialog
            dialog = ExportDialog(self.root, self.current_quote_data)
            if dialog.result:
                export_path = dialog.result.get('file_path')
                if export_path:
                    self.status_var.set("Exporting quote...")
                    self.root.update()
                    
                    # Generate quote with customer info
                    customer_info = {
                        'customer_name': self.customer_var.get(),
                        'quantity': int(self.quantity_var.get() or 1)
                    }
                    
                    # Export to Word
                    output_path = self.quote_generator.generate_quote(
                        self.current_quote_data, 
                        output_path=export_path,
                        customer_info=customer_info
                    )
                    
                    self.status_var.set(f"Quote exported to {output_path}")
                    messagebox.showinfo("Export Success", f"Quote exported successfully to:\n{output_path}")
                    
        except Exception as e:
            self.status_var.set("Export failed")
            messagebox.showerror("Export Error", f"Failed to export quote:\n{str(e)}")
    
    def new_quote(self):
        """Start a new quote"""
        self.part_number_var.set("")
        self.customer_var.set("New Customer")
        self.quantity_var.set("1")
        self.current_quote_data = None
        self.quote_display.clear_display()
        self.status_var.set("Ready for new quote")
    
    def open_quote(self):
        """Open an existing quote (placeholder)"""
        messagebox.showinfo("Feature Not Available", "Open quote functionality will be implemented in a future version.")
    
    def save_quote(self):
        """Save current quote (placeholder)"""
        if not self.current_quote_data:
            messagebox.showwarning("No Quote", "Please parse a part number first.")
            return
        messagebox.showinfo("Feature Not Available", "Save quote functionality will be implemented in a future version.")
    
    def clear_part_number(self):
        """Clear part number entry"""
        self.part_number_var.set("")
        self.part_number_entry.focus()
    
    def clear_results(self):
        """Clear results display"""
        self.current_quote_data = None
        self.quote_display.clear_display()
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
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run() 
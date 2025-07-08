#!/usr/bin/env python3
"""
Babbitt Quote Generator - Main Application
Simple quote generator for Babbitt International products
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from database.db_manager import DatabaseManager
    from core.part_parser import PartNumberParser
    from core.quote_generator import QuoteGenerator
except ImportError as e:
    print(f"Import error: {e}")
    print("Creating minimal application without full functionality")
    
    # Create dummy classes for basic functionality
    class DatabaseManager:
        def test_connection(self):
            return False
    
    class PartNumberParser:
        def parse_part_number(self, pn):
            return {'original_part_number': pn, 'error': 'Parser not available'}
    
    class QuoteGenerator:
        def generate_quote(self, data):
            return False

class BabbittQuoteGenerator:
    def __init__(self):
        """Initialize the main application"""
        self.root = tk.Tk()
        self.root.title("Babbitt Quote Generator - v1.0")
        self.root.geometry("800x600")
        
        # Initialize components
        self.db = DatabaseManager()
        self.parser = PartNumberParser()
        self.quote_gen = QuoteGenerator()
        
        # Current parsed data
        self.current_data = None
        
        # Setup GUI
        self.setup_gui()
        
        # Check database connection
        self.check_database_connection()
    
    def setup_gui(self):
        """Create the main GUI interface"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Babbitt Quote Generator", 
                              font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Part Number Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Part Number Entry", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)
        
        # Part number input
        ttk.Label(input_frame, text="Part Number:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.part_entry = ttk.Entry(input_frame, width=50, font=("Consolas", 10))
        self.part_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.part_entry.bind('<Return>', self.on_parse_part)
        
        parse_button = ttk.Button(input_frame, text="Parse & Generate", command=self.on_parse_part)
        parse_button.grid(row=0, column=2, padx=(10, 0))
        
        # Example
        example_label = ttk.Label(input_frame, text="Example: LS2000-115VAC-S-10\"-XSP-VR-8\"TEFINS", 
                                font=("Arial", 8), foreground="gray")
        example_label.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Configuration Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        results_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Results display
        self.results_text = tk.Text(results_frame, height=15, width=80, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        results_frame.rowconfigure(0, weight=1)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        export_button = ttk.Button(button_frame, text="Export to Word", command=self.export_quote)
        export_button.grid(row=0, column=0, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_results)
        clear_button.grid(row=0, column=1, padx=(0, 10))
        
        test_db_button = ttk.Button(button_frame, text="Test Database", command=self.test_database)
        test_db_button.grid(row=0, column=2, padx=(0, 10))
        
        price_button = ttk.Button(button_frame, text="Calculate Price Only", command=self.calculate_price_only)
        price_button.grid(row=0, column=3, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Add some sample part numbers for testing
        self.add_sample_parts()
    
    def add_sample_parts(self):
        """Add sample part numbers to the interface"""
        sample_frame = ttk.LabelFrame(self.root, text="Sample Part Numbers", padding="5")
        sample_frame.place(x=10, y=450, width=780, height=100)
        
        samples = [
            "LS2000-115VAC-S-10\"",
            "LS2000-115VAC-S-10\"-XSP-VR",
            "LS2100-24VDC-H-12\"",
            "LS6000-115VAC-S-14\"-1\"NPT"
        ]
        
        for i, sample in enumerate(samples):
            btn = ttk.Button(sample_frame, text=sample, 
                           command=lambda s=sample: self.load_sample(s))
            btn.grid(row=i//2, column=i%2, padx=5, pady=2, sticky=tk.W)
    
    def load_sample(self, sample_part):
        """Load a sample part number"""
        self.part_entry.delete(0, tk.END)
        self.part_entry.insert(0, sample_part)
        self.on_parse_part()
    
    def check_database_connection(self):
        """Check if database is connected"""
        try:
            if self.db.test_connection():
                self.status_var.set("Database connected")
            else:
                self.status_var.set("Database not found - limited functionality")
        except:
            self.status_var.set("Database error - using demo mode")
    
    def on_parse_part(self, event=None):
        """Handle part number parsing"""
        part_number = self.part_entry.get().strip()
        
        if not part_number:
            messagebox.showwarning("Warning", "Please enter a part number")
            return
        
        self.status_var.set("Parsing part number...")
        self.root.update()
        
        try:
            # Parse the part number
            parsed_data = self.parser.parse_part_number(part_number)
            self.current_data = parsed_data
            
            # Display results
            self.display_results(parsed_data)
            self.status_var.set("Part number parsed successfully")
            
        except Exception as e:
            self.status_var.set(f"Error parsing part number: {str(e)}")
            messagebox.showerror("Error", f"Failed to parse part number:\n{str(e)}")
    
    def display_results(self, data: Dict[str, Any]):
        """Display parsed results in the text area"""
        self.results_text.delete(1.0, tk.END)
        
        if data.get('error'):
            self.results_text.insert(tk.END, f"❌ ERROR: {data['error']}\n\n")
            return
        
        # Header
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, f"QUOTE CONFIGURATION FOR: {data.get('original_part_number', 'N/A')}\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Basic specifications
        self.results_text.insert(tk.END, "BASIC SPECIFICATIONS:\n")
        self.results_text.insert(tk.END, "-" * 25 + "\n")
        self.results_text.insert(tk.END, f"Model:              {data.get('model', 'N/A')}\n")
        self.results_text.insert(tk.END, f"Voltage:            {data.get('voltage', 'N/A')}\n")
        self.results_text.insert(tk.END, f"Probe Material:     {data.get('probe_material_name', 'N/A')}\n")
        self.results_text.insert(tk.END, f"Probe Length:       {data.get('probe_length', 'N/A')}\"\n")
        self.results_text.insert(tk.END, f"Housing:            {data.get('housing_type', 'N/A')}\n")
        self.results_text.insert(tk.END, f"Output:             {data.get('output_type', 'N/A')}\n\n")
        
        # Process Connection
        self.results_text.insert(tk.END, "PROCESS CONNECTION:\n")
        self.results_text.insert(tk.END, "-" * 20 + "\n")
        
        if data.get('process_connection'):
            conn = data['process_connection']
            self.results_text.insert(tk.END, f"Type:               {conn.get('type', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Size:               {conn.get('size', 'N/A')}\n")
            if conn.get('rating'):
                self.results_text.insert(tk.END, f"Rating:             {conn.get('rating', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Material:           {data.get('process_connection_material', 'N/A')}\n")
        else:
            self.results_text.insert(tk.END, f"Type:               {data.get('process_connection_type', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Size:               {data.get('process_connection_size', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Material:           {data.get('process_connection_material', 'N/A')}\n")
        
        self.results_text.insert(tk.END, "\n")
        
        # Insulator
        self.results_text.insert(tk.END, "INSULATOR:\n")
        self.results_text.insert(tk.END, "-" * 10 + "\n")
        
        if data.get('insulator'):
            ins = data['insulator']
            self.results_text.insert(tk.END, f"Material:           {ins.get('material_name', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Length:             {ins.get('length', 'N/A')}\"\n")
        else:
            self.results_text.insert(tk.END, f"Material:           {data.get('insulator_material', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Length:             {data.get('insulator_length', 'N/A')}\"\n")
        
        self.results_text.insert(tk.END, "\n")
        
        # Operating Limits
        self.results_text.insert(tk.END, "OPERATING LIMITS:\n")
        self.results_text.insert(tk.END, "-" * 17 + "\n")
        self.results_text.insert(tk.END, f"Max Temperature:    {data.get('max_temperature', 'N/A')}°F\n")
        self.results_text.insert(tk.END, f"Max Pressure:       {data.get('max_pressure', 'N/A')} PSI\n")
        self.results_text.insert(tk.END, f"O-Ring Material:    {data.get('oring_material', 'N/A')}\n\n")
        
        # Options
        options = data.get('options', [])
        if options:
            self.results_text.insert(tk.END, "OPTIONS:\n")
            self.results_text.insert(tk.END, "-" * 8 + "\n")
            for option in options:
                self.results_text.insert(tk.END, f"• {option.get('code', 'N/A')}: {option.get('name', 'N/A')}\n")
            self.results_text.insert(tk.END, "\n")
        
        # Warnings
        warnings = data.get('warnings', [])
        if warnings:
            self.results_text.insert(tk.END, "⚠️  WARNINGS:\n")
            self.results_text.insert(tk.END, "-" * 11 + "\n")
            for warning in warnings:
                self.results_text.insert(tk.END, f"• {warning}\n")
            self.results_text.insert(tk.END, "\n")
        
        # Errors
        errors = data.get('errors', [])
        if errors:
            self.results_text.insert(tk.END, "❌ ERRORS:\n")
            self.results_text.insert(tk.END, "-" * 9 + "\n")
            for error in errors:
                self.results_text.insert(tk.END, f"• {error}\n")
            self.results_text.insert(tk.END, "\n")
        
        # Pricing Information
        pricing = data.get('pricing', {})
        if pricing and pricing.get('success', True):
            self.results_text.insert(tk.END, "💰 PRICING BREAKDOWN:\n")
            self.results_text.insert(tk.END, "-" * 19 + "\n")
            
            # Show individual pricing components
            if pricing.get('base_price', 0) > 0:
                self.results_text.insert(tk.END, f"Base Price:         ${pricing['base_price']:.2f}\n")
            if pricing.get('length_cost', 0) > 0:
                self.results_text.insert(tk.END, f"Length Cost:        ${pricing['length_cost']:.2f}\n")
            if pricing.get('length_surcharge', 0) > 0:
                self.results_text.insert(tk.END, f"Length Surcharge:   ${pricing['length_surcharge']:.2f}\n")
            if pricing.get('option_cost', 0) > 0:
                self.results_text.insert(tk.END, f"Options:            ${pricing['option_cost']:.2f}\n")
            if pricing.get('insulator_cost', 0) > 0:
                self.results_text.insert(tk.END, f"Insulator:          ${pricing['insulator_cost']:.2f}\n")
            if pricing.get('connection_cost', 0) > 0:
                self.results_text.insert(tk.END, f"Process Connection: ${pricing['connection_cost']:.2f}\n")
            
            self.results_text.insert(tk.END, "-" * 19 + "\n")
            self.results_text.insert(tk.END, f"TOTAL PRICE:        ${pricing.get('total_price', 0):.2f}\n\n")
            
            # Show detailed breakdown if available
            breakdown = pricing.get('breakdown', [])
            if breakdown:
                self.results_text.insert(tk.END, "Detailed Breakdown:\n")
                for item in breakdown:
                    self.results_text.insert(tk.END, f"  {item}\n")
                self.results_text.insert(tk.END, "\n")
        
        # Footer
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "Quote generated by Babbitt Quote Generator v1.0\n")
    
    def export_quote(self):
        """Export the current quote to Word document"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No quote data to export. Please parse a part number first.")
            return
        
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word documents", "*.docx"), ("All files", "*.*")],
                title="Save Quote As"
            )
            
            if filename:
                self.status_var.set("Exporting quote...")
                self.root.update()
                
                # Generate quote document
                success = self.quote_gen.generate_quote(self.current_data, filename)
                
                if success:
                    self.status_var.set(f"Quote exported to {filename}")
                    messagebox.showinfo("Success", f"Quote exported successfully to:\n{filename}")
                else:
                    self.status_var.set("Export failed")
                    messagebox.showerror("Error", "Failed to export quote")
        
        except Exception as e:
            self.status_var.set(f"Export error: {str(e)}")
            messagebox.showerror("Error", f"Failed to export quote:\n{str(e)}")
    
    def clear_results(self):
        """Clear the results area"""
        self.results_text.delete(1.0, tk.END)
        self.part_entry.delete(0, tk.END)
        self.current_data = None
        self.status_var.set("Ready")
    
    def test_database(self):
        """Test database connection"""
        try:
            if self.db.test_connection():
                messagebox.showinfo("Database Test", "✓ Database connection successful!")
            else:
                messagebox.showwarning("Database Test", "❌ Database connection failed!")
        except Exception as e:
            messagebox.showerror("Database Test", f"Database error:\n{str(e)}")
    
    def calculate_price_only(self):
        """Calculate and display only pricing information"""
        part_number = self.part_entry.get().strip()
        
        if not part_number:
            messagebox.showwarning("Warning", "Please enter a part number")
            return
        
        self.status_var.set("Calculating price...")
        self.root.update()
        
        try:
            # Parse the part number to get pricing
            parsed_data = self.parser.parse_part_number(part_number)
            
            # Clear results and show only pricing
            self.results_text.delete(1.0, tk.END)
            
            if parsed_data.get('error'):
                self.results_text.insert(tk.END, f"❌ ERROR: {parsed_data['error']}\n\n")
                return
            
            # Header
            self.results_text.insert(tk.END, "=" * 60 + "\n")
            self.results_text.insert(tk.END, f"PRICE CALCULATION FOR: {parsed_data.get('original_part_number', 'N/A')}\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n\n")
            
            # Show pricing information
            pricing = parsed_data.get('pricing', {})
            if pricing and pricing.get('success', True):
                self.results_text.insert(tk.END, "💰 PRICING BREAKDOWN:\n")
                self.results_text.insert(tk.END, "-" * 19 + "\n")
                
                # Show individual pricing components
                if pricing.get('base_price', 0) > 0:
                    self.results_text.insert(tk.END, f"Base Price:         ${pricing['base_price']:.2f}\n")
                if pricing.get('length_cost', 0) > 0:
                    self.results_text.insert(tk.END, f"Length Cost:        ${pricing['length_cost']:.2f}\n")
                if pricing.get('length_surcharge', 0) > 0:
                    self.results_text.insert(tk.END, f"Length Surcharge:   ${pricing['length_surcharge']:.2f}\n")
                if pricing.get('option_cost', 0) > 0:
                    self.results_text.insert(tk.END, f"Options:            ${pricing['option_cost']:.2f}\n")
                if pricing.get('insulator_cost', 0) > 0:
                    self.results_text.insert(tk.END, f"Insulator:          ${pricing['insulator_cost']:.2f}\n")
                if pricing.get('connection_cost', 0) > 0:
                    self.results_text.insert(tk.END, f"Process Connection: ${pricing['connection_cost']:.2f}\n")
                
                self.results_text.insert(tk.END, "-" * 19 + "\n")
                self.results_text.insert(tk.END, f"TOTAL PRICE:        ${pricing.get('total_price', 0):.2f}\n\n")
                
                # Show detailed breakdown if available
                breakdown = pricing.get('breakdown', [])
                if breakdown:
                    self.results_text.insert(tk.END, "Detailed Breakdown:\n")
                    for item in breakdown:
                        self.results_text.insert(tk.END, f"  {item}\n")
                    self.results_text.insert(tk.END, "\n")
            else:
                self.results_text.insert(tk.END, "❌ Pricing calculation failed\n\n")
            
            self.results_text.insert(tk.END, "=" * 60 + "\n")
            self.status_var.set("Price calculated successfully")
            
        except Exception as e:
            self.status_var.set(f"Error calculating price: {str(e)}")
            messagebox.showerror("Error", f"Failed to calculate price:\n{str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("Starting Babbitt Quote Generator...")
    
    # Check if running from correct directory
    if not os.path.exists("database") and not os.path.exists("quotes.db"):
        print("⚠️  Warning: Database directory not found.")
        print("   Make sure you're running from the project root directory.")
        print("   The application will run in demo mode.")
    
    try:
        app = BabbittQuoteGenerator()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
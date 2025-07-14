#!/usr/bin/env python3
"""
Test script to verify button styling changes
"""

import tkinter as tk
from tkinter import ttk

def test_button_styling():
    """Test the new button styling"""
    root = tk.Tk()
    root.title("Button Styling Test")
    root.geometry("600x400")
    
    # Create a frame
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Test Parse button styling
    parse_button = tk.Button(frame, text="🔍 PARSE & PRICE", 
                           font=("Arial", 10, "bold"),
                           bg="#2E7D32", fg="white",
                           relief=tk.RAISED, bd=2,
                           padx=10, pady=3)
    parse_button.pack(pady=10)
    
    # Test Add to Quote button styling
    add_button = tk.Button(frame, text="➕ ADD TO QUOTE", 
                          font=("Arial", 10, "bold"),
                          bg="#1565C0", fg="white",
                          relief=tk.RAISED, bd=2,
                          padx=10, pady=3)
    add_button.pack(pady=10)
    
    # Test Export button styling
    export_button = tk.Button(frame, text="📄 EXPORT QUOTE", 
                             font=("Arial", 10, "bold"),
                             bg="#E65100", fg="white",
                             relief=tk.RAISED, bd=2,
                             padx=10, pady=3)
    export_button.pack(pady=10)
    
    # Add hover effects
    def on_parse_enter(e):
        parse_button.config(bg="#1B5E20", relief=tk.SUNKEN)
    
    def on_parse_leave(e):
        parse_button.config(bg="#2E7D32", relief=tk.RAISED)
    
    parse_button.bind('<Enter>', on_parse_enter)
    parse_button.bind('<Leave>', on_parse_leave)
    
    def on_add_enter(e):
        add_button.config(bg="#0D47A1", relief=tk.SUNKEN)
    
    def on_add_leave(e):
        add_button.config(bg="#1565C0", relief=tk.RAISED)
    
    add_button.bind('<Enter>', on_add_enter)
    add_button.bind('<Leave>', on_add_leave)
    
    def on_export_enter(e):
        export_button.config(bg="#BF360C", relief=tk.SUNKEN)
    
    def on_export_leave(e):
        export_button.config(bg="#E65100", relief=tk.RAISED)
    
    export_button.bind('<Enter>', on_export_enter)
    export_button.bind('<Leave>', on_export_leave)
    
    # Add click feedback
    def on_parse_click(e):
        original_bg = parse_button.cget('bg')
        parse_button.config(bg="#1B5E20")
        root.after(150, lambda: parse_button.config(bg=original_bg))
    
    def on_add_click(e):
        original_bg = add_button.cget('bg')
        add_button.config(bg="#0D47A1")
        root.after(150, lambda: add_button.config(bg=original_bg))
    
    def on_export_click(e):
        original_bg = export_button.cget('bg')
        export_button.config(bg="#BF360C")
        root.after(150, lambda: export_button.config(bg=original_bg))
    
    parse_button.bind('<Button-1>', on_parse_click)
    add_button.bind('<Button-1>', on_add_click)
    export_button.bind('<Button-1>', on_export_click)
    
    # Add instructions
    instruction_label = ttk.Label(frame, text="Test the buttons above:\n• Hover over them to see color changes\n• Click them to see feedback effects\n• Notice the bold text and icons", 
                                font=("Arial", 10), justify=tk.CENTER)
    instruction_label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_button_styling() 
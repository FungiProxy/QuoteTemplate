"""
Auto-complete functionality for part number input
Provides suggestions as user types based on database content and aliases
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional, Callable
from database.db_manager import DatabaseManager

class AutocompleteEntry(ttk.Entry):
    """Enhanced Entry widget with auto-complete functionality"""
    
    def __init__(self, parent, db_manager: DatabaseManager, **kwargs):
        super().__init__(parent, **kwargs)
        self.db_manager = db_manager
        self.suggestions = []
        self.suggestion_window = None
        self.suggestion_listbox = None
        self.current_section = 0  # Track which section of part number we're in
        
        # Bind events
        self.bind('<KeyRelease>', self.on_key_release)
        self.bind('<KeyPress>', self.on_key_press)
        self.bind('<FocusOut>', self.hide_suggestions)
        self.bind('<Return>', self.on_return)
        self.bind('<Tab>', self.on_tab)
        self.bind('<Escape>', self.hide_suggestions)
        
        # Callback for when a suggestion is selected
        self.on_suggestion_selected = None
    
    def set_suggestion_callback(self, callback: Callable[[str], None]):
        """Set callback function to be called when a suggestion is selected"""
        self.on_suggestion_selected = callback
    
    def on_key_release(self, event):
        """Handle key release events"""
        if event.keysym in ['Up', 'Down', 'Return', 'Tab', 'Escape']:
            return
        
        # Get current cursor position and text
        cursor_pos = self.index(tk.INSERT)
        text = self.get()
        
        # Determine which section we're in
        self.current_section = self._get_section_at_cursor(text, cursor_pos)
        
        # Get suggestions for current section
        current_word = self._get_current_word(text, cursor_pos)
        if len(current_word) >= 1:  # Show suggestions after 1 character
            self.show_suggestions(current_word)
        else:
            self.hide_suggestions()
    
    def on_key_press(self, event):
        """Handle key press events for navigation"""
        if not self.suggestion_window or not self.suggestion_listbox:
            return
        
        if event.keysym == 'Up':
            self._select_previous()
            return 'break'
        elif event.keysym == 'Down':
            self._select_next()
            return 'break'
    
    def on_return(self, event):
        """Handle Return key"""
        if self.suggestion_window and self.suggestion_listbox:
            self._select_current_suggestion()
            return 'break'
        return None
    
    def on_tab(self, event):
        """Handle Tab key"""
        if self.suggestion_window and self.suggestion_listbox:
            self._select_current_suggestion()
            return 'break'
        return None
    
    def _get_section_at_cursor(self, text: str, cursor_pos: int) -> int:
        """Determine which section of the part number the cursor is in"""
        if cursor_pos == 0:
            return 0
        
        # Count hyphens before cursor
        section = 0
        for i in range(cursor_pos):
            if text[i] == '-':
                section += 1
        
        return section
    
    def _get_current_word(self, text: str, cursor_pos: int) -> str:
        """Get the current word being typed"""
        if cursor_pos == 0:
            return ""
        
        # Find the start of the current word
        start = cursor_pos
        while start > 0 and text[start - 1] not in ['-', ' ']:
            start -= 1
        
        return text[start:cursor_pos]
    
    def _get_section_type(self, section: int) -> str:
        """Get the type of section based on position"""
        section_types = ['model', 'voltage', 'material', 'length', 'options']
        if section < len(section_types):
            return section_types[section]
        return 'options'  # Default to options for additional sections
    
    def show_suggestions(self, partial_text: str):
        """Show suggestion window"""
        # Get suggestions from database
        section_type = self._get_section_type(self.current_section)
        suggestions = self.db_manager.get_autocomplete_suggestions(section_type, partial_text, 10)
        
        if not suggestions:
            self.hide_suggestions()
            return
        
        self.suggestions = suggestions
        
        # Create suggestion window if it doesn't exist
        if not self.suggestion_window:
            self.suggestion_window = tk.Toplevel(self)
            self.suggestion_window.overrideredirect(True)
            self.suggestion_window.configure(bg='white')
            
            # Create listbox
            self.suggestion_listbox = tk.Listbox(
                self.suggestion_window,
                bg='white',
                fg='black',
                selectmode=tk.SINGLE,
                font=self.cget('font'),
                height=min(len(suggestions), 8)
            )
            self.suggestion_listbox.pack(fill=tk.BOTH, expand=True)
            
            # Bind listbox events
            self.suggestion_listbox.bind('<Button-1>', self._on_listbox_click)
            self.suggestion_listbox.bind('<Return>', self._on_listbox_return)
        
        # Clear and populate listbox
        self.suggestion_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            display_text = f"{suggestion['code']} - {suggestion['name']}"
            self.suggestion_listbox.insert(tk.END, display_text)
        
        # Position the suggestion window
        self._position_suggestion_window()
        
        # Select first item
        if self.suggestion_listbox.size() > 0:
            self.suggestion_listbox.selection_set(0)
    
    def hide_suggestions(self, event=None):
        """Hide suggestion window"""
        if self.suggestion_window:
            self.suggestion_window.destroy()
            self.suggestion_window = None
            self.suggestion_listbox = None
    
    def _position_suggestion_window(self):
        """Position the suggestion window below the entry"""
        if not self.suggestion_window:
            return
        
        # Get entry position
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        
        # Position window
        self.suggestion_window.geometry(f"+{x}+{y}")
        
        # Make sure window is on top
        self.suggestion_window.lift()
        self.suggestion_window.focus_force()
    
    def _select_previous(self):
        """Select previous suggestion"""
        if not self.suggestion_listbox:
            return
        
        current = self.suggestion_listbox.curselection()
        if current:
            if current[0] > 0:
                self.suggestion_listbox.selection_clear(current[0])
                self.suggestion_listbox.selection_set(current[0] - 1)
                self.suggestion_listbox.see(current[0] - 1)
        elif self.suggestion_listbox.size() > 0:
            self.suggestion_listbox.selection_set(0)
    
    def _select_next(self):
        """Select next suggestion"""
        if not self.suggestion_listbox:
            return
        
        current = self.suggestion_listbox.curselection()
        if current:
            if current[0] < self.suggestion_listbox.size() - 1:
                self.suggestion_listbox.selection_clear(current[0])
                self.suggestion_listbox.selection_set(current[0] + 1)
                self.suggestion_listbox.see(current[0] + 1)
        elif self.suggestion_listbox.size() > 0:
            self.suggestion_listbox.selection_set(0)
    
    def _select_current_suggestion(self):
        """Select the currently highlighted suggestion"""
        if not self.suggestion_listbox:
            return
        
        current = self.suggestion_listbox.curselection()
        if not current:
            return
        
        # Get selected suggestion
        index = current[0]
        if index < len(self.suggestions):
            suggestion = self.suggestions[index]
            self._apply_suggestion(suggestion['code'])
    
    def _on_listbox_click(self, event):
        """Handle listbox click"""
        if not self.suggestion_listbox:
            return
        
        # Get clicked index
        index = self.suggestion_listbox.nearest(event.y)
        if index >= 0 and index < len(self.suggestions):
            suggestion = self.suggestions[index]
            self._apply_suggestion(suggestion['code'])
    
    def _on_listbox_return(self, event):
        """Handle listbox return key"""
        self._select_current_suggestion()
        return 'break'
    
    def _apply_suggestion(self, suggestion_code: str):
        """Apply the selected suggestion to the entry"""
        # Get current text and cursor position
        text = self.get()
        cursor_pos = self.index(tk.INSERT)
        
        # Find the start of the current word
        start = cursor_pos
        while start > 0 and text[start - 1] not in ['-', ' ']:
            start -= 1
        
        # Replace the current word with the suggestion
        new_text = text[:start] + suggestion_code + text[cursor_pos:]
        
        # Update the entry
        self.delete(0, tk.END)
        self.insert(0, new_text)
        
        # Position cursor after the inserted text
        new_cursor_pos = start + len(suggestion_code)
        self.icursor(new_cursor_pos)
        
        # Hide suggestions
        self.hide_suggestions()
        
        # Call callback if set
        if self.on_suggestion_selected:
            self.on_suggestion_selected(new_text)
        
        # Focus back to entry
        self.focus_set() 
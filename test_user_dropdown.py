import pytest
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

class TestUserDropdown:
    """Test the user dropdown functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.main_window = MainWindow()
        self.root = self.main_window.root
        self.db_manager = self.main_window.db_manager
        
        # Add some test employees to the database
        if self.db_manager.connect():
            # Clear existing test employees
            self.db_manager.execute_query("DELETE FROM employees WHERE first_name LIKE 'Test%'")
            
            # Add test employees
            self.db_manager.add_employee("Test", "User1", "test1@example.com", "555-0001")
            self.db_manager.add_employee("Test", "User2", "test2@example.com", "555-0002")
            self.db_manager.add_employee("Test", "User3", "test3@example.com", "555-0003")
            
            self.db_manager.disconnect()
    
    def teardown_method(self):
        """Clean up test environment"""
        # Remove test employees
        if self.db_manager.connect():
            self.db_manager.execute_query("DELETE FROM employees WHERE first_name LIKE 'Test%'")
            self.db_manager.disconnect()
        
        self.root.destroy()
    
    def test_refresh_employee_dropdown(self):
        """Test that the employee dropdown is populated correctly"""
        # Refresh the dropdown
        self.main_window.populate_user_dropdown()
        
        # Check that employees are loaded
        assert len(self.main_window.employee_list) >= 3  # At least our test employees
        
        # Check that dropdown values are set
        dropdown_values = self.main_window.user_dropdown['values']
        assert len(dropdown_values) >= 3
        
        # Check that test employees are in the list
        test_names = ["Test User1", "Test User2", "Test User3"]
        for name in test_names:
            assert name in dropdown_values
    
    def test_user_selection(self):
        """Test that selecting a user works correctly"""
        # Refresh the dropdown
        self.main_window.populate_user_dropdown()
        
        # Select the first user
        self.main_window.user_dropdown.current(0)
        self.main_window.on_user_selected()
        
        # Check that employee info is set
        assert self.main_window.selected_employee_info is not None
        assert self.main_window.selected_employee_info['first_name'] == 'Test'
        assert self.main_window.selected_employee_info['last_name'] == 'User1'
    
    def test_get_user_initials(self):
        """Test that user initials are generated correctly"""
        # Refresh the dropdown
        self.main_window.populate_user_dropdown()
        
        # Select a user
        self.main_window.user_dropdown.current(0)
        self.main_window.on_user_selected()
        
        # Get initials
        initials = self.main_window.get_user_initials()
        assert initials == "TU"  # Test User1 -> TU
    
    def test_no_user_selected(self):
        """Test that no initials are returned when no user is selected"""
        # Don't select any user
        self.main_window.selected_employee_info = None
        
        # Get initials
        initials = self.main_window.get_user_initials()
        assert initials == ""
    
    def test_employee_manager_integration(self):
        """Test that employee manager integration works"""
        # Refresh the dropdown
        self.main_window.populate_user_dropdown()
        
        # Simulate selecting an employee from employee manager
        test_employee = {
            'id': 1,
            'first_name': 'Test',
            'last_name': 'Manager',
            'work_email': 'manager@example.com',
            'work_phone': '555-0000'
        }
        
        # Find the employee in the list and select it
        for i, emp in enumerate(self.main_window.employee_list):
            if emp['first_name'] == 'Test' and emp['last_name'] == 'User1':
                self.main_window.user_dropdown.current(i)
                self.main_window.selected_employee_info = emp
                break
        
        # Check that the selection worked
        assert self.main_window.selected_employee_info is not None
        assert self.main_window.get_user_initials() == "TU"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
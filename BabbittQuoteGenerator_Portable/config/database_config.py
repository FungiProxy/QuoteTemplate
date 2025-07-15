"""
Database Configuration for Babbitt Quote Generator
Handles database connection settings and configuration
"""

import sqlite3
import os
from pathlib import Path
from .settings import DATABASE_PATH, DATABASE_NAME

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.database_path = DATABASE_PATH
        self.connection_timeout = 30
        self.enable_foreign_keys = True
        self.row_factory = sqlite3.Row
        
    def get_connection_string(self):
        """Get database connection string"""
        return str(self.database_path)
    
    def get_connection_params(self):
        """Get connection parameters for sqlite3.connect()"""
        return {
            'database': str(self.database_path),
            'timeout': self.connection_timeout,
            'check_same_thread': False
        }
    
    def setup_connection(self, connection):
        """Setup connection with proper settings"""
        if self.enable_foreign_keys:
            connection.execute("PRAGMA foreign_keys = ON")
        
        if self.row_factory:
            connection.row_factory = self.row_factory
        
        return connection
    
    def verify_database_exists(self):
        """Check if database file exists"""
        return self.database_path.exists()
    
    def get_database_info(self):
        """Get database information"""
        return {
            'path': str(self.database_path),
            'name': DATABASE_NAME,
            'exists': self.verify_database_exists(),
            'size': self.database_path.stat().st_size if self.verify_database_exists() else 0
        }

# Database schema information
DATABASE_SCHEMA = {
    'tables': {
        'product_models': {
            'description': 'Base product models (LS2000, LS2100, etc.)',
            'key_columns': ['model_number', 'base_price', 'default_voltage']
        },
        'materials': {
            'description': 'Material codes and pricing (S, H, U, T, etc.)',
            'key_columns': ['code', 'name', 'base_price_adder', 'length_adder_per_foot']
        },
        'options': {
            'description': 'Option codes and pricing (XSP, VR, BP, etc.)',
            'key_columns': ['code', 'name', 'price', 'category']
        },
        'insulators': {
            'description': 'Insulator materials and specifications',
            'key_columns': ['code', 'name', 'price_adder', 'max_temp_rating']
        },
        'voltages': {
            'description': 'Available voltages for each model family',
            'key_columns': ['model_family', 'voltage', 'is_default']
        },
        'length_pricing': {
            'description': 'Length-based pricing rules',
            'key_columns': ['material_code', 'model_family', 'adder_per_foot']
        },
        'quotes': {
            'description': 'Generated quotes tracking',
            'key_columns': ['quote_number', 'customer_name', 'total_price']
        },
        'quote_items': {
            'description': 'Individual items within quotes',
            'key_columns': ['quote_id', 'part_number', 'quantity', 'unit_price']
        }
    }
}

# Connection pool settings (for future expansion)
POOL_SETTINGS = {
    'max_connections': 10,
    'min_connections': 1,
    'connection_timeout': 30,
    'idle_timeout': 300
}

# Database backup settings
BACKUP_SETTINGS = {
    'auto_backup': True,
    'backup_interval_hours': 24,
    'max_backups': 7,
    'backup_directory': 'database/backups'
}
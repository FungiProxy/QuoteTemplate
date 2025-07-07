"""
Database Manager for Babbitt Quote Generator
Handles all database connections and queries
"""

import sqlite3
import os
import json
from typing import Dict, List, Optional, Any

class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database manager"""
        if db_path is None:
            # Try to find the database in common locations
            possible_paths = [
                "database/quotes.db",
                "quotes.db", 
                "../quotes.db"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.db_path = path
                    break
            else:
                self.db_path = "database/quotes.db"  # Default location
        else:
            self.db_path = db_path
            
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a SELECT query and return results"""
        if not self.connection:
            if not self.connect():
                return []
        
        if not self.connection:  # Double check after connect attempt
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            # Convert Row objects to dictionaries
            results = []
            for row in cursor.fetchall():
                results.append(dict(row))
            
            return results
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return []
    
    def get_model_info(self, model_code: str) -> Optional[Dict]:
        """Get model information by model code"""
        query = """
        SELECT * FROM product_models 
        WHERE model_number = ? OR model_number LIKE ?
        LIMIT 1
        """
        
        results = self.execute_query(query, (model_code, f"{model_code}%"))
        return results[0] if results else None
    
    def get_material_info(self, material_code: str) -> Optional[Dict]:
        """Get material information by code"""
        query = "SELECT * FROM materials WHERE code = ?"
        results = self.execute_query(query, (material_code,))
        return results[0] if results else None
    
    def get_insulator_info(self, insulator_code: str) -> Optional[Dict]:
        """Get insulator information by code"""
        query = "SELECT * FROM insulators WHERE code = ?"
        results = self.execute_query(query, (insulator_code,))
        return results[0] if results else None
    
    def get_option_info(self, option_code: str) -> Optional[Dict]:
        """Get option information by code"""
        query = "SELECT * FROM options WHERE code = ?"
        results = self.execute_query(query, (option_code,))
        return results[0] if results else None
    
    def get_voltage_options(self, model_family: Optional[str] = None) -> List[Dict]:
        """Get available voltage options, optionally filtered by model family"""
        if model_family:
            query = "SELECT * FROM voltages WHERE model_family = ? ORDER BY is_default DESC, voltage"
            params = (model_family,)
        else:
            query = "SELECT * FROM voltages ORDER BY model_family, is_default DESC, voltage"
            params = ()
        
        return self.execute_query(query, params)
    
    def get_length_pricing(self, material_code: str, model_family: str) -> Optional[Dict]:
        """Get length pricing rules for material and model"""
        query = """
        SELECT * FROM length_pricing 
        WHERE material_code = ? AND model_family = ?
        LIMIT 1
        """
        results = self.execute_query(query, (material_code, model_family))
        return results[0] if results else None
    
    def calculate_base_price(self, model_code: str, voltage: str, material_code: str) -> float:
        """Calculate base price for model/voltage/material combination"""
        # Get model base price
        model_info = self.get_model_info(model_code)
        if not model_info:
            return 0.0
        
        base_price = model_info['base_price']
        
        # Add material price adder
        material_info = self.get_material_info(material_code)
        if material_info:
            base_price += material_info['base_price_adder']
        
        # Add voltage price adder (if any)
        voltage_info = self.execute_query(
            "SELECT * FROM voltages WHERE model_family = ? AND voltage = ?", 
            (model_code, voltage)
        )
        if voltage_info:
            base_price += voltage_info[0].get('price_adder', 0.0)
        
        return base_price
    
    def calculate_length_cost(self, material_code: str, model_family: str, probe_length: float) -> Dict[str, float]:
        """Calculate length-based pricing"""
        length_pricing = self.get_length_pricing(material_code, model_family)
        if not length_pricing:
            return {'length_cost': 0.0, 'surcharge': 0.0}
        
        base_length = length_pricing['base_length']
        extra_length = max(0, probe_length - base_length)
        
        # Calculate length cost
        length_cost = 0.0
        if extra_length > 0:
            if length_pricing['adder_per_foot'] > 0:
                length_cost = (extra_length / 12.0) * length_pricing['adder_per_foot']
            elif length_pricing['adder_per_inch'] > 0:
                length_cost = extra_length * length_pricing['adder_per_inch']
        
        # Calculate nonstandard length surcharge
        surcharge = 0.0
        if (length_pricing['nonstandard_threshold'] > 0 and 
            probe_length > length_pricing['nonstandard_threshold']):
            surcharge = length_pricing['nonstandard_surcharge']
        
        return {
            'length_cost': length_cost,
            'surcharge': surcharge,
            'extra_length': extra_length,
            'base_length': base_length
        }
    
    def calculate_option_cost(self, option_codes: List[str]) -> Dict[str, Any]:
        """Calculate total cost for options"""
        total_cost = 0.0
        option_details = []
        
        for code in option_codes:
            option_info = self.get_option_info(code)
            if option_info:
                option_details.append({
                    'code': code,
                    'name': option_info['name'],
                    'price': option_info['price'],
                    'price_type': option_info['price_type']
                })
                total_cost += option_info['price']
        
        return {
            'total_cost': total_cost,
            'options': option_details
        }
    
    def calculate_insulator_cost(self, insulator_code: str) -> float:
        """Calculate insulator cost"""
        insulator_info = self.get_insulator_info(insulator_code)
        return insulator_info['price_adder'] if insulator_info else 0.0
    
    def calculate_total_price(self, model_code: str, voltage: str, material_code: str, 
                            probe_length: float, option_codes: Optional[List[str]] = None, 
                            insulator_code: Optional[str] = None) -> Dict[str, Any]:
        """Calculate total price for a complete configuration"""
        if option_codes is None:
            option_codes = []
        
        # Base price
        base_price = self.calculate_base_price(model_code, voltage, material_code)
        
        # Length pricing
        length_info = self.calculate_length_cost(material_code, model_code, probe_length)
        
        # Option pricing
        option_info = self.calculate_option_cost(option_codes)
        
        # Insulator pricing
        insulator_cost = 0.0
        if insulator_code:
            insulator_cost = self.calculate_insulator_cost(insulator_code)
        
        # Total calculation
        total_price = (base_price + 
                      length_info['length_cost'] + 
                      length_info['surcharge'] + 
                      option_info['total_cost'] + 
                      insulator_cost)
        
        return {
            'total_price': total_price,
            'base_price': base_price,
            'length_cost': length_info['length_cost'],
            'length_surcharge': length_info['surcharge'],
            'option_cost': option_info['total_cost'],
            'insulator_cost': insulator_cost,
            'length_details': length_info,
            'option_details': option_info['options']
        }
    
    def get_material_codes(self) -> Dict[str, str]:
        """Get material code mappings"""
        query = "SELECT code, name FROM materials"
        results = self.execute_query(query)
        
        return {row['code']: row['name'] for row in results}
    
    def get_insulator_codes(self) -> Dict[str, str]:
        """Get insulator code mappings"""
        query = "SELECT code, name FROM insulators"
        results = self.execute_query(query)
        
        return {row['code']: row['name'] for row in results}
    
    def get_option_codes(self) -> Dict[str, str]:
        """Get option code mappings"""
        query = "SELECT code, name FROM options"
        results = self.execute_query(query)
        
        return {row['code']: row['name'] for row in results}
    
    def search_parts(self, search_term: str) -> List[Dict]:
        """Search for parts by model number or description"""
        query = """
        SELECT * FROM product_models 
        WHERE model_number LIKE ? OR description LIKE ?
        LIMIT 20
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern))
    
    def test_connection(self) -> bool:
        """Test database connection and return basic info"""
        if not self.connect():
            return False
        
        try:
            # Test query
            if not self.connection:
                return False
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'")
            result = cursor.fetchone()
            
            print(f"✓ Database connected: {self.db_path}")
            print(f"✓ Tables found: {result['count']}")
            
            # Check for key tables
            key_tables = ['product_models', 'materials', 'options', 'insulators', 'voltages']
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            for table in key_tables:
                if table in existing_tables:
                    print(f"✓ {table} table found")
                else:
                    print(f"! {table} table missing")
            
            return True
            
        except sqlite3.Error as e:
            print(f"Database test failed: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

# Test the database connection if run directly
if __name__ == "__main__":
    print("Testing Database Connection...")
    print("=" * 40)
    
    db = DatabaseManager()
    if db.test_connection():
        print("\n✓ Database connection successful!")
        
        # Test a few queries
        print("\nTesting queries...")
        
        models = db.execute_query("SELECT model_number FROM product_models LIMIT 5")
        print(f"Found {len(models)} product models")
        
        materials = db.execute_query("SELECT code, name FROM materials LIMIT 5")
        print(f"Found {len(materials)} materials")
        
        # Test pricing calculation
        print("\nTesting pricing calculation...")
        pricing = db.calculate_total_price('LS2000', '115VAC', 'S', 10.0, ['XSP'], 'U')
        print(f"Sample price: ${pricing['total_price']:.2f}")
        
    else:
        print("\n✗ Database connection failed!")
        print("Make sure quotes.db is in the database/ folder")
    
    db.disconnect() 
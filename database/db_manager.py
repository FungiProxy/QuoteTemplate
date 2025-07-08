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
        """Calculate length-based pricing using new stepped calculation"""
        import math
        
        # Round up any non-whole number lengths for pricing
        probe_length = math.ceil(probe_length)
        
        # Get model info for base length
        model_info = self.get_model_info(model_family)
        if not model_info:
            return {'length_cost': 0.0, 'surcharge': 0.0}
        
        model_base_length = model_info['base_length']
        
        # Get material info for pricing
        material_info = self.get_material_info(material_code)
        if not material_info:
            return {'length_cost': 0.0, 'surcharge': 0.0}
        
        # Calculate length cost based on material type
        length_cost = 0.0
        if material_info['length_adder_per_foot'] > 0:
            # Per-foot materials use stepped calculation
            length_cost = self._calculate_stepped_foot_pricing(
                model_base_length, 
                probe_length, 
                material_info['length_adder_per_foot']
            )
        elif material_info['length_adder_per_inch'] > 0:
            # Per-inch materials use continuous calculation from material base length
            material_base_length = material_info.get('material_base_length', 4.0)  # Default to 4" if not specified
            extra_length = max(0, probe_length - material_base_length)
            if extra_length > 0:
                length_cost = extra_length * material_info['length_adder_per_inch']
        
        # Calculate nonstandard length surcharge
        surcharge = 0.0
        if (material_info['nonstandard_length_surcharge'] > 0 and 
            probe_length > 96.0):  # Standard threshold for most materials
            surcharge = material_info['nonstandard_length_surcharge']
        
        return {
            'length_cost': length_cost,
            'surcharge': surcharge,
            'extra_length': probe_length - model_base_length if probe_length > model_base_length else 0,
            'base_length': model_base_length
        }
    
    def _calculate_stepped_foot_pricing(self, model_base_length: float, probe_length: float, adder_per_foot: float) -> float:
        """
        Calculate stepped foot pricing based on foot thresholds.
        For 10" base models: first adder at 11", then 24", 36", 48", etc.
        For 6" base models: first adder at 7", then 18", 30", 42", etc. (every 12" from base)
        """
        if probe_length <= model_base_length:
            return 0.0
        
        # Calculate foot thresholds based on model base length
        if model_base_length == 10.0:
            # For 10" base: thresholds at 11", 24", 36", 48", 60", 72", 84", 96", 108", 120"...
            thresholds = [11.0]
            next_threshold = 24.0
            while next_threshold <= 120.0:  # Reasonable upper limit
                thresholds.append(next_threshold)
                next_threshold += 12.0
        elif model_base_length == 6.0:
            # For 6" base (FS10000): first adder at 7", then every 12" from base: 18", 30", 42", 54"...
            thresholds = [7.0]  # First adder at base + 1"
            next_threshold = model_base_length + 12.0  # Start at 18" (6" + 12")
            while next_threshold <= 120.0:  # Reasonable upper limit
                thresholds.append(next_threshold)
                next_threshold += 12.0  # Continue every 12": 30", 42", 54", etc.
        else:
            # For other base lengths, use simple 12" increments from base + 1"
            thresholds = [model_base_length + 1.0]
            next_threshold = model_base_length + 12.0
            while next_threshold <= model_base_length + 120.0:
                thresholds.append(next_threshold)
                next_threshold += 12.0
        
        # Count how many thresholds the probe length exceeds
        num_adders = 0
        for threshold in thresholds:
            if probe_length >= threshold:
                num_adders += 1
            else:
                break
        
        return num_adders * adder_per_foot
    
    def _calculate_od_option_foot_pricing(self, model_base_length: float, probe_length: float, adder_per_foot: float) -> float:
        """
        Calculate 3/4"OD option stepped foot pricing with strict 12" increments.
        For 3/4"OD: 11" = first adder, 22" = second adder, 34" = third adder, etc.
        Every 12" from model base length + 1".
        """
        if probe_length <= model_base_length:
            return 0.0
        
        # Calculate thresholds: base + 1", base + 12", base + 24", base + 36", etc.
        thresholds = []
        for i in range(10):  # Generate up to 10 thresholds (reasonable limit)
            if i == 0:
                threshold = model_base_length + 1.0  # First threshold at base + 1"
            else:
                threshold = model_base_length + (12.0 * i)  # Subsequent thresholds every 12"
            
            if threshold > 120.0:  # Stop at reasonable upper limit
                break
            thresholds.append(threshold)
        
        # Count how many thresholds the probe length exceeds
        num_adders = 0
        for threshold in thresholds:
            if probe_length >= threshold:
                num_adders += 1
            else:
                break
        
        return num_adders * adder_per_foot
    
    def calculate_option_cost(self, option_codes: List[str], probe_length: float = 10.0, model_code: Optional[str] = None) -> Dict[str, Any]:
        """Calculate total cost for options with special handling for 3/4"OD probe"""
        total_cost = 0.0
        option_details = []
        
        for code in option_codes:
            # Check for bent probe degree format (e.g., 90DEG, 45DEG)
            if code.endswith('DEG'):
                # Extract degree and validate
                try:
                    degree = int(code[:-3])  # Remove 'DEG' suffix
                    if 0 <= degree <= 180:
                        option_details.append({
                            'code': code,
                            'name': f'Bent Probe ({degree}°)',
                            'price': 50.0,  # Fixed price for all bent probe configurations
                            'price_type': 'fixed'
                        })
                        total_cost += 50.0
                    else:
                        # Invalid degree range
                        option_details.append({
                            'code': code,
                            'name': f'Invalid Bent Probe ({degree}°)',
                            'price': 0.0,
                            'price_type': 'fixed'
                        })
                except ValueError:
                    # Invalid format
                    option_details.append({
                        'code': code,
                        'name': f'Invalid Bent Probe Format',
                        'price': 0.0,
                        'price_type': 'fixed'
                    })
            elif code == '3/4"OD':
                # Special handling for 3/4" OD probe: $175 base + $175 per foot in strict 12" increments
                model_info = self.get_model_info(model_code) if model_code else None
                model_base_length = model_info['base_length'] if model_info else 10.0  # Default to 10" if not found
                
                base_cost = 175.0
                # Use OD-specific stepped foot pricing: 11"=1st adder, 22"=2nd adder, 34"=3rd adder, etc.
                stepped_foot_cost = self._calculate_od_option_foot_pricing(model_base_length, probe_length, 175.0)
                total_od_cost = base_cost + stepped_foot_cost
                
                option_details.append({
                    'code': code,
                    'name': '3/4" Diameter Probe',
                    'price': total_od_cost,
                    'price_type': 'base_plus_per_foot',
                    'base_cost': base_cost,
                    'per_foot_cost': stepped_foot_cost,
                    'probe_length_feet': probe_length / 12.0,
                    'model_base_length': model_base_length
                })
                total_cost += total_od_cost
            else:
                # Regular option from database
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
    
    def calculate_insulator_cost(self, insulator_code: str, material_code: Optional[str] = None) -> float:
        """Calculate insulator cost with material-specific rules"""
        insulator_info = self.get_insulator_info(insulator_code)
        if not insulator_info:
            return 0.0
        
        cost = insulator_info['price_adder']
        
        # Special rule: If probe material is 'h', teflon insulation adder is not applied
        if (material_code and material_code.upper() == 'H' and 
            insulator_code.upper() == 'TEF'):
            return 0.0
        
        return cost
    
    def calculate_total_price(self, model_code: str, voltage: str, material_code: str, 
                            probe_length: float, option_codes: Optional[List[str]] = None, 
                            insulator_code: Optional[str] = None, 
                            connection_info: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Calculate total price for a complete configuration"""
        if option_codes is None:
            option_codes = []
        
        # Base price
        base_price = self.calculate_base_price(model_code, voltage, material_code)
        
        # Length pricing
        length_info = self.calculate_length_cost(material_code, model_code, probe_length)
        
        # Option pricing (with special handling for 3/4"OD)
        option_info = self.calculate_option_cost(option_codes, probe_length, model_code)
        
        # Insulator pricing
        insulator_cost = 0.0
        if insulator_code:
            insulator_cost = self.calculate_insulator_cost(insulator_code, material_code)
        
        # Process connection pricing
        connection_cost = 0.0
        if connection_info:
            connection_cost = self.calculate_connection_cost(
                connection_info.get('type', 'NPT'),
                connection_info.get('size', '3/4"'),
                connection_info.get('material', 'SS'),
                connection_info.get('rating')
            )
        
        # Total calculation
        total_price = (base_price + 
                      length_info['length_cost'] + 
                      length_info['surcharge'] + 
                      option_info['total_cost'] + 
                      insulator_cost + 
                      connection_cost)
        
        return {
            'total_price': total_price,
            'base_price': base_price,
            'length_cost': length_info['length_cost'],
            'length_surcharge': length_info['surcharge'],
            'option_cost': option_info['total_cost'],
            'insulator_cost': insulator_cost,
            'connection_cost': connection_cost,
            'length_details': length_info,
            'option_details': option_info['options']
        }
    
    # PROCESS CONNECTION METHODS
    def get_process_connection_info(self, conn_type: str, size: str, material: str = 'SS', rating: Optional[str] = None) -> Optional[Dict]:
        """Get process connection information by type, size, material, and rating"""
        if rating:
            query = """
            SELECT * FROM process_connections 
            WHERE type = ? AND size = ? AND material = ? AND rating = ?
            LIMIT 1
            """
            params = (conn_type, size, material, rating)
        else:
            query = """
            SELECT * FROM process_connections 
            WHERE type = ? AND size = ? AND material = ? AND (rating IS NULL OR rating = '')
            LIMIT 1
            """
            params = (conn_type, size, material)
        
        results = self.execute_query(query, params)
        return results[0] if results else None
    
    def get_available_connections(self, model_family: Optional[str] = None, conn_type: Optional[str] = None) -> List[Dict]:
        """Get available process connections, optionally filtered by model family and/or connection type"""
        base_query = "SELECT * FROM process_connections WHERE 1=1"
        params = []
        
        if model_family:
            base_query += " AND (compatible_models = 'ALL' OR compatible_models LIKE ?)"
            params.append(f'%{model_family}%')
        
        if conn_type:
            base_query += " AND type = ?"
            params.append(conn_type)
        
        base_query += " ORDER BY type, size, material, rating"
        
        return self.execute_query(base_query, tuple(params))
    
    def get_connection_types(self) -> List[str]:
        """Get all available connection types"""
        query = "SELECT DISTINCT type FROM process_connections ORDER BY type"
        results = self.execute_query(query)
        return [row['type'] for row in results]
    
    def get_connection_sizes(self, conn_type: Optional[str] = None) -> List[str]:
        """Get available connection sizes, optionally filtered by connection type"""
        if conn_type:
            query = "SELECT DISTINCT size FROM process_connections WHERE type = ? ORDER BY size"
            params = (conn_type,)
        else:
            query = "SELECT DISTINCT size FROM process_connections ORDER BY size"
            params = ()
        
        results = self.execute_query(query, params)
        return [row['size'] for row in results]
    
    def get_connection_materials(self, conn_type: Optional[str] = None, size: Optional[str] = None) -> List[str]:
        """Get available connection materials, optionally filtered by type and size"""
        base_query = "SELECT DISTINCT material FROM process_connections WHERE 1=1"
        params = []
        
        if conn_type:
            base_query += " AND type = ?"
            params.append(conn_type)
        
        if size:
            base_query += " AND size = ?"
            params.append(size)
        
        base_query += " ORDER BY material"
        
        results = self.execute_query(base_query, tuple(params))
        return [row['material'] for row in results]
    
    def get_connection_ratings(self, conn_type: str, size: str, material: str = 'SS') -> List[str]:
        """Get available ratings for a specific connection type/size/material combination"""
        query = """
        SELECT DISTINCT rating FROM process_connections 
        WHERE type = ? AND size = ? AND material = ? AND rating IS NOT NULL AND rating != ''
        ORDER BY rating
        """
        results = self.execute_query(query, (conn_type, size, material))
        return [row['rating'] for row in results]
    
    def calculate_connection_cost(self, conn_type: str, size: str, material: str = 'SS', rating: Optional[str] = None) -> float:
        """Calculate cost for a process connection"""
        conn_info = self.get_process_connection_info(conn_type, size, material, rating)
        return conn_info['price'] if conn_info else 0.0
    
    def format_connection_display(self, conn_type: str, size: str, material: str = 'SS', rating: Optional[str] = None) -> str:
        """Format connection information for display"""
        if conn_type == 'NPT':
            return f"{size}NPT ({material})"
        elif conn_type == 'Flange':
            rating_str = f" {rating}" if rating else ""
            return f"{size}{rating_str} RF Flange ({material})"
        elif conn_type == 'Tri-Clamp':
            return f"{size} Tri-Clamp ({material})"
        else:
            return f"{size} {conn_type} ({material})"
    
    def get_default_connection(self, model_code: str) -> Optional[Dict]:
        """Get default process connection for a model"""
        model_info = self.get_model_info(model_code)
        if not model_info:
            return None
        
        conn_type = model_info.get('default_process_connection_type', 'NPT')
        conn_size = model_info.get('default_process_connection_size', '3/4"')
        conn_material = model_info.get('default_process_connection_material', 'SS')
        
        return self.get_process_connection_info(conn_type, conn_size, conn_material)

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
        """Search for parts in product catalog"""
        query = """
        SELECT model_number as part_number, description as name, base_price as price, 'product' as type
        FROM product_models 
        WHERE model_number LIKE ? OR description LIKE ?
        """
        
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern))

    # SPARE PARTS METHODS
    
    def get_spare_parts_by_model(self, model_code: str) -> List[Dict]:
        """Get all spare parts compatible with a specific model"""
        query = """
        SELECT sp.*, 
               CASE 
                   WHEN sp.compatible_models LIKE ? THEN 1
                   ELSE 0
               END as direct_match
        FROM spare_parts sp
        WHERE sp.compatible_models LIKE ?
        ORDER BY direct_match DESC, sp.category, sp.name
        """
        
        search_pattern = f"%{model_code}%"
        return self.execute_query(query, (search_pattern, search_pattern))
    
    def get_spare_parts_by_category(self, category: str, model_code: Optional[str] = None) -> List[Dict]:
        """Get spare parts by category, optionally filtered by model compatibility"""
        if model_code:
            query = """
            SELECT * FROM spare_parts 
            WHERE category = ? AND compatible_models LIKE ?
            ORDER BY name
            """
            search_pattern = f"%{model_code}%"
            params = (category, search_pattern)
        else:
            query = """
            SELECT * FROM spare_parts 
            WHERE category = ?
            ORDER BY name
            """
            params = (category,)
        
        return self.execute_query(query, params)
    
    def get_spare_part_by_part_number(self, part_number: str) -> Optional[Dict]:
        """Get specific spare part by part number"""
        query = "SELECT * FROM spare_parts WHERE part_number = ?"
        results = self.execute_query(query, (part_number,))
        return results[0] if results else None
    
    def search_spare_parts(self, search_term: str, model_code: Optional[str] = None) -> List[Dict]:
        """Search spare parts by name, part number, or description"""
        if model_code:
            query = """
            SELECT * FROM spare_parts 
            WHERE (part_number LIKE ? OR name LIKE ? OR description LIKE ?)
              AND compatible_models LIKE ?
            ORDER BY 
                CASE WHEN part_number LIKE ? THEN 1 ELSE 2 END,
                name
            """
            search_pattern = f"%{search_term}%"
            model_pattern = f"%{model_code}%"
            params = (search_pattern, search_pattern, search_pattern, model_pattern, search_pattern)
        else:
            query = """
            SELECT * FROM spare_parts 
            WHERE part_number LIKE ? OR name LIKE ? OR description LIKE ?
            ORDER BY 
                CASE WHEN part_number LIKE ? THEN 1 ELSE 2 END,
                name
            """
            search_pattern = f"%{search_term}%"
            params = (search_pattern, search_pattern, search_pattern, search_pattern)
        
        return self.execute_query(query, params)
    
    def get_spare_part_categories(self, model_code: Optional[str] = None) -> List[Dict]:
        """Get available spare part categories, optionally filtered by model"""
        if model_code:
            query = """
            SELECT DISTINCT category, COUNT(*) as part_count
            FROM spare_parts 
            WHERE category IS NOT NULL AND compatible_models LIKE ?
            GROUP BY category
            ORDER BY category
            """
            search_pattern = f"%{model_code}%"
            params = (search_pattern,)
        else:
            query = """
            SELECT DISTINCT category, COUNT(*) as part_count
            FROM spare_parts 
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY category
            """
            params = ()
        
        return self.execute_query(query, params)
    
    def calculate_spare_part_price(self, part_number: str, quantity: int = 1, 
                                 voltage: Optional[str] = None, 
                                 length: Optional[float] = None,
                                 sensitivity: Optional[str] = None) -> Dict[str, Any]:
        """Calculate spare part pricing with options for voltage, length, and sensitivity specs"""
        
        spare_part = self.get_spare_part_by_part_number(part_number)
        if not spare_part:
            return {
                'base_price': 0.0,
                'total_price': 0.0,
                'quantity': quantity,
                'error': f"Spare part '{part_number}' not found"
            }
        
        base_price = spare_part['price']
        total_price = base_price * quantity
        
        # Handle special pricing for length-dependent parts
        if spare_part['requires_length_spec'] and length and length > 10.0:
            # For probe assemblies with length specifications
            if '3/4' in spare_part['part_number'].upper() and 'PROBE' in spare_part['part_number'].upper():
                # 3/4" diameter probes have $175/ft adder
                extra_feet = (length - 10.0) / 12.0  # Convert inches to feet
                if extra_feet > 0:
                    length_adder = extra_feet * 175.0
                    total_price = (base_price + length_adder) * quantity
        
        # Handle special requirements notes
        notes = []
        if spare_part['requires_voltage_spec']:
            if voltage:
                notes.append(f"Voltage: {voltage}")
            else:
                notes.append("Voltage specification required when ordering")
        
        if spare_part['requires_length_spec']:
            if length:
                notes.append(f"Length: {length}\"")
            else:
                notes.append("Length specification required when ordering")
        
        if spare_part['requires_sensitivity_spec']:
            if sensitivity:
                notes.append(f"Sensitivity: {sensitivity}")
            else:
                notes.append("Sensitivity specification required when ordering")
        
        return {
            'part_number': part_number,
            'name': spare_part['name'],
            'description': spare_part['description'],
            'category': spare_part['category'],
            'base_price': base_price,
            'unit_price': total_price / quantity,
            'total_price': total_price,
            'quantity': quantity,
            'notes': notes,
            'special_requirements': {
                'requires_voltage': spare_part['requires_voltage_spec'],
                'requires_length': spare_part['requires_length_spec'],
                'requires_sensitivity': spare_part['requires_sensitivity_spec']
            }
        }
    
    def get_popular_spare_parts(self, model_code: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get most common spare parts, optionally filtered by model"""
        # Priority order: electronics, probe_assembly, housing, card, transmitter, receiver, fuse, cable
        priority_categories = ['electronics', 'probe_assembly', 'housing', 'card', 'transmitter', 'receiver', 'fuse', 'cable']
        
        if model_code:
            query = """
            SELECT *, 
                   CASE 
                       WHEN category = 'electronics' THEN 1
                       WHEN category = 'probe_assembly' THEN 2
                       WHEN category = 'housing' THEN 3
                       WHEN category = 'card' THEN 4
                       WHEN category = 'transmitter' THEN 5
                       WHEN category = 'receiver' THEN 6
                       WHEN category = 'fuse' THEN 7
                       WHEN category = 'cable' THEN 8
                       ELSE 9
                   END as priority
            FROM spare_parts 
            WHERE compatible_models LIKE ?
            ORDER BY priority, price DESC
            LIMIT ?
            """
            search_pattern = f"%{model_code}%"
            params = (search_pattern, limit)
        else:
            query = """
            SELECT *, 
                   CASE 
                       WHEN category = 'electronics' THEN 1
                       WHEN category = 'probe_assembly' THEN 2
                       WHEN category = 'housing' THEN 3
                       WHEN category = 'card' THEN 4
                       WHEN category = 'transmitter' THEN 5
                       WHEN category = 'receiver' THEN 6
                       WHEN category = 'fuse' THEN 7
                       WHEN category = 'cable' THEN 8
                       ELSE 9
                   END as priority
            FROM spare_parts
            ORDER BY priority, price DESC
            LIMIT ?
            """
            params = (limit,)
        
        return self.execute_query(query, params)
    
    def validate_spare_part_compatibility(self, part_number: str, model_code: str) -> Dict[str, Any]:
        """Validate if a spare part is compatible with a specific model"""
        spare_part = self.get_spare_part_by_part_number(part_number)
        if not spare_part:
            return {
                'compatible': False,
                'error': f"Spare part '{part_number}' not found"
            }
        
        try:
            # Parse the compatible_models JSON array
            compatible_models = json.loads(spare_part['compatible_models'])
            
            # Check for exact match or wildcard compatibility
            if model_code in compatible_models or 'ALL' in compatible_models:
                return {
                    'compatible': True,
                    'part_number': part_number,
                    'model_code': model_code,
                    'compatible_models': compatible_models
                }
            else:
                return {
                    'compatible': False,
                    'part_number': part_number,
                    'model_code': model_code,
                    'compatible_models': compatible_models,
                    'error': f"Part '{part_number}' is not compatible with model '{model_code}'"
                }
        except (json.JSONDecodeError, KeyError):
            # Fallback to string search if JSON parsing fails
            if model_code in spare_part['compatible_models']:
                return {'compatible': True}
            else:
                return {
                    'compatible': False,
                    'error': f"Compatibility data format error for part '{part_number}'"
                }

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
            key_tables = ['product_models', 'materials', 'options', 'insulators', 'voltages', 'process_connections']
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
        
        # Test process connections
        print("\nTesting process connections...")
        connection_types = db.get_connection_types()
        print(f"Available connection types: {connection_types}")
        
        if connection_types:
            connections = db.get_available_connections(conn_type='NPT')
            print(f"NPT connections found: {len(connections)}")
            
            # Test specific connection
            npt_conn = db.get_process_connection_info('NPT', '3/4"', 'SS')
            if npt_conn:
                print(f"3/4\" NPT connection: {db.format_connection_display('NPT', '3/4\"', 'SS')}")
            
            # Test default connection for LS2000
            default_conn = db.get_default_connection('LS2000')
            if default_conn:
                print(f"LS2000 default connection: {default_conn['description']}")
        
    else:
        print("\n✗ Database connection failed!")
        print("Make sure quotes.db is in the database/ folder")
    
    db.disconnect() 
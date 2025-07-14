"""
Simple Customer Database Manager
Handles basic customer information: company, contact name, email, and phone
"""

import sqlite3
import os
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CustomerDBManager:
    """Manages the simple customer database operations."""
    
    def __init__(self, db_path: str = "database/customers.db"):
        """Initialize the customer database manager.
        
        Args:
            db_path: Path to the customer database file
        """
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure the customer database exists and has the correct schema."""
        if not os.path.exists(self.db_path):
            self._create_database()
    
    def _create_database(self):
        """Create the customer database with the proper schema."""
        try:
            with open("database/create_customer_db.sql", "r") as f:
                sql_script = f.read()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(sql_script)
                conn.commit()
            
            logger.info(f"Customer database created at {self.db_path}")
        except Exception as e:
            logger.error(f"Error creating customer database: {e}")
            raise
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def add_customer(self, customer_name: str, contact_name: Optional[str] = None, 
                    email: Optional[str] = None, phone: Optional[str] = None) -> int:
        """Add a new customer to the database.
        
        Returns:
            The ID of the newly created customer
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (customer_name, contact_name, email, phone)
                VALUES (?, ?, ?, ?)
            """, (customer_name, contact_name, email, phone))
            conn.commit()
            result = cursor.lastrowid
            if result is None:
                raise RuntimeError("Failed to insert customer")
            return result
    
    def get_customer(self, customer_id: int) -> Optional[Dict]:
        """Get a customer by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def get_all_customers(self) -> List[Dict]:
        """Get all customers."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers ORDER BY customer_name")
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def search_customers(self, search_term: str) -> List[Dict]:
        """Search customers by name or contact name."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            cursor.execute("""
                SELECT * FROM customers 
                WHERE customer_name LIKE ? OR contact_name LIKE ?
                ORDER BY customer_name
            """, (search_pattern, search_pattern))
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def update_customer(self, customer_id: int, **kwargs) -> bool:
        """Update a customer's information."""
        allowed_fields = ['customer_name', 'contact_name', 'email', 'phone']
        
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not update_fields:
            return False
        
        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values()) + [customer_id]
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE customers SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_customer_summary(self) -> Dict:
        """Get a summary of customer database statistics."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Count customers
            cursor.execute("SELECT COUNT(*) FROM customers")
            total_customers = cursor.fetchone()[0]
            
            return {
                'total_customers': total_customers
            }


# Convenience function to get a database manager instance
def get_customer_db_manager(db_path: str = "database/customers.db") -> CustomerDBManager:
    """Get a customer database manager instance."""
    return CustomerDBManager(db_path) 
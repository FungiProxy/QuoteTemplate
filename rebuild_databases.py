import sqlite3
import os

def rebuild_quotes_database():
    """Rebuild the quotes database from the SQL script"""
    db_path = 'database/quotes.db'
    sql_path = 'database/create_quote_db.sql'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing quotes database")
    
    # Create new database from SQL script
    conn = sqlite3.connect(db_path)
    with open(sql_path, 'r') as f:
        sql_script = f.read()
    
    conn.executescript(sql_script)
    conn.close()
    
    print("Quotes database recreated successfully!")

def rebuild_customers_database():
    """Rebuild the customers database from the SQL script"""
    db_path = 'database/customers.db'
    sql_path = 'database/create_customer_db.sql'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing customers database")
    
    # Create new database from SQL script
    conn = sqlite3.connect(db_path)
    with open(sql_path, 'r') as f:
        sql_script = f.read()
    
    conn.executescript(sql_script)
    conn.close()
    
    print("Customers database recreated successfully!")

def main():
    """Rebuild both databases"""
    print("Rebuilding databases for portable distribution...")
    print("This will remove all saved customer data.")
    print()
    
    rebuild_quotes_database()
    print()
    rebuild_customers_database()
    print()
    
    print("Database rebuild complete!")
    print("Both databases now contain only the base schema and sample data.")
    print("All previously saved customer information has been removed.")

if __name__ == "__main__":
    main() 
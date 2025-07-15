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

def rebuild_customer_database():
    """Rebuild the customer database from the SQL script"""
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
    print("Customer database recreated successfully!")

if __name__ == "__main__":
    print("Rebuilding all databases for portable distribution...")
    print("This will remove all saved customer data.")
    print()
    
    rebuild_quotes_database()
    print()
    rebuild_customer_database()
    print()
    print("All databases rebuilt successfully!")
    print("Customer data has been removed from both databases.") 
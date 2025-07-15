import sqlite3

def check_customer_database():
    """Check customer database for any saved data"""
    conn = sqlite3.connect('database/customers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM customers')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def check_quotes_database():
    """Check quotes database for any saved quote data"""
    conn = sqlite3.connect('database/quotes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM quotes')
    count = cursor.fetchone()[0]
    conn.close()
    return count

if __name__ == "__main__":
    print("Verifying database cleanup...")
    print()
    
    customer_count = check_customer_database()
    quotes_count = check_quotes_database()
    
    print(f"Customer records: {customer_count}")
    print(f"Quote records: {quotes_count}")
    print()
    
    if customer_count == 0 and quotes_count == 0:
        print("✓ Both databases are clean - no saved customer data found!")
    else:
        print("⚠ Some data still exists in databases") 
import sqlite3

# Check customer database
conn = sqlite3.connect('database/customers.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM customers')
customer_count = cursor.fetchone()[0]
conn.close()

# Check quotes database
conn = sqlite3.connect('database/quotes.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM quotes')
quotes_count = cursor.fetchone()[0]
conn.close()

print("Customer records:", customer_count)
print("Quote records:", quotes_count) 
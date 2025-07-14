import sqlite3

# Connect to the database
conn = sqlite3.connect('database/quotes.db')
cursor = conn.cursor()

# First, let's see what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  {table[0]}")

# Check the schema of the product_models table
cursor.execute("PRAGMA table_info(product_models)")
columns = cursor.fetchall()
print("\nProduct models table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Now check LS2100 price with correct column names
cursor.execute("SELECT * FROM product_models WHERE model_number = 'LS2100'")
result = cursor.fetchone()

if result:
    print(f"\nLS2100 found: {result}")
else:
    print("\nLS2100 not found in database")

# Also check a few other models for comparison
cursor.execute("SELECT model_number, base_price FROM product_models WHERE model_number IN ('LS2000', 'LS2100', 'LS6000') ORDER BY model_number")
results = cursor.fetchall()

print("\nComparison of model prices:")
for model_number, base_price in results:
    print(f"{model_number}: ${base_price}")

conn.close() 
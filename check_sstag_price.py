import sqlite3

# Connect to the database
conn = sqlite3.connect('database/quotes.db')
cursor = conn.cursor()

# Check SSTAG option price
cursor.execute("SELECT code, name, price FROM options WHERE code = 'SSTAG'")
result = cursor.fetchone()

if result:
    print(f"SSTAG option found:")
    print(f"  Code: {result[0]}")
    print(f"  Name: {result[1]}")
    print(f"  Price: ${result[2]}")
    
    if result[2] == 35.0:
        print("✅ SSTAG price successfully updated to $35.00")
    else:
        print(f"❌ SSTAG price is ${result[2]}, expected $35.00")
else:
    print("❌ SSTAG option not found in database")

# Also check a few other options for comparison
cursor.execute("SELECT code, name, price FROM options WHERE code IN ('XSP', 'VR', 'SSTAG', 'SSHOUSING') ORDER BY code")
results = cursor.fetchall()

print("\nComparison of option prices:")
for code, name, price in results:
    print(f"{code}: ${price}")

conn.close() 
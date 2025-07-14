import sqlite3

# Connect to the database
conn = sqlite3.connect('database/quotes.db')
cursor = conn.cursor()

# Check 1/2 inch NPT process connection price
cursor.execute("SELECT type, size, material, price, description FROM process_connections WHERE type = 'NPT' AND size = '1/2\"'")
result = cursor.fetchone()

if result:
    print(f"1/2 inch NPT process connection found:")
    print(f"  Type: {result[0]}")
    print(f"  Size: {result[1]}")
    print(f"  Material: {result[2]}")
    print(f"  Price: ${result[3]}")
    print(f"  Description: {result[4]}")
    
    if result[3] == 70.0:
        print("✅ 1/2 inch NPT price successfully set to $70.00")
    else:
        print(f"❌ 1/2 inch NPT price is ${result[3]}, expected $70.00")
else:
    print("❌ 1/2 inch NPT process connection not found in database")

# Also check other NPT connections for comparison
cursor.execute("SELECT size, price FROM process_connections WHERE type = 'NPT' ORDER BY size")
results = cursor.fetchall()

print("\nComparison of NPT connection prices:")
for size, price in results:
    print(f"{size}: ${price}")

conn.close() 
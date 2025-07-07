import sqlite3
import os

# Set database path
db_path = 'database/quotes.db'
sql_path = 'database/create_quote_db.sql'

# Remove existing database
if os.path.exists(db_path):
    os.remove(db_path)
    print("Removed existing database")

# Create new database from SQL script
conn = sqlite3.connect(db_path)
with open(sql_path, 'r') as f:
    sql_script = f.read()

conn.executescript(sql_script)
conn.close()

print("Database recreated successfully!")
print("The following changes have been applied:")
print("PRODUCT MODELS TABLE:")
print("- Added default_process_connection_type column")
print("- Added default_process_connection_material column") 
print("- Added default_process_connection_size column")
print("- Updated all models with correct NPT/Flange connection specs")
print("INSULATORS TABLE:")
print("- Removed standard_length column")
print("- Changed all compatible_models to 'ALL'")
print("MATERIALS TABLE:")
print("- Added new Cable (C) material: base_adder=80, length_adder=45/foot")
print("- Zeroed out all adders for exotic materials (A, HC, HB, TT)")
print("- Changed all compatible_models to 'ALL'") 
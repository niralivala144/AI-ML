import sqlite3

# Step 1: File paths
sql_file = "database_sqlite.sql"   # ya database_sqlite.sql agar usme correct tables hain
db_file = "travel.db"

# Step 2: Read SQL file
with open(sql_file, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Step 3: Execute SQL commands
conn = sqlite3.connect(db_file)
conn.executescript(sql_script)
conn.commit()
conn.close()

print("✅ SQL file imported successfully into travel.db")


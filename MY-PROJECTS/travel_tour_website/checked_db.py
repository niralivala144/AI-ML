import sqlite3

conn = sqlite3.connect('travel.db')  # ya 'travelers.db' if that's your DB name
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users);")
for col in cursor.fetchall():
    print(col)

conn.close()
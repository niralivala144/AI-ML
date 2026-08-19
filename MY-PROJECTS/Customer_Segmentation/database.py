import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "customer_segmentation.db")

def get_connection():
    """Returns a SQLite database connection with row factory enabled."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema for application customers."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # Customers Table (standalone application customers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL,
        annual_income REAL NOT NULL,
        spending_score INTEGER NOT NULL,
        cluster INTEGER NOT NULL,
        segment_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_cluster ON customers(cluster);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name);")

    conn.commit()
    conn.close()

def save_new_customer(name, gender, age, annual_income, spending_score, cluster, segment_name):
    """Saves a new analyzed customer to SQLite or updates if exact same name exists."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Check if customer with identical name already exists to prevent duplicate spam
        cursor.execute("SELECT id FROM customers WHERE LOWER(name) = ?", (name.strip().lower(),))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("""
                UPDATE customers
                SET gender = ?, age = ?, annual_income = ?, spending_score = ?,
                    cluster = ?, segment_name = ?, created_at = ?
                WHERE id = ?
            """, (gender, int(age), float(annual_income), int(spending_score),
                  int(cluster), segment_name, now, existing['id']))
            conn.commit()
            return existing['id'], "Customer profile updated in database."
        else:
            cursor.execute("""
                INSERT INTO customers (name, gender, age, annual_income, spending_score, cluster, segment_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name.strip(), gender, int(age), float(annual_income), int(spending_score),
                  int(cluster), segment_name, now))
            conn.commit()
            return cursor.lastrowid, "New customer successfully saved to database."
    except Exception as e:
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

def get_all_app_customers():
    """Retrieves all application customer records stored in SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

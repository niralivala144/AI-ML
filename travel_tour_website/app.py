import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'change-this-secret')

# ========================
# 🔹 Database Functions
# ========================

def get_db_path():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'travel.db')  # Path to your database file

def get_db_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ========================
# 🔹 Routes
# ========================

@app.route('/')
def home():
    return render_template('index.html')  # Make sure index.html exists in /templates

# ------------------------
# 🔸 LOGIN
# ------------------------
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('pwd')
    email = request.form.get('email') or f"{name}@example.com"

    if name and password:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (name, password, email))
        conn.commit()
        conn.close()
        flash("✅ Login successful & saved to database!", "success")
    else:
        flash("⚠️ Please enter both name and password.", "error")
    return redirect(url_for('home'))
# ------------------------
# 🔸 DESTINATION
# ------------------------
@app.route('/destination', methods=['POST'])
def destination():
    place = request.form.get('place')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    travelers = request.form.get('travelers')

    if place and start_date and end_date and travelers:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO destinations (place, start_date, end_date, travelers)
            VALUES (?, ?, ?, ?)
        """, (place, start_date, end_date, travelers))
        conn.commit()
        conn.close()
        flash(f"✅ Destination '{place}' added successfully for {travelers} travelers!", "success")
    else:
        flash("⚠️ Please fill in all destination details.", "error")

    return redirect(url_for('home'))
# ------------------------
# 🔸 BOOKING
# ------------------------
@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    if name and email and phone:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO bookings (user_id, booking_type, item_id, seat_number, passenger_name, passenger_email, amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (1, "flight", 1, "A1", name, email, 5000.00, "confirmed"))
        
        conn.commit()
        conn.close()
        flash("✅ Booking successful!", "success")
    else:
        flash("⚠️ Please fill in all booking details.", "error")

    return redirect(url_for('home'))
# ------------------------
# 🔸 PAYMENT
# ------------------------
@app.route('/payment', methods=['POST'])
def payment():
    email = request.form.get('email')
    card_number = request.form.get('card-number')
    expiry_date = request.form.get('expiry-date')
    cvv = request.form.get('cvv')
    method = request.form.get('payment-method')

    if email and card_number and expiry_date and cvv and method:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO payments (email, card_number, expiry_date, cvv, method)
            VALUES (?, ?, ?, ?, ?)
        """, (email, card_number, expiry_date, cvv, method))
        conn.commit()
        conn.close()
        flash("✅ Payment processed successfully!", "success")
    else:
        flash("⚠️ Please fill in all payment details.", "error")

    return redirect(url_for('home'))
# ------------------------
# 🔸 FEEDBACK
# ------------------------
@app.route('/feedback', methods=['POST'])
def feedback():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    message = request.form.get('yourfeedback')

    if fname and lname and message:
        full_name = f"{fname} {lname}"
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO feedback (name, email, message)
            VALUES (?, ?, ?)
        """, (full_name, f"{fname.lower()}@example.com", message))
        conn.commit()
        conn.close()
        flash("🙏 Thank you for your feedback!", "success")
    else:
        flash("⚠️ Please fill out all feedback fields.", "error")

    return redirect(url_for('home'))
# ========================
# 🔹 Run the App
# ========================
if __name__ == '__main__':
    app.run(debug=True)
🧳 Travel Recommendation & Booking System

A full-stack Travel Website built using Flask (Python), SQLite, HTML, CSS, and JavaScript.
This project allows users to explore destinations, view prices, book trips, make payments, and submit feedback — all in one platform.

🚀 Features

🔐 User Login System

🌍 Popular Destinations Showcase

🗺️ Interactive Map (Leaflet.js)

🧾 Trip Booking System

💳 Payment Form

💬 Feedback System

🗃️ SQLite Database Integration

🎨 Responsive UI with CSS

🛠️ Tech Stack

Frontend

HTML5

CSS3

JavaScript

Leaflet.js (Map)

Font Awesome

Backend

Python

Flask

Database

SQLite3

📂 Project Structure
travel_recommendation_system/
│
├── app.py
├── travel.db
├── check_db.py
├── data_setup.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── styles.css
│   └── images/
│       ├── hero.jpg
│       ├── goa.jpg
│       ├── manali.jpg
│       ├── jaipur.jpg
│       ├── kerala.jpg
│       └── logo.jpg
│
└── README.md

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/travel-recommendation-system.git
cd travel-recommendation-system

2️⃣ Install Dependencies
pip install flask

3️⃣ Create Database

Run this once:

python data_setup.py


(Optional) Verify tables:

python check_db.py

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000

🗄️ Database Tables

users

destinations

flights

buses

hotels

bookings

payments

feedback

📸 Screenshots

✔ Home Page
✔ Destination Section
✔ Booking & Payment
✔ Interactive Map
✔ Feedback Form

(Add screenshots in GitHub later if you want)

🎯 Learning Outcomes

Flask routing & templates

SQLite database integration

Full-stack project structure

Form handling & validation

Real-world project deployment flow

📌 Future Improvements

Authentication with sessions

Real payment gateway integration

Admin dashboard

Recommendation using ML

Deployment on Render / Railway

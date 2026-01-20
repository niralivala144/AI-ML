

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Drop existing tables if any (safe recreate)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS buses;
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS destinations;
DROP TABLE IF EXISTS users;

-- ===== USERS =====
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

INSERT INTO users (username, email, password) VALUES
('NiraliV', 'nirali@example.com', 'nirali123'),
('RahulS', 'rahulsharma@example.com', 'rahul123'),
('PriyaP', 'priya.patel@example.com', 'priya123'),
('AmitS', 'amit.singh@example.com', 'amit123'),
('KavyaM', 'kavya.mehta@example.com', 'kavya123'),
('RohitJ', 'rohit.jain@example.com', 'rohit123'),
('SnehaD', 'sneha.desai@example.com', 'sneha123'),
('AnkitV', 'ankit.verma@example.com', 'ankit123'),
('NehaG', 'neha.gupta@example.com', 'neha123'),
('VikasT', 'vikas.thakur@example.com', 'vikas123');

-- ===== DESTINATIONS =====
CREATE TABLE destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO destinations (name, description) VALUES
('Goa', 'Famous for beaches, nightlife, and water sports.'),
('Manali', 'Beautiful hill station surrounded by snow-capped mountains.'),
('Jaipur', 'Known as the Pink City, rich in culture and history.'),
('Kerala', 'Famous for backwaters, houseboats, and greenery.'),
('Leh Ladakh', 'Adventure destination known for mountains and monasteries.'),
('Kashmir', 'Heaven on Earth with valleys, lakes, and snow-covered peaks.');

-- ===== FLIGHTS =====
CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline TEXT NOT NULL,
    flight_number TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_datetime TEXT NOT NULL,
    arrival_datetime TEXT NOT NULL,
    price REAL NOT NULL,
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL
);

INSERT INTO flights (airline, flight_number, origin, destination, departure_datetime, arrival_datetime, price, total_seats, available_seats) VALUES
('IndiGo', '6E-201', 'Delhi', 'Mumbai', '2025-11-01 08:00:00', '2025-11-01 10:00:00', 4500.00, 180, 180),
('Air India', 'AI-305', 'Mumbai', 'Goa', '2025-11-02 09:30:00', '2025-11-02 10:45:00', 3800.00, 160, 160),
('SpiceJet', 'SG-410', 'Chennai', 'Bengaluru', '2025-11-03 07:15:00', '2025-11-03 08:10:00', 2500.00, 150, 150),
('Vistara', 'UK-550', 'Delhi', 'Kolkata', '2025-11-04 13:00:00', '2025-11-04 15:30:00', 5200.00, 170, 170),
('Go First', 'G8-102', 'Pune', 'Hyderabad', '2025-11-05 06:30:00', '2025-11-05 07:40:00', 3100.00, 140, 140),
('IndiGo', '6E-340', 'Bengaluru', 'Jaipur', '2025-11-06 11:45:00', '2025-11-06 14:15:00', 5700.00, 180, 180),
('Air India', 'AI-720', 'Delhi', 'Leh', '2025-11-07 05:45:00', '2025-11-07 08:15:00', 6900.00, 150, 150),
('Vistara', 'UK-220', 'Ahmedabad', 'Delhi', '2025-11-08 18:30:00', '2025-11-08 20:00:00', 4200.00, 160, 160),
('SpiceJet', 'SG-510', 'Kolkata', 'Guwahati', '2025-11-09 07:00:00', '2025-11-09 08:10:00', 2700.00, 140, 140),
('Air Asia', 'I5-870', 'Delhi', 'Chandigarh', '2025-11-10 09:00:00', '2025-11-10 09:50:00', 2300.00, 120, 120);

-- ===== BUSES =====
CREATE TABLE buses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator TEXT NOT NULL,
    bus_number TEXT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_datetime TEXT NOT NULL,
    arrival_datetime TEXT NOT NULL,
    price REAL NOT NULL,
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL
);

INSERT INTO buses (operator, bus_number, origin, destination, departure_datetime, arrival_datetime, price, total_seats, available_seats) VALUES
('RedBus Travels', 'RB-101', 'Ahmedabad', 'Udaipur', '2025-11-01 21:00:00', '2025-11-02 03:30:00', 750.00, 40, 40),
('Shiv Shakti Travels', 'SS-204', 'Delhi', 'Jaipur', '2025-11-02 22:00:00', '2025-11-03 03:00:00', 600.00, 45, 45),
('Patel Tours', 'PT-330', 'Mumbai', 'Goa', '2025-11-03 19:30:00', '2025-11-04 07:00:00', 1200.00, 50, 50),
('VRL Travels', 'VRL-515', 'Bengaluru', 'Hyderabad', '2025-11-04 21:00:00', '2025-11-05 05:00:00', 950.00, 48, 48),
('Neeta Travels', 'NT-432', 'Pune', 'Mumbai', '2025-11-05 06:30:00', '2025-11-05 10:00:00', 500.00, 40, 40),
('Raj Express', 'RE-208', 'Lucknow', 'Delhi', '2025-11-06 19:00:00', '2025-11-07 06:00:00', 850.00, 52, 52),
('Orange Travels', 'OT-775', 'Hyderabad', 'Chennai', '2025-11-07 22:30:00', '2025-11-08 06:30:00', 900.00, 46, 46),
('SRS Travels', 'SRS-889', 'Bengaluru', 'Mysuru', '2025-11-08 07:30:00', '2025-11-08 10:30:00', 400.00, 40, 40),
('GSRTC', 'GS-110', 'Surat', 'Ahmedabad', '2025-11-09 15:00:00', '2025-11-09 19:00:00', 350.00, 55, 55),
('Hans Travels', 'HT-999', 'Indore', 'Bhopal', '2025-11-10 17:00:00', '2025-11-10 21:00:00', 500.00, 50, 50);

-- ===== HOTELS =====
CREATE TABLE hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    price_per_night REAL NOT NULL,
    total_rooms INTEGER NOT NULL,
    available_rooms INTEGER NOT NULL
);

INSERT INTO hotels (name, city, address, price_per_night, total_rooms, available_rooms) VALUES
('Taj Mahal Palace', 'Mumbai', 'Apollo Bunder, Colaba', 12000.00, 100, 100),
('The Oberoi', 'Bengaluru', 'MG Road', 9500.00, 80, 80),
('ITC Grand Chola', 'Chennai', 'Guindy', 8500.00, 90, 90),
('The Leela Palace', 'Delhi', 'Chanakyapuri', 11000.00, 70, 70),
('Radisson Blu', 'Jaipur', 'M.I. Road', 6000.00, 60, 60),
('Lalit Jaipur', 'Jaipur', 'Bani Park', 5500.00, 50, 50),
('Marriott', 'Goa', 'Panaji', 8000.00, 75, 75),
('Novotel', 'Pune', 'Camp', 4500.00, 60, 60),
('Hyatt Regency', 'Ahmedabad', 'Navrangpura', 7000.00, 65, 65),
('Fortune Park', 'Kolkata', 'Park Street', 5000.00, 55, 55);

-- ===== BOOKINGS =====
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    booking_type TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    seat_number TEXT,
    passenger_name TEXT NOT NULL,
    passenger_email TEXT,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'confirmed',
    booked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

INSERT INTO bookings (user_id, booking_type, item_id, seat_number, passenger_name, passenger_email, amount, status, booked_at) VALUES
(1, 'flight', 1, '12A', 'Nirali Vala', 'nirali@example.com', 6500.00, 'confirmed', '2025-10-10 09:45:00'),
(2, 'flight', 3, '14B', 'Ravi Patel', 'ravi@example.com', 8200.00, 'confirmed', '2025-10-11 15:30:00'),
(3, 'flight', 5, '18C', 'Aditi Sharma', 'aditi@example.com', 5500.00, 'pending', '2025-10-12 20:10:00'),
(4, 'flight', 7, '22D', 'Vikas Mehta', 'vikas@example.com', 7200.00, 'cancelled', '2025-10-13 08:15:00'),
(5, 'flight', 9, '9F', 'Karan Joshi', 'karan@example.com', 9400.00, 'confirmed', '2025-10-14 13:25:00'),
(6, 'bus', 2, '5', 'Priya Singh', 'priya@example.com', 600.00, 'confirmed', '2025-10-15 22:00:00'),
(7, 'bus', 4, '18', 'Rohan Desai', 'rohan@example.com', 950.00, 'pending', '2025-10-16 19:45:00'),
(8, 'bus', 6, '8', 'Manisha Verma', 'manisha@example.com', 850.00, 'confirmed', '2025-10-17 20:10:00'),
(9, 'bus', 8, '12', 'Jay Mehta', 'jay@example.com', 400.00, 'cancelled', '2025-10-18 09:20:00'),
(10, 'bus', 10, '22', 'Sneha Raval', 'sneha@example.com', 500.00, 'confirmed', '2025-10-19 18:35:00');

-- ===== PAYMENTS =====
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    amount REAL NOT NULL
);

INSERT INTO payments (name, email, amount) VALUES
('Nirali Vala', 'nirali@example.com', 2500.00),
('Rahul Sharma', 'rahulsharma@example.com', 3200.50),
('Priya Patel', 'priya.patel@example.com', 1800.00),
('Amit Singh', 'amit.singh@example.com', 4500.75),
('Kavya Mehta', 'kavya.mehta@example.com', 2999.00),
('Rohit Jain', 'rohit.jain@example.com', 5200.00),
('Sneha Desai', 'sneha.desai@example.com', 4100.25),
('Ankit Verma', 'ankit.verma@example.com', 1500.00),
('Neha Gupta', 'neha.gupta@example.com', 3800.00),
('Vikas Thakur', 'vikas.thakur@example.com', 2700.50);

-- ===== FEEDBACK =====
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL
);

INSERT INTO feedback (name, email, message) VALUES
('Nirali Vala', 'nirali@example.com', 'Amazing travel site! The recommendations were perfect.'),
('Rahul Sharma', 'rahulsharma@example.com', 'Very user-friendly interface and fast results.'),
('Priya Patel', 'priya.patel@example.com', 'Loved the beach destinations suggestions.'),
('Amit Singh', 'amit.singh@example.com', 'Payment and feedback system works smoothly.'),
('Kavya Mehta', 'kavya.mehta@example.com', 'The site could use more hill station options, otherwise great!'),
('Rohit Jain', 'rohit.jain@example.com', 'I found my ideal trip to Manali using this system.'),
('Sneha Desai', 'sneha.desai@example.com', 'Easy to use, clean design, and accurate results.'),
('Ankit Verma', 'ankit.verma@example.com', 'Would love to see hotel recommendations added too.'),
('Neha Gupta', 'neha.gupta@example.com', 'Loved the visuals and map integration.'),
('Vikas Thakur', 'vikas.thakur@example.com', 'Great for planning trips under a budget!');

COMMIT;

import streamlit as st
import sqlite3
import hashlib
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="🥔 PotatoGuard AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------
# Hide Sidebar & Streamlit Default UI
# -------------------------
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ===== GLOBAL FONTS ===== */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

/* ===== ANIMATED BACKGROUND ===== */
.stApp {
    background: #020c06;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(0,255,100,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(0,200,80,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(0,150,60,0.04) 0%, transparent 40%);
    min-height: 100vh;
}

/* ===== GRID OVERLAY ===== */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,255,80,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,80,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ===== MAIN CARD ===== */
.glass-card {
    background: rgba(5, 25, 12, 0.85);
    border: 1px solid rgba(0, 255, 100, 0.2);
    border-radius: 20px;
    padding: 40px;
    box-shadow:
        0 0 40px rgba(0,255,80,0.08),
        0 0 80px rgba(0,255,80,0.04),
        inset 0 1px 0 rgba(0,255,100,0.15);
    backdrop-filter: blur(20px);
    margin: 20px 0;
}

/* ===== LOGO / TITLE ===== */
.logo-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.8em;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00ff64, #00cc50, #00ff64);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    letter-spacing: 3px;
    margin-bottom: 5px;
}

.logo-sub {
    font-family: 'Rajdhani', sans-serif;
    text-align: center;
    color: rgba(0,255,100,0.5);
    font-size: 0.95em;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 35px;
}

@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* ===== SCAN LINE ANIMATION ===== */
@keyframes scanline {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}

/* ===== INPUTS ===== */
.stTextInput > div > div > input {
    background: rgba(0, 255, 100, 0.05) !important;
    border: 1px solid rgba(0, 255, 100, 0.25) !important;
    border-radius: 10px !important;
    color: #00ff64 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1em !important;
    letter-spacing: 1px;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0, 255, 100, 0.7) !important;
    box-shadow: 0 0 15px rgba(0,255,100,0.2) !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(0,255,100,0.3) !important;
}
.stTextInput label {
    color: rgba(0,255,100,0.7) !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 2px;
    font-size: 0.85em !important;
    text-transform: uppercase;
}

/* ===== BUTTONS ===== */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(0,200,80,0.2), rgba(0,255,100,0.1)) !important;
    border: 1px solid rgba(0,255,100,0.5) !important;
    border-radius: 10px !important;
    color: #00ff64 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.85em !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    padding: 14px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,255,100,0.3), rgba(0,200,80,0.2)) !important;
    box-shadow: 0 0 25px rgba(0,255,100,0.3), 0 0 50px rgba(0,255,100,0.1) !important;
    transform: translateY(-1px) !important;
    border-color: #00ff64 !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,255,100,0.05);
    border-radius: 12px;
    gap: 5px;
    padding: 5px;
    border: 1px solid rgba(0,255,100,0.1);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(0,255,100,0.5) !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.75em !important;
    letter-spacing: 2px;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,255,100,0.15) !important;
    color: #00ff64 !important;
    border: 1px solid rgba(0,255,100,0.3) !important;
}

/* ===== ALERTS ===== */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid rgba(0,255,100,0.2) !important;
}
div[data-testid="stSuccessMessage"] {
    background: rgba(0,255,100,0.08) !important;
    border-color: rgba(0,255,100,0.3) !important;
    color: #00ff64 !important;
}
div[data-testid="stErrorMessage"] {
    background: rgba(255,50,50,0.08) !important;
    border-color: rgba(255,50,50,0.3) !important;
}

/* ===== DIVIDER ===== */
.neon-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,100,0.4), transparent);
    margin: 25px 0;
}

.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #00ff64;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse-dot 2s infinite;
    box-shadow: 0 0 8px #00ff64;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

.system-text {
    color: rgba(0,255,100,0.4);
    font-size: 0.8em;
    letter-spacing: 2px;
    text-align: center;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# DB Setup
# -------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS history
             (username TEXT, result TEXT, confidence REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

def register_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# -------------------------
# Session Init
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""

# -------------------------
# Auto Redirect if Logged In
# -------------------------
if st.session_state.logged_in:
    st.switch_page("pages/home.py")

# -------------------------
# UI
# -------------------------
st.markdown("""
<div style='text-align:center; padding: 30px 0 10px 0;'>
    <div style='font-family:Orbitron,sans-serif; font-size:3em; font-weight:900;
        background: linear-gradient(135deg, #00ff64, #00cc50);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing:3px;'>
        🥔 POTATO<span style='-webkit-text-fill-color:rgba(0,255,100,0.5);'>GUARD</span>
    </div>
    <div style='color:rgba(0,255,100,0.45); font-size:0.8em; letter-spacing:8px;
        font-family:Rajdhani,sans-serif; margin-top:5px;'>
        AI PLANT DISEASE DETECTION SYSTEM
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🔐  LOGIN", "📝  REGISTER"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter username", key="login_user")
    password = st.text_input("Password", placeholder="Enter password", type="password", key="login_pass")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  INITIALIZE SESSION", key="login_btn"):
        if username and password:
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("✅ Access Granted! Loading System...")
                st.switch_page("pages/home.py")
            else:
               st.error("❌ Invalid credentials. Access Denied.")
        else:
            st.warning("⚠️ Please fill all fields.")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    new_user = st.text_input("Choose Username", placeholder="Create username", key="reg_user")
    new_pass = st.text_input("Choose Password", placeholder="Create password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", placeholder="Re-enter password", type="password", key="reg_confirm")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🌱  CREATE ACCOUNT", key="reg_btn"):
        if new_user and new_pass and confirm_pass:
            if new_pass != confirm_pass:
                st.error("❌ Passwords do not match.")
            elif len(new_pass) < 4:
                st.warning("⚠️ Password must be at least 4 characters.")
            else:
                if register_user(new_user, new_pass):
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Username already exists.")
        else:
            st.warning("⚠️ Please fill all fields.")

st.markdown("""
<div class='system-text'>
    <span class='status-dot'></span>
    SYSTEM ONLINE &nbsp;|&nbsp; MODEL v2.1 &nbsp;|&nbsp; CNN ARCHITECTURE
</div>
""", unsafe_allow_html=True)

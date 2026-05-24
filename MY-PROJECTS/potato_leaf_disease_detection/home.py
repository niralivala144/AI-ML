import streamlit as st
import numpy as np
from PIL import Image
import sqlite3
import sys
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="KisanGuard AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# Hide Sidebar & Default UI
# -------------------------
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.stApp {
    background: #020c06;
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(0,255,100,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(0,200,80,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(0,100,40,0.03) 0%, transparent 70%);
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,255,80,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,80,0.025) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

.section-card {
    background: rgba(5, 20, 10, 0.8);
    border: 1px solid rgba(0,255,100,0.12);
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 0 30px rgba(0,255,80,0.05);
    backdrop-filter: blur(15px);
    position: relative;
    overflow: hidden;
}
.section-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,255,100,0.5), transparent);
}

.sec-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.9em;
    font-weight: 700;
    color: rgba(0,255,100,0.7);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.result-healthy {
    background: rgba(0,255,100,0.08);
    border: 1px solid rgba(0,255,100,0.35);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}
.result-early {
    background: rgba(255,160,0,0.08);
    border: 1px solid rgba(255,160,0,0.35);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}
.result-late {
    background: rgba(255,60,60,0.08);
    border: 1px solid rgba(255,60,60,0.35);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}

.result-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.4em;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 10px;
}
.healthy-text { color: #00ff64; }
.early-text { color: #ffa040; }
.late-text { color: #ff4040; }

.confidence-bar-wrap {
    background: rgba(0,0,0,0.3);
    border-radius: 10px;
    height: 10px;
    margin: 15px 0;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}
.confidence-bar-healthy { background: linear-gradient(90deg, #00cc50, #00ff64); border-radius: 10px; height: 100%; }
.confidence-bar-early { background: linear-gradient(90deg, #cc8000, #ffa040); border-radius: 10px; height: 100%; }
.confidence-bar-late { background: linear-gradient(90deg, #cc2020, #ff4040); border-radius: 10px; height: 100%; }

.solution-box {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
    font-size: 0.95em;
    line-height: 1.7;
    color: rgba(255,255,255,0.75);
    letter-spacing: 0.5px;
}
.solution-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.7em;
    letter-spacing: 3px;
    color: rgba(0,255,100,0.5);
    margin-bottom: 10px;
}

.chat-wrap {
    max-height: 320px;
    overflow-y: auto;
    padding: 10px;
    scrollbar-width: thin;
    scrollbar-color: rgba(0,255,80,0.2) transparent;
}
.chat-bubble-user {
    background: rgba(0,255,100,0.1);
    border: 1px solid rgba(0,255,100,0.2);
    border-radius: 14px 14px 4px 14px;
    padding: 10px 16px;
    margin: 8px 0 8px 40px;
    color: #00ff64;
    font-size: 0.92em;
}
.chat-bubble-bot {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px 14px 14px 4px;
    padding: 10px 16px;
    margin: 8px 40px 8px 0;
    color: rgba(255,255,255,0.75);
    font-size: 0.92em;
}
.bot-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65em;
    color: rgba(0,255,100,0.4);
    letter-spacing: 2px;
    margin-bottom: 4px;
}

.history-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0,255,80,0.06);
    font-size: 0.9em;
    color: rgba(255,255,255,0.65);
}
.history-badge-healthy {
    background: rgba(0,255,100,0.12);
    border: 1px solid rgba(0,255,100,0.25);
    color: #00ff64; border-radius: 20px; padding: 3px 12px; font-size:0.8em;
}
.history-badge-early {
    background: rgba(255,160,0,0.12);
    border: 1px solid rgba(255,160,0,0.25);
    color: #ffa040; border-radius: 20px; padding: 3px 12px; font-size:0.8em;
}
.history-badge-late {
    background: rgba(255,60,60,0.12);
    border: 1px solid rgba(255,60,60,0.25);
    color: #ff6060; border-radius: 20px; padding: 3px 12px; font-size:0.8em;
}

[data-testid="stFileUploader"] {
    background: rgba(0,255,100,0.03) !important;
    border: 2px dashed rgba(0,255,100,0.2) !important;
    border-radius: 15px !important;
    padding: 20px !important;
}

.stTextInput > div > div > input {
    background: rgba(0,255,100,0.04) !important;
    border: 1px solid rgba(0,255,100,0.2) !important;
    border-radius: 10px !important;
    color: #00ff64 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1em !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,255,100,0.6) !important;
    box-shadow: 0 0 12px rgba(0,255,100,0.15) !important;
}
.stTextInput label {
    color: rgba(0,255,100,0.6) !important;
    font-size: 0.8em !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Logout button — small, red-tinted */
div[data-testid="column"]:last-child .stButton > button {
    background: linear-gradient(135deg, rgba(255,50,50,0.15), rgba(255,80,80,0.08)) !important;
    border: 1px solid rgba(255,80,80,0.4) !important;
    color: #ff6060 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.7em !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    width: auto !important;
}
div[data-testid="column"]:last-child .stButton > button:hover {
    background: rgba(255,60,60,0.25) !important;
    box-shadow: 0 0 15px rgba(255,60,60,0.2) !important;
    border-color: #ff4040 !important;
}

/* All other buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,200,80,0.15), rgba(0,255,100,0.08)) !important;
    border: 1px solid rgba(0,255,100,0.4) !important;
    border-radius: 10px !important;
    color: #00ff64 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.75em !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
}
.stButton > button:hover {
    background: rgba(0,255,100,0.2) !important;
    box-shadow: 0 0 20px rgba(0,255,100,0.2) !important;
    border-color: #00ff64 !important;
}

.neon-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,100,0.3), transparent);
    margin: 20px 0;
}

.stat-box {
    background: rgba(0,255,100,0.05);
    border: 1px solid rgba(0,255,100,0.12);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}
.stat-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.8em;
    font-weight: 900;
    color: #00ff64;
}
.stat-label {
    color: rgba(0,255,100,0.45);
    font-size: 0.75em;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

@keyframes pulse-anim {
    0%, 100% { opacity:1; transform:scale(1); }
    50% { opacity:0.3; transform:scale(0.7); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# DB Connection
# -------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS history
             (username TEXT, result TEXT, confidence REAL)''')
conn.commit()

try:
    c.execute("ALTER TABLE history ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP")
    conn.commit()
except Exception:
    pass

# -------------------------
# Import preprocess
# -------------------------
sys.path.append(os.path.abspath("utils"))
from utils.processes import preprocess_image

# -------------------------
# Login Check
# -------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.stop()

# -------------------------
# Load Model
# -------------------------
from tensorflow.keras.models import load_model

@st.cache_resource
def load_cnn_model():
    return load_model("model/potato_disease_cnn.h5")

model = load_cnn_model()

class_names = ["Potato_Healthy", "Potato_Late_blight", "Potato_Early_blight"]

solutions = {
    "Potato_Healthy": """
        ✅ Your potato plant is perfectly healthy!<br><br>
        🌱 <b>Maintenance Tips:</b><br>
        • Water consistently — 1-2 inches per week<br>
        • Ensure 6-8 hours of sunlight daily<br>
        • Monitor for early signs of pests<br>
        • Apply balanced NPK fertilizer monthly<br>
        • Keep soil well-drained to avoid root rot
    """,
    "Potato_Early_blight": """
        🟠 <b>Early Blight Detected</b> (Alternaria solani)<br><br>
        💊 <b>Treatment Protocol:</b><br>
        • Remove and destroy infected leaves immediately<br>
        • Apply <b>Mancozeb</b> (2.5g/liter) fungicide spray<br>
        • Repeat spray every 7-10 days<br>
        • Avoid overhead irrigation<br>
        • Improve air circulation around plants<br>
        • Apply copper-based fungicide as preventive
    """,
    "Potato_Late_blight": """
        🔴 <b>Late Blight Detected</b> (Phytophthora infestans)<br><br>
        🚨 <b>Urgent Treatment Required:</b><br>
        • Apply <b>Metalaxyl</b> (2ml/liter) immediately<br>
        • Remove heavily infected plants to stop spread<br>
        • Spray Cymoxanil + Mancozeb combination<br>
        • Avoid working in wet/humid conditions<br>
        • Ensure proper field drainage<br>
        • Repeat spray every 5-7 days until controlled
    """
}

# ==============================
# TOP NAV BAR — Username Left | Status Center | Logout Right
# ==============================
col_nav1, col_nav2, col_nav3 = st.columns([3, 3, 2])

with col_nav1:
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:12px; padding:8px 0;'>
        <div style='font-family:Orbitron,sans-serif; font-size:1em; font-weight:900;
            background:linear-gradient(135deg,#00ff64,#00cc50);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text; letter-spacing:3px;'>
            🌱 KisanGuard
        </div>
        <div style='color:rgba(0,255,100,0.5); font-size:0.85em; letter-spacing:2px;
            background:rgba(0,255,80,0.08); border:1px solid rgba(0,255,80,0.2);
            border-radius:20px; padding:3px 12px;'>
            👤 {st.session_state.user.upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_nav2:
    st.markdown("""
    <div style='text-align:center; padding:10px 0;'>
        <span style='background:rgba(0,255,80,0.1); border:1px solid rgba(0,255,80,0.3);
        border-radius:20px; padding:5px 16px; color:#00ff64; font-size:0.78em; letter-spacing:2px;'>
        <span style='display:inline-block; width:7px; height:7px; background:#00ff64;
        border-radius:50%; margin-right:6px; animation:pulse-anim 2s infinite;
        box-shadow:0 0 8px #00ff64; vertical-align:middle;'></span>
        SYSTEM ACTIVE
        </span>
    </div>""", unsafe_allow_html=True)

with col_nav3:
    # Logout button — top right
    if st.button("🚪 LOGOUT", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.session_state.messages = []
        st.switch_page("pages/app.py")

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# STATS ROW
# -------------------------
c.execute("SELECT COUNT(*) FROM history WHERE username=?", (st.session_state.user,))
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM history WHERE username=? AND result='Potato_Healthy'", (st.session_state.user,))
healthy_count = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM history WHERE username=? AND result!='Potato_Healthy'", (st.session_state.user,))
disease_count = c.fetchone()[0]

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"""<div class='stat-box'>
        <div class='stat-number'>{total}</div>
        <div class='stat-label'>Total Scans</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""<div class='stat-box'>
        <div class='stat-number' style='color:#00ff64;'>{healthy_count}</div>
        <div class='stat-label'>Healthy</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""<div class='stat-box'>
        <div class='stat-number' style='color:#ff6060;'>{disease_count}</div>
        <div class='stat-label'>Diseased</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# MAIN COLUMNS
# -------------------------
col_left, col_right = st.columns([1.1, 1], gap="medium")

# ========================
# LEFT — Upload & Detect
# ========================
with col_left:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>🔬 Scan Leaf Image</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload a potato leaf image",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="", use_container_width=True)

        with st.spinner("🧬 Analyzing..."):
            processed_img = preprocess_image(img)
            prediction = model.predict(processed_img)
            class_index = np.argmax(prediction)
            result = class_names[class_index]
            confidence = float(np.max(prediction) * 100)

        if result == "Potato_Healthy":
            damage_pct = 0.0
            severity = "NONE"
            sev_color = "#00ff64"
        elif result == "Potato_Early_blight":
            damage_pct = round(20 + (confidence / 100) * 40, 1)
            severity = "MILD" if damage_pct < 35 else "MODERATE"
            sev_color = "#ffd040" if damage_pct < 35 else "#ffa040"
        else:
            damage_pct = min(round(50 + (confidence / 100) * 45, 1), 95.0)
            severity = "SEVERE" if damage_pct < 70 else "CRITICAL"
            sev_color = "#ff6040" if damage_pct < 70 else "#ff2020"

        if result == "Potato_Healthy":
            css_class = "result-healthy"
            txt_class = "healthy-text"
            bar_class = "confidence-bar-healthy"
            damage_bar_color = "#00ff64"
            icon = "✅"
        elif result == "Potato_Early_blight":
            css_class = "result-early"
            txt_class = "early-text"
            bar_class = "confidence-bar-early"
            damage_bar_color = "#ffa040"
            icon = "⚠️"
        else:
            css_class = "result-late"
            txt_class = "late-text"
            bar_class = "confidence-bar-late"
            damage_bar_color = "#ff4040"
            icon = "🔴"

        display_name = result.replace("_", " ")
        sev_color_border = sev_color + "40"
        damage_bar_gradient = damage_bar_color + "99"

        result_html = (
            "<div class='" + css_class + "'>"
            "<div class='result-label " + txt_class + "'>" + icon + " " + display_name + "</div>"
            "<div style='display:flex;justify-content:space-between;"
            "color:rgba(255,255,255,0.45);font-size:0.78em;letter-spacing:2px;margin-top:12px;'>"
            "<span>MODEL CONFIDENCE</span>"
            "<span style='color:rgba(255,255,255,0.7);'>" + str(round(confidence, 1)) + "%</span>"
            "</div>"
            "<div class='confidence-bar-wrap'>"
            "<div class='" + bar_class + "' style='width:" + str(round(confidence, 1)) + "%;'></div>"
            "</div>"
            "<div style='display:flex;justify-content:space-between;"
            "color:rgba(255,255,255,0.45);font-size:0.78em;letter-spacing:2px;margin-top:14px;'>"
            "<span>🍂 LEAF DAMAGE SCORE</span>"
            "<span style='color:" + sev_color + ";font-weight:700;'>" + str(damage_pct) + "% &nbsp;"
            "<span style='background:rgba(255,255,255,0.07);border:1px solid " + sev_color_border + ";"
            "border-radius:8px;padding:2px 8px;font-size:0.85em;'>" + severity + "</span>"
            "</span></div>"
            "<div class='confidence-bar-wrap'>"
            "<div style='width:" + str(damage_pct) + "%;height:100%;border-radius:10px;"
            "background:linear-gradient(90deg," + damage_bar_gradient + "," + damage_bar_color + ");'></div>"
            "</div>"
            "</div>"
            "<div class='solution-box'>"
            "<div class='solution-title'>// TREATMENT PROTOCOL</div>"
            + solutions[result] +
            "</div>"
        )

        st.markdown(result_html, unsafe_allow_html=True)

        try:
            c.execute("INSERT INTO history (username, result, confidence) VALUES (?, ?, ?)",
                      (st.session_state.user, result, damage_pct))
            conn.commit()
        except Exception as e:
            st.error(f"Save error: {e}")

    else:
        st.markdown("""
        <div style='text-align:center; padding:50px 20px; color:rgba(0,255,100,0.25);'>
            <div style='font-size:4em; margin-bottom:15px;'>🌿</div>
            <div style='font-family:Orbitron,sans-serif; font-size:0.8em; letter-spacing:3px;'>
                AWAITING IMAGE INPUT
            </div>
            <div style='font-size:0.8em; margin-top:10px; letter-spacing:1px;'>
                Upload a potato leaf to begin analysis
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ========================
# RIGHT — Chatbot + History
# ========================
with col_right:

    # --- CHATBOT ---
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>🤖 Kisan AI Assistant</div>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [("Bot", "Namaste! I am Kisan AI. Ask me about potato diseases, fertilizers, or farming tips. 🌱")]

    chat_html = "<div class='chat-wrap'>"
    for sender, msg in st.session_state.messages:
        if sender == "You":
            chat_html += f"<div class='chat-bubble-user'>👤 {msg}</div>"
        else:
            chat_html += f"<div class='chat-bubble-bot'><div class='bot-name'>// KISAN AI</div>{msg}</div>"
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    def chatbot_response(user_input):
        u = user_input.lower()
        if any(w in u for w in ["early blight", "early"]):
            return "🟠 Early Blight: Remove infected leaves immediately. Spray Mancozeb (2.5g/liter) every 7-10 days. Ensure good air circulation."
        elif any(w in u for w in ["late blight", "late"]):
            return "🔴 Late Blight: Very dangerous! Apply Metalaxyl (2ml/liter) urgently. Remove heavily infected plants. Re-spray every 5 days."
        elif any(w in u for w in ["fertilizer", "khad", "npk"]):
            return "🌿 Use balanced NPK (10-10-10) fertilizer. Apply nitrogen in early growth stage. Potassium improves disease resistance."
        elif any(w in u for w in ["water", "paani", "irrigation"]):
            return "💧 Water 1-2 inches per week. Avoid overhead irrigation. Morning watering is best. Good drainage prevents root rot."
        elif any(w in u for w in ["healthy", "swasth", "normal"]):
            return "✅ Healthy plant! Maintain regular watering, 6-8 hrs sunlight, monthly fertilizing. Check weekly for pests."
        elif any(w in u for w in ["pest", "keeda", "insect"]):
            return "🐛 For pests: Use neem oil spray weekly. Check undersides of leaves. Remove infected plants. Introduce beneficial insects."
        elif any(w in u for w in ["weather", "mausam", "temperature"]):
            return "🌡️ Potatoes grow best at 15-20°C. High humidity (>80%) promotes blight. Ensure good ventilation in humid conditions."
        elif any(w in u for w in ["hello", "hi", "namaste", "hey"]):
            return "🙏 Namaste! I'm Kisan AI, your farming assistant. Ask me about diseases, fertilizers, watering, or pests!"
        else:
            return "🤔 I can help with: potato diseases, fertilizers, irrigation, pest control, and farming tips. Please ask specifically!"

    user_input = st.text_input("Your question...", key="chat_input", label_visibility="collapsed",
                               placeholder="Ask about diseases, fertilizers, farming...")
    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col2:
        ask_btn = st.button("SEND →", key="ask_btn")

    if ask_btn and user_input.strip():
        response = chatbot_response(user_input)
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Bot", response))
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- HISTORY ---
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>📊 Scan History</div>", unsafe_allow_html=True)

    try:
        c.execute("SELECT result, confidence, timestamp FROM history WHERE username=? ORDER BY timestamp DESC LIMIT 8",
                  (st.session_state.user,))
        data = c.fetchall()

        if data:
            for row in data:
                result_name = row[0].replace("_", " ")
                conf = row[1]
                ts = row[2][:10] if row[2] else ""

                if "Healthy" in row[0]:
                    badge = f"<span class='history-badge-healthy'>{result_name}</span>"
                elif "Early" in row[0]:
                    badge = f"<span class='history-badge-early'>{result_name}</span>"
                else:
                    badge = f"<span class='history-badge-late'>{result_name}</span>"

                st.markdown(f"""
                <div class='history-row'>
                    {badge}
                    <span style='color:rgba(0,255,100,0.5); font-size:0.82em;'>{conf:.1f}%</span>
                    <span style='color:rgba(255,255,255,0.25); font-size:0.75em;'>{ts}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center; padding:25px; color:rgba(0,255,100,0.25);
                font-size:0.85em; letter-spacing:2px;'>
                NO SCAN HISTORY YET
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; color:rgba(0,255,100,0.2); font-size:0.72em;
    letter-spacing:3px; margin-top:20px; font-family:Orbitron,sans-serif;'>
    POTATOGUARD AI © 2026 &nbsp;|&nbsp; CNN MODEL v2.1 &nbsp;|&nbsp; ALL RIGHTS RESERVED
</div>
""", unsafe_allow_html=True)
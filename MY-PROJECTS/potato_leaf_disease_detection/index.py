import streamlit as st

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

* { font-family: 'Rajdhani', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }

.stApp {
    background: #020c06;
    background-image:
        radial-gradient(ellipse at 15% 50%, rgba(0,255,100,0.07) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 20%, rgba(0,200,80,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 90%, rgba(0,150,60,0.04) 0%, transparent 40%);
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,255,80,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,80,0.02) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 50px;
    background: rgba(0,255,80,0.03);
    border-bottom: 1px solid rgba(0,255,80,0.08);
    backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3em;
    font-weight: 900;
    background: linear-gradient(135deg, #00ff64, #00cc50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 3px;
}
.nav-status {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,255,80,0.08);
    border: 1px solid rgba(0,255,80,0.2);
    border-radius: 20px;
    padding: 6px 16px;
    color: #00ff64;
    font-size: 0.78em;
    letter-spacing: 2px;
}
.dot-live {
    width: 8px; height: 8px;
    background: #00ff64;
    border-radius: 50%;
    animation: blink 2s infinite;
    box-shadow: 0 0 8px #00ff64;
}
@keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:0.2; }
}

.hero {
    text-align: center;
    padding: 90px 20px 70px 20px;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,255,80,0.08);
    border: 1px solid rgba(0,255,80,0.25);
    border-radius: 30px;
    padding: 7px 20px;
    color: rgba(0,255,100,0.7);
    font-size: 0.8em;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 30px;
}
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.8em;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 20px;
}
.hero-title-white { color: #ffffff; }
.hero-title-green {
    background: linear-gradient(135deg, #00ff64, #00cc50, #00ff64);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer { 0% { background-position:0% center; } 100% { background-position:200% center; } }
.hero-sub {
    color: rgba(255,255,255,0.45);
    font-size: 1.15em;
    max-width: 600px;
    margin: 0 auto 45px auto;
    line-height: 1.7;
    letter-spacing: 0.5px;
}

.stats-row {
    display: flex;
    justify-content: center;
    gap: 50px;
    margin: 50px 0;
    flex-wrap: wrap;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2em;
    font-weight: 900;
    color: #00ff64;
    display: block;
}
.stat-desc {
    color: rgba(255,255,255,0.35);
    font-size: 0.82em;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}
.stat-divider {
    width: 1px;
    background: rgba(0,255,80,0.15);
    align-self: stretch;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6em;
    font-weight: 900;
    text-align: center;
    color: white;
    letter-spacing: 3px;
    margin-bottom: 8px;
}
.section-sub {
    text-align: center;
    color: rgba(255,255,255,0.35);
    font-size: 0.9em;
    letter-spacing: 2px;
    margin-bottom: 45px;
}

.feature-card {
    background: rgba(5,20,10,0.7);
    border: 1px solid rgba(0,255,80,0.1);
    border-radius: 20px;
    padding: 35px 28px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,255,100,0.4), transparent);
}
.feature-card:hover {
    border-color: rgba(0,255,80,0.3);
    box-shadow: 0 0 30px rgba(0,255,80,0.08);
    transform: translateY(-3px);
}
.feature-icon { font-size: 2.5em; margin-bottom: 18px; display: block; }
.feature-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85em;
    font-weight: 700;
    color: #00ff64;
    letter-spacing: 2px;
    margin-bottom: 12px;
}
.feature-desc { color: rgba(255,255,255,0.45); font-size: 0.9em; line-height: 1.7; }

.step-wrap {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 25px;
    background: rgba(5,20,10,0.5);
    border: 1px solid rgba(0,255,80,0.08);
    border-radius: 16px;
    margin-bottom: 15px;
    transition: all 0.3s;
}
.step-wrap:hover { border-color: rgba(0,255,80,0.2); background: rgba(0,255,80,0.03); }
.step-num {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5em;
    font-weight: 900;
    color: rgba(0,255,100,0.25);
    min-width: 45px;
}
.step-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.82em;
    font-weight: 700;
    color: #00ff64;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.step-desc { color: rgba(255,255,255,0.45); font-size: 0.88em; line-height: 1.6; }

.disease-card { border-radius: 16px; padding: 28px; text-align: center; position: relative; overflow: hidden; }
.disease-healthy { background: rgba(0,255,100,0.06); border: 1px solid rgba(0,255,100,0.2); }
.disease-early { background: rgba(255,160,0,0.06); border: 1px solid rgba(255,160,0,0.2); }
.disease-late { background: rgba(255,60,60,0.06); border: 1px solid rgba(255,60,60,0.2); }
.disease-icon { font-size: 2.8em; margin-bottom: 12px; display: block; }
.disease-name { font-family: 'Orbitron', sans-serif; font-size: 0.82em; font-weight: 700; letter-spacing: 2px; margin-bottom: 10px; }
.disease-healthy .disease-name { color: #00ff64; }
.disease-early .disease-name { color: #ffa040; }
.disease-late .disease-name { color: #ff6060; }
.disease-desc { color: rgba(255,255,255,0.4); font-size: 0.85em; line-height: 1.6; }

.stButton > button {
    background: linear-gradient(135deg, rgba(0,200,80,0.2), rgba(0,255,100,0.1)) !important;
    border: 1px solid rgba(0,255,100,0.5) !important;
    border-radius: 12px !important;
    color: #00ff64 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.82em !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    padding: 14px 30px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(0,255,100,0.25) !important;
    box-shadow: 0 0 30px rgba(0,255,100,0.25) !important;
    border-color: #00ff64 !important;
    transform: translateY(-2px) !important;
}

.neon-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,100,0.25), transparent);
    margin: 60px 0;
}

.footer {
    text-align: center;
    padding: 30px;
    color: rgba(0,255,100,0.2);
    font-size: 0.78em;
    letter-spacing: 3px;
    font-family: 'Orbitron', sans-serif;
    border-top: 1px solid rgba(0,255,80,0.06);
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# NAVBAR
# -------------------------
st.markdown("""
<div class='navbar'>
    <div class='nav-logo'>🌱 KisanGuard AI</div>
    <div style='display:flex; gap:35px;'>
        <a href='#features' style='color:rgba(0,255,100,0.55); text-decoration:none;
            font-size:0.88em; letter-spacing:2px; text-transform:uppercase;'>Features</a>
        <a href='#how' style='color:rgba(0,255,100,0.55); text-decoration:none;
            font-size:0.88em; letter-spacing:2px; text-transform:uppercase;'>How It Works</a>
        <a href='#diseases' style='color:rgba(0,255,100,0.55); text-decoration:none;
            font-size:0.88em; letter-spacing:2px; text-transform:uppercase;'>Diseases</a>
    </div>
    <div class='nav-status'>
        <span class='dot-live'></span> AI ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# HERO SECTION
# -------------------------
st.markdown("""
<div class='hero'>
    <div class='hero-badge'>🌿 AI Powered Plant Disease Detection</div>
    <div class='hero-title'>
        <span class='hero-title-white'>Protect Your</span><br>
        <span class='hero-title-green'>Potato Harvest</span><br>
        <span class='hero-title-white'>With AI</span>
    </div>
    <div class='hero-sub'>
        Upload a photo of your potato leaf and get instant disease detection,
        damage score, and treatment plan — powered by deep learning CNN model.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# SINGLE GET STARTED BUTTON (Hero)
# -------------------------
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🚀  GET STARTED", key="hero_start"):
        if st.session_state.get("logged_in"):
            st.switch_page("pages/home.py")
        else:
            st.switch_page("pages/app.py")

# Stats
st.markdown("""
<div class='stats-row'>
    <div class='stat-item'>
        <span class='stat-num'>95%+</span>
        <div class='stat-desc'>Detection Accuracy</div>
    </div>
    <div class='stat-divider'></div>
    <div class='stat-item'>
        <span class='stat-num'>3</span>
        <div class='stat-desc'>Disease Classes</div>
    </div>
    <div class='stat-divider'></div>
    <div class='stat-item'>
        <span class='stat-num'>&lt;2s</span>
        <div class='stat-desc'>Analysis Time</div>
    </div>
    <div class='stat-divider'></div>
    <div class='stat-item'>
        <span class='stat-num'>CNN</span>
        <div class='stat-desc'>Deep Learning Model</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# FEATURES SECTION
# -------------------------
st.markdown("""
<div id='features'>
    <div class='section-title'>CORE FEATURES</div>
    <div class='section-sub'>EVERYTHING YOU NEED TO PROTECT YOUR CROP</div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4, gap="medium")
with f1:
    st.markdown("""<div class='feature-card'>
        <span class='feature-icon'>🔬</span>
        <div class='feature-title'>INSTANT DETECTION</div>
        <div class='feature-desc'>Upload leaf photo and get disease result in under 2 seconds using CNN deep learning model.</div>
    </div>""", unsafe_allow_html=True)
with f2:
    st.markdown("""<div class='feature-card'>
        <span class='feature-icon'>🍂</span>
        <div class='feature-title'>DAMAGE SCORE</div>
        <div class='feature-desc'>Know exactly how much your leaf is damaged — from 0% healthy to 95% critical stage.</div>
    </div>""", unsafe_allow_html=True)
with f3:
    st.markdown("""<div class='feature-card'>
        <span class='feature-icon'>💊</span>
        <div class='feature-title'>TREATMENT PLAN</div>
        <div class='feature-desc'>Get specific fungicide names, dosage, and step-by-step treatment protocol instantly.</div>
    </div>""", unsafe_allow_html=True)
with f4:
    st.markdown("""<div class='feature-card'>
        <span class='feature-icon'>🤖</span>
        <div class='feature-title'>KISAN AI CHAT</div>
        <div class='feature-desc'>Ask farming questions anytime — disease control, fertilizers, irrigation, pest control.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# HOW IT WORKS
# -------------------------
st.markdown("""
<div id='how'>
    <div class='section-title'>HOW IT WORKS</div>
    <div class='section-sub'>3 SIMPLE STEPS TO PROTECT YOUR CROP</div>
</div>
""", unsafe_allow_html=True)

hw1, hw2 = st.columns([1, 1], gap="large")
with hw1:
    st.markdown("""
    <div class='step-wrap'>
        <div class='step-num'>01</div>
        <div>
            <div class='step-title'>CREATE ACCOUNT & LOGIN</div>
            <div class='step-desc'>Register with a simple username and password. Your scan history is saved securely for future reference.</div>
        </div>
    </div>
    <div class='step-wrap'>
        <div class='step-num'>02</div>
        <div>
            <div class='step-title'>UPLOAD LEAF PHOTO</div>
            <div class='step-desc'>Take a clear photo of your potato leaf and upload it. Supports JPG, PNG, and JPEG formats.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with hw2:
    st.markdown("""
    <div class='step-wrap'>
        <div class='step-num'>03</div>
        <div>
            <div class='step-title'>GET AI ANALYSIS</div>
            <div class='step-desc'>Our CNN model instantly analyzes the image and detects whether the leaf is Healthy, Early Blight, or Late Blight.</div>
        </div>
    </div>
    <div class='step-wrap'>
        <div class='step-num'>04</div>
        <div>
            <div class='step-title'>FOLLOW TREATMENT PLAN</div>
            <div class='step-desc'>Get detailed treatment protocol with specific fungicide names, dosage, and farming tips to save your crop.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# DISEASE CLASSES
# -------------------------
st.markdown("""
<div id='diseases'>
    <div class='section-title'>DETECTABLE DISEASES</div>
    <div class='section-sub'>OUR MODEL IDENTIFIES 3 CLASSES</div>
</div>
""", unsafe_allow_html=True)

d1, d2, d3 = st.columns(3, gap="medium")
with d1:
    st.markdown("""<div class='disease-card disease-healthy'>
        <span class='disease-icon'>✅</span>
        <div class='disease-name'>POTATO HEALTHY</div>
        <div class='disease-desc'>Plant is in perfect condition. No disease detected. Damage Score: 0%. Continue regular maintenance.</div>
    </div>""", unsafe_allow_html=True)
with d2:
    st.markdown("""<div class='disease-card disease-early'>
        <span class='disease-icon'>⚠️</span>
        <div class='disease-name'>EARLY BLIGHT</div>
        <div class='disease-desc'>Caused by Alternaria solani. Brown spots on leaves. Damage Score: 20-60%. Treatable with Mancozeb fungicide.</div>
    </div>""", unsafe_allow_html=True)
with d3:
    st.markdown("""<div class='disease-card disease-late'>
        <span class='disease-icon'>🔴</span>
        <div class='disease-name'>LATE BLIGHT</div>
        <div class='disease-desc'>Caused by Phytophthora infestans. Very dangerous. Damage Score: 50-95%. Requires urgent Metalaxyl treatment.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# SAMPLE IMAGES SECTION
# -------------------------
st.markdown("""
<div class='section-title'>SAMPLE LEAF IMAGES</div>
<div class='section-sub'>EXAMPLES OF WHAT TO UPLOAD FOR BEST RESULTS</div>
""", unsafe_allow_html=True)

si1, si2, si3 = st.columns(3, gap="medium")
with si1:
    st.markdown("""<div class='disease-card disease-healthy' style='margin-bottom:12px;'>
        <span class='disease-icon'>🌿</span>
        <div class='disease-name'>HEALTHY LEAF</div>
        <div class='disease-desc' style='margin-top:10px;'>
            Full green color, No spots or marks, Smooth texture, Clear veins visible.<br><br>
            <span style='color:rgba(0,255,100,0.5); font-size:0.85em;'>Upload: Clear top-view photo in good lighting</span>
        </div>
    </div>""", unsafe_allow_html=True)
with si2:
    st.markdown("""<div class='disease-card disease-early' style='margin-bottom:12px;'>
        <span class='disease-icon'>🟤</span>
        <div class='disease-name'>EARLY BLIGHT LEAF</div>
        <div class='disease-desc' style='margin-top:10px;'>
            Dark brown circular spots, Yellow ring around spots, Concentric ring pattern.<br><br>
            <span style='color:rgba(255,160,0,0.6); font-size:0.85em;'>Upload: Show the spotted area clearly</span>
        </div>
    </div>""", unsafe_allow_html=True)
with si3:
    st.markdown("""<div class='disease-card disease-late' style='margin-bottom:12px;'>
        <span class='disease-icon'>⚫</span>
        <div class='disease-name'>LATE BLIGHT LEAF</div>
        <div class='disease-desc' style='margin-top:10px;'>
            Large dark/black patches, Water-soaked appearance, Rapid spreading lesions.<br><br>
            <span style='color:rgba(255,60,60,0.6); font-size:0.85em;'>Upload: Capture full leaf with patches visible</span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-top:15px; padding:15px;
    background:rgba(0,255,80,0.03); border:1px solid rgba(0,255,80,0.08);
    border-radius:12px; color:rgba(255,255,255,0.4); font-size:0.85em;'>
    💡 <b style='color:rgba(0,255,100,0.6);'>TIP:</b>
    Natural daylight • Keep leaf flat • Avoid blurry images • JPG, PNG, JPEG supported
</div>""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# TECH STACK
# -------------------------
st.markdown("""
<div class='section-title'>TECHNOLOGY STACK</div>
<div class='section-sub'>BUILT WITH POWERFUL MODERN TECHNOLOGIES</div>
""", unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.columns(5, gap="medium")
techs = [
    ("🐍", "PYTHON", "Core programming language for backend and model integration"),
    ("🧠", "TENSORFLOW", "Deep learning framework to build and train CNN model"),
    ("🌐", "STREAMLIT", "Web framework for interactive UI and multi-page app"),
    ("🗄️", "SQLITE", "Lightweight database for users and scan history"),
    ("📷", "CNN MODEL", "Convolutional Neural Network trained on PlantVillage dataset"),
]
for col, (icon, name, desc) in zip([t1, t2, t3, t4, t5], techs):
    with col:
        st.markdown(f"""
        <div style='background:rgba(5,20,10,0.7); border:1px solid rgba(0,255,80,0.1);
            border-radius:16px; padding:22px 12px; text-align:center;'>
            <div style='font-size:2em; margin-bottom:10px;'>{icon}</div>
            <div style='font-family:Orbitron,sans-serif; font-size:0.72em; font-weight:700;
                color:#00ff64; letter-spacing:2px; margin-bottom:8px;'>{name}</div>
            <div style='color:rgba(255,255,255,0.35); font-size:0.78em; line-height:1.5;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# FAQ
# -------------------------
st.markdown("""
<div class='section-title'>FREQUENTLY ASKED QUESTIONS</div>
<div class='section-sub'>EVERYTHING YOU NEED TO KNOW</div>
""", unsafe_allow_html=True)

faqs = [
    ("❓", "Kaunsi image upload karni chahiye?", "Potato leaf ki clear, well-lit photo upload karein. Natural daylight me li hui photo best results deti hai. JPG, PNG, JPEG formats supported hain."),
    ("🎯", "Model kitna accurate hai?", "Hamara CNN model 95%+ accuracy ke saath diseases detect karta hai. Model ko PlantVillage dataset pe train kiya gaya hai."),
    ("💰", "Kya yeh system free hai?", "Haan, PotatoGuard AI bilkul free hai! Account banao, login karo aur unlimited scans karo. Koi payment nahi."),
    ("⏱️", "Ek scan me kitna time lagta hai?", "Sirf 1-2 seconds me result aa jaata hai. CNN model real-time me leaf analyze karta hai."),
    ("📱", "Kya mobile pe kaam karta hai?", "Haan! Browser-based hai — mobile, tablet, computer sab pe kaam karta hai. Koi app download nahi chahiye."),
    ("🔒", "Kya mera data safe hai?", "Haan! Password SHA-256 hashing se encrypted hai. Scan history sirf aapke account me save hoti hai."),
]
faq1, faq2 = st.columns(2, gap="large")
for i, (icon, question, answer) in enumerate(faqs):
    col = faq1 if i % 2 == 0 else faq2
    with col:
        st.markdown(f"""
        <div style='background:rgba(5,20,10,0.6); border:1px solid rgba(0,255,80,0.08);
            border-radius:14px; padding:20px; margin-bottom:14px;'>
            <div style='display:flex; gap:12px;'>
                <span style='font-size:1.3em;'>{icon}</span>
                <div>
                    <div style='font-family:Orbitron,sans-serif; font-size:0.76em; font-weight:700;
                        color:#00ff64; letter-spacing:1px; margin-bottom:7px;'>{question}</div>
                    <div style='color:rgba(255,255,255,0.45); font-size:0.87em; line-height:1.7;'>{answer}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# LANGUAGE TOGGLE
# -------------------------
st.markdown("""
<div class='section-title'>LANGUAGE / BHASHA</div>
<div class='section-sub'>SELECT YOUR PREFERRED LANGUAGE</div>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "English"
lc1, lc2, lc3, lc4 = st.columns([2, 1, 1, 2])
with lc2:
    if st.button("🇬🇧  ENGLISH", key="lang_en"):
        st.session_state.lang = "English"
with lc3:
    if st.button("🇮🇳  HINDI", key="lang_hi"):
        st.session_state.lang = "Hindi"

if st.session_state.lang == "Hindi":
    st.markdown("""
    <div style='background:rgba(0,255,80,0.04); border:1px solid rgba(0,255,80,0.12);
        border-radius:16px; padding:28px; margin-top:18px; text-align:center;'>
        <div style='font-family:Orbitron,sans-serif; font-size:0.88em; color:#00ff64;
            letter-spacing:3px; margin-bottom:14px;'>HINDI MODE — हिंदी</div>
        <div style='color:rgba(255,255,255,0.5); font-size:1.05em; line-height:1.9;'>
            PotatoGuard AI किसानों को आलू की पत्ती की बीमारी तुरंत पहचानने में मदद करता है।<br>
            पत्ती की फोटो अपलोड करें → बीमारी का रिजल्ट पाएं → इलाज करें।<br>
            तेज़ • सटीक • मुफ़्त • 24/7 उपलब्ध
        </div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='background:rgba(0,255,80,0.04); border:1px solid rgba(0,255,80,0.12);
        border-radius:16px; padding:28px; margin-top:18px; text-align:center;'>
        <div style='font-family:Orbitron,sans-serif; font-size:0.88em; color:#00ff64;
            letter-spacing:3px; margin-bottom:14px;'>ENGLISH MODE ACTIVE</div>
        <div style='color:rgba(255,255,255,0.5); font-size:1em; line-height:1.8;'>
            PotatoGuard AI helps farmers detect potato leaf diseases instantly.<br>
            Upload a leaf photo → Get disease result → Follow treatment plan.<br>
            Fast • Accurate • Free • Available 24/7
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

# -------------------------
# ABOUT PROJECT
# -------------------------
st.markdown("""
<div class='section-title'>ABOUT THE PROJECT</div>
<div class='section-sub'>PROJECT DETAILS AND INFORMATION</div>
""", unsafe_allow_html=True)

ab1, ab2 = st.columns(2, gap="large")
with ab1:
    st.markdown("""
    <div style='background:rgba(5,20,10,0.7); border:1px solid rgba(0,255,80,0.1);
        border-radius:18px; padding:28px;'>
        <div style='font-family:Orbitron,sans-serif; font-size:0.82em; font-weight:700;
            color:#00ff64; letter-spacing:3px; margin-bottom:18px;'>// ABOUT PROJECT</div>
        <div style='color:rgba(255,255,255,0.55); font-size:0.93em; line-height:1.9;'>
            PotatoGuard AI is a <b style='color:rgba(0,255,100,0.8);'>final year project</b>
            developed to help Indian farmers detect potato diseases early using AI and Deep Learning.<br><br>
            The system uses a <b style='color:rgba(0,255,100,0.8);'>CNN model</b> trained on PlantVillage
            dataset to classify potato leaves into 3 categories with 95%+ accuracy.<br><br>
            Built with <b style='color:rgba(0,255,100,0.8);'>Python, TensorFlow, and Streamlit</b>
            — accessible from any device without installation.
        </div>
    </div>""", unsafe_allow_html=True)
with ab2:
    st.markdown("""
    <div style='background:rgba(5,20,10,0.7); border:1px solid rgba(0,255,80,0.1);
        border-radius:18px; padding:28px;'>
        <div style='font-family:Orbitron,sans-serif; font-size:0.82em; font-weight:700;
            color:#00ff64; letter-spacing:3px; margin-bottom:18px;'>// PROJECT DETAILS</div>
        <div style='display:flex; justify-content:space-between; padding:11px 0; border-bottom:1px solid rgba(0,255,80,0.06);'>
            <span style='color:rgba(0,255,100,0.5); font-size:0.83em;'>PROJECT NAME</span>
            <span style='color:rgba(255,255,255,0.7); font-size:0.85em;'>PotatoGuard AI</span>
        </div>
        <div style='display:flex; justify-content:space-between; padding:11px 0; border-bottom:1px solid rgba(0,255,80,0.06);'>
            <span style='color:rgba(0,255,100,0.5); font-size:0.83em;'>TECHNOLOGY</span>
            <span style='color:rgba(255,255,255,0.7); font-size:0.85em;'>CNN / Deep Learning</span>
        </div>
        <div style='display:flex; justify-content:space-between; padding:11px 0; border-bottom:1px solid rgba(0,255,80,0.06);'>
            <span style='color:rgba(0,255,100,0.5); font-size:0.83em;'>FRAMEWORK</span>
            <span style='color:rgba(255,255,255,0.7); font-size:0.85em;'>TensorFlow + Streamlit</span>
        </div>
        <div style='display:flex; justify-content:space-between; padding:11px 0; border-bottom:1px solid rgba(0,255,80,0.06);'>
            <span style='color:rgba(0,255,100,0.5); font-size:0.83em;'>DATASET</span>
            <span style='color:rgba(255,255,255,0.7); font-size:0.85em;'>PlantVillage Dataset</span>
        </div>
        <div style='display:flex; justify-content:space-between; padding:11px 0; border-bottom:1px solid rgba(0,255,80,0.06);'>
            <span style='color:rgba(0,255,100,0.5); font-size:0.83em;'>ACCURACY</span>
            <span style='color:#00ff64; font-size:0.88em; font-weight:700;'>95%+</span>
        </div>
        <div style='display:flex; justify-content:space-between; padding:11px 0;'>
            <span style='color:rgba(0,255,100,0.5); font-size:0.83em;'>YEAR</span>
            <span style='color:rgba(255,255,255,0.7); font-size:0.85em;'>2025 - 2026</span>
        </div>
    </div>""", unsafe_allow_html=True)

# -------------------------
# FINAL CTA (no button — already at top)
# -------------------------
st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding:60px 20px;
    background:rgba(0,255,80,0.03); border-top:1px solid rgba(0,255,80,0.08);
    border-bottom:1px solid rgba(0,255,80,0.08); margin-bottom:30px;'>
    <div style='font-family:Orbitron,sans-serif; font-size:1.8em; font-weight:900;
        color:white; letter-spacing:3px; margin-bottom:12px;'>READY TO PROTECT YOUR CROP?</div>
    <div style='color:rgba(255,255,255,0.4); font-size:1em; letter-spacing:1px;'>
        Scroll up and click GET STARTED to begin your AI analysis
    </div>
</div>
""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style='text-align:center; padding:28px; color:rgba(0,255,100,0.2); font-size:0.76em;
    letter-spacing:3px; font-family:Orbitron,sans-serif; border-top:1px solid rgba(0,255,80,0.06);'>
    POTATOGUARD AI &nbsp;©&nbsp; 2026 &nbsp;|&nbsp; CNN MODEL v2.1 &nbsp;|&nbsp;
    DEEP LEARNING &nbsp;|&nbsp; BUILT FOR FARMERS &nbsp;|&nbsp; INDIA
</div>
""", unsafe_allow_html=True)
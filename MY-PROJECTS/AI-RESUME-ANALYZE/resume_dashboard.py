# ================= Advanced & Polished Streamlit Resume Analyzer =================

import streamlit as st
import joblib
import re
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ================= Load Model & Vectorizer =================
model = joblib.load("ats_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# ================= Skills List =================
skills = [
    'recruitment', 'talent acquisition', 'employee relations', 'hr', 'training',
    'payroll', 'performance management', 'ms excel', 'communication',
    'leadership', 'team management', 'project management', 'hiring',
    'onboarding', 'benefits', 'employee engagement', 'analytics',
    'hr policies', 'labor laws'
]

# ================= Helper Functions =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z ]', ' ', text)
    return text

def extract_skills(text):
    return [skill for skill in skills if skill in text]

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def generate_suggestions(score, matched_skills):
    suggestions = []
    missing_skills = list(set(skills) - set(matched_skills))

    if score < 40:
        suggestions.append("❌ **Resume needs major improvement**")
        suggestions.append("Add a clear professional summary")
        suggestions.append("Mention tools and technologies explicitly")
    elif score < 70:
        suggestions.append("⚠️ **Resume is average, improvements needed**")
        suggestions.append("Improve skill keywords and project descriptions")
    else:
        suggestions.append("✅ Resume is strong")

    if missing_skills:
        suggestions.append("📌 Consider adding these skills: " + ", ".join(missing_skills[:5]))

    suggestions.append("Use action verbs (developed, implemented, analyzed)")
    suggestions.append("Keep resume ATS-friendly (simple format, no tables)")
    return suggestions, missing_skills

def resume_structure_guide(score):
    structure = []
    if score < 70:
        structure.append("📌 Recommended ATS-Friendly Resume Structure:")
        structure.append("1️⃣ Header: Name | Phone | Email | LinkedIn | Location")
        structure.append("2️⃣ Professional Summary: 2–3 lines highlighting experience & skills")
        structure.append("3️⃣ Key Skills: Bullet points of technical & soft skills")
        structure.append("4️⃣ Experience / Internship: Company | Role | Duration | Achievements")
        structure.append("5️⃣ Projects: Project name | Tools | Impact")
        structure.append("6️⃣ Education: Degree | University | Year")
        structure.append("7️⃣ Certifications (Optional)")
        structure.append("⚠️ Avoid tables, graphics, columns & images")
    else:
        structure.append("✅ Your resume structure is already ATS-friendly")
    return structure

def generate_professional_summary(score, skills):
    if not skills:
        return "Motivated professional seeking opportunities to grow and contribute effectively."
    skill_text = ", ".join(skills[:5])
    if score >= 70:
        return f"Results-driven professional with strong experience in {skill_text}. Proven ability to deliver high-quality outcomes."
    elif score >= 40:
        return f"Dedicated professional with hands-on experience in {skill_text}. Seeking opportunities to enhance skills and grow."
    else:
        return f"Entry-level candidate with foundational knowledge in {skill_text}. Eager to learn and contribute."

def generate_pdf(score, skills, summary, suggestions, structure):
    file_path = "resume_improvement_report.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "AI Resume Improvement Report")
    c.setFont("Helvetica", 11)
    y -= 30
    c.drawString(40, y, f"ATS Score: {round(score,2)} / 100")
    y -= 20
    c.drawString(40, y, "Professional Summary:")
    y -= 15
    c.drawString(40, y, summary[:100])
    y -= 30
    c.drawString(40, y, "Matched Skills:")
    y -= 15
    c.drawString(40, y, ", ".join(skills))
    y -= 30
    c.drawString(40, y, "Improvement Suggestions:")
    for s in suggestions:
        y -= 15
        c.drawString(50, y, f"- {s}")
    y -= 20
    c.drawString(40, y, "Recommended Resume Structure:")
    for s in structure:
        y -= 15
        c.drawString(50, y, s)
    c.save()
    return file_path

# ================= Streamlit UI =================
st.set_page_config(page_title="AI Resume ATS Analyzer", layout="wide")

st.title("📄 AI Resume ATS Score Analyzer")
st.write("Upload your resume to predict ATS score, skills, structure suggestions, and improvement report")

# ---------- Tabs ----------
tabs = st.tabs(["Resume Upload", "Job Description Match", "Download Report"])

# ---------- Tab 1: Resume Upload ----------
with tabs[0]:
    uploaded_file = st.file_uploader("📤 Upload Resume (PDF only)", type=["pdf"])
    if uploaded_file:
        resume_text = read_pdf(uploaded_file)
        cleaned_resume = clean_text(resume_text)

        resume_vec = vectorizer.transform([cleaned_resume])
        predicted_score = model.predict(resume_vec)[0]
        matched_skills = extract_skills(cleaned_resume)

        # ----- ATS Score with Progress Bar -----
        st.subheader("📊 ATS Score")
        if predicted_score >= 70:
            st.progress(100)
            st.success(f"{round(predicted_score,2)} / 100 💪 Strong Resume")
        elif predicted_score >= 40:
            st.progress(int(predicted_score))
            st.warning(f"{round(predicted_score,2)} / 100 ⚠️ Average Resume")
        else:
            st.progress(int(predicted_score))
            st.error(f"{round(predicted_score,2)} / 100 ❌ Needs Improvement")

        # ----- Matched & Missing Skills -----
        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"<span style='color:green'>• {skill}</span>", unsafe_allow_html=True)
        else:
            st.warning("No matching skills found")

        st.subheader("⚠️ Missing Skills")
        suggestions, missing_skills = generate_suggestions(predicted_score, matched_skills)
        if missing_skills:
            for skill in missing_skills[:5]:
                st.markdown(f"<span style='color:red'>• {skill}</span>", unsafe_allow_html=True)

        # ----- Suggestions & Structure -----
        st.subheader("📝 Resume Improvement Suggestions")
        with st.expander("View Suggestions"):
            for tip in suggestions:
                st.write("•", tip)

        st.subheader("📑 Recommended Resume Structure")
        structure_tips = resume_structure_guide(predicted_score)
        with st.expander("View Resume Structure"):
            for tip in structure_tips:
                st.write(tip)

        # ----- Professional Summary -----
        st.subheader("✍️ Auto-Generated Professional Summary")
        summary = generate_professional_summary(predicted_score, matched_skills)
        st.info(summary)

# ---------- Tab 2: Job Description Match ----------
with tabs[1]:
    job_desc = st.text_area("📌 Paste Job Description here")
    if uploaded_file and job_desc:
        cleaned_jd = clean_text(job_desc)
        jd_vec = vectorizer.transform([cleaned_jd])
        similarity = cosine_similarity(resume_vec, jd_vec)[0][0] * 100

        st.write(f"🔗 Resume–JD Match Score: {round(similarity,2)}%")
        if similarity >= 70:
            st.success("Excellent match 🎯")
        elif similarity >= 40:
            st.warning("Average match ⚠️")
        else:
            st.error("Low match ❌")

# ---------- Tab 3: Download PDF ----------
with tabs[2]:
    if uploaded_file:
        st.subheader("⬇️ Download Resume Improvement Report")
        if st.button("Generate & Download PDF"):
            pdf_file = generate_pdf(predicted_score, matched_skills, summary, suggestions, structure_tips)
            with open(pdf_file, "rb") as f:
                st.download_button("Click to Download PDF", f, file_name=pdf_file)
            st.success("PDF Report generated successfully!")

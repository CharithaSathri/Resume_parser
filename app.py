import streamlit as st
import fitz  # PyMuPDF
import re

# --- Skill keywords list ---
skill_keywords = [
    'Python', 'Java', 'C++', 'C', 'Machine Learning', 'Deep Learning',
    'Data Science', 'NLP', 'SQL', 'Tableau', 'Pandas', 'NumPy', 'React',
    'Django', 'Flask', 'Excel', 'Power BI', 'TensorFlow', 'Keras'
]

# --- Function to extract text from PDF ---
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# --- Extraction functions ---
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group() if match else ""

def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,15}", text)
    return match.group() if match else ""

def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        if line.strip():
            return line.strip()
    return ""

def extract_skills(text):
    found_skills = []
    for skill in skill_keywords:
        if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return ', '.join(found_skills)

# --- Streamlit App UI ---
st.title("📄 Resume Parser")
uploaded_file = st.file_uploader("Upload a PDF Resume", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    st.subheader("📑 Extracted Details")
    st.markdown(f"**Name:** {name}")
    st.markdown(f"**Email:** {email}")
    st.markdown(f"**Phone:** {phone}")
    st.markdown(f"**Skills:** {skills if skills else 'Not detected'}")

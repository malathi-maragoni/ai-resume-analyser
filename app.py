import streamlit as st
import spacy
import pandas as pd
from utils.parser import extract_text_from_docx

# Load NLP model
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

st.title("📄 AI Resume Analyser")

uploaded_file = st.file_uploader("Upload your resume (.docx)", type=["docx"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_resume.docx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text
    resume_text = extract_text_from_docx("temp_resume.docx")
    st.subheader("Extracted Resume Text")
    st.text(resume_text)

    # NLP analysis
    doc = nlp(resume_text)

    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    df = pd.DataFrame(entities, columns=["Entity", "Label"])
    st.subheader("Named Entities Found")
    st.dataframe(df)

    # Simple keyword check
    keywords = ["Python", "Java", "Machine Learning", "SQL", "Communication"]
    found = [kw for kw in keywords if kw.lower() in resume_text.lower()]
    st.subheader("Matched Keywords")
    st.write(found if found else "No keywords found.")

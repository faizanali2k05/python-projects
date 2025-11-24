import streamlit as st
import pdfplumber
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load BERT Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------------
# FUNCTION TO EXTRACT TEXT FROM PDF
# ------------------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# ------------------------------------
# STREAMLIT GUI
# ------------------------------------
st.set_page_config(page_title="AI Resume Screening System", layout="wide")

st.title("📄 Intelligent Resume Screening System (AI Based)")
st.write("Upload resumes + job description → get ranked candidates using BERT similarity.")

# Upload job description
job_description = st.text_area("📝 Paste Job Description Here", height=200)

# Upload resumes
uploaded_files = st.file_uploader("📂 Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

if st.button("🔍 Start Screening"):

    if not job_description:
        st.warning("Please paste a job description!")
    elif not uploaded_files:
        st.warning("Please upload at least one resume!")
    else:
        st.success("Processing resumes... Please wait.")

        # Convert job description into vector
        job_vector = model.encode(job_description, convert_to_tensor=True)

        results = []

        for file in uploaded_files:
            resume_text = extract_text_from_pdf(file)

            resume_vector = model.encode(resume_text, convert_to_tensor=True)
            similarity = util.cos_sim(job_vector, resume_vector).item()

            results.append({
                "Candidate": file.name,
                "Similarity Score": round(similarity, 4)
            })

        # Convert results to DataFrame
        df = pd.DataFrame(results)
        df = df.sort_values(by="Similarity Score", ascending=False)

        st.subheader("📊 Ranked Candidates")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download Results as CSV",
            data=csv,
            file_name="ranked_resumes.csv",
            mime="text/csv"
        )

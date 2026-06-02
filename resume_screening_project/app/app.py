"""
app.py - Streamlit Dashboard
AI-powered Resume Screening System — main web interface.
Run with: streamlit run app/app.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from src.parser import parse_resume_bytes
from src.preprocessing import preprocess
from src.skill_extractor import extract_skills, skill_frequency
from src.matcher import tfidf_similarity, semantic_similarity, combined_similarity
from src.ranking import rank_candidates, export_to_csv
from src.utils import ensure_dir, timestamp_filename

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "reports")
ensure_dir(OUTPUTS_DIR)

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

ACCENT = "#4F8EF7"
BG_CARD = "#1E1E2F"

st.markdown("""
<style>
    body { font-family: 'Segoe UI', sans-serif; }
    .main { background-color: #0F0F1A; }
    .block-container { padding: 2rem 2.5rem; }
    h1 { color: #4F8EF7; font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { color: #D0D0FF; }
    .metric-card {
        background: #1E1E2F;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid #4F8EF7;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background: #4F8EF7;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: background 0.2s;
    }
    .stButton > button:hover { background: #3a6fd8; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    .sidebar .sidebar-content { background: #111122; }
</style>
""", unsafe_allow_html=True)


def sidebar():
    st.sidebar.image(
        "https://img.icons8.com/fluency/96/resume.png",
        width=70,
    )
    st.sidebar.title("AI Resume Screener")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📤 Upload & Screen", "📊 Analytics", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Built with Python · Streamlit · spaCy · scikit-learn")
    return page


def home_page():
    st.title("📄 AI-Powered Resume Screening System")
    st.markdown(
        "Automatically rank candidates by relevance to a job description using "
        "**TF-IDF**, **Cosine Similarity**, and **Semantic Matching**."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matching Algorithms", "3")
    col2.metric("Skill Database", "50+")
    col3.metric("Export Formats", "CSV")
    col4.metric("PDF Parsing", "✓ pdfplumber")

    st.markdown("---")
    st.subheader("How It Works")
    steps = [
        ("1️⃣", "Upload PDFs", "Upload one or more PDF resumes."),
        ("2️⃣", "Add JD", "Paste or type the job description."),
        ("3️⃣", "Screen", "Click **Run Screening** to analyse."),
        ("4️⃣", "Export", "Download the ranked CSV report."),
    ]
    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, steps):
        col.markdown(f"### {icon} {title}\n{desc}")


def upload_and_screen_page():
    st.title("📤 Upload & Screen")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("1 · Upload Resumes")
        uploaded_files = st.file_uploader(
            "Select PDF resumes (multiple allowed)",
            type=["pdf"],
            accept_multiple_files=True,
        )

        st.subheader("2 · Job Description")
        jd_source = st.radio("Source", ["Paste text", "Upload file"], horizontal=True)

        jd_text = ""
        if jd_source == "Paste text":
            jd_text = st.text_area(
                "Paste the job description here",
                height=250,
                placeholder="We are looking for a Python developer with experience in machine learning, SQL, and AWS...",
            )
        else:
            jd_file = st.file_uploader("Upload JD (.txt or .pdf)", type=["txt", "pdf"])
            if jd_file:
                if jd_file.name.endswith(".pdf"):
                    jd_text = parse_resume_bytes(jd_file.read(), jd_file.name)
                else:
                    jd_text = jd_file.read().decode("utf-8", errors="ignore")

        st.subheader("3 · Matching Settings")
        method = st.selectbox(
            "Similarity Method",
            ["TF-IDF Only", "Semantic Only", "Combined (TF-IDF + Semantic)"],
        )
        if method == "Combined (TF-IDF + Semantic)":
            tfidf_w = st.slider("TF-IDF Weight", 0.0, 1.0, 0.5, 0.05)
            sem_w = round(1.0 - tfidf_w, 2)
            st.caption(f"Semantic weight: {sem_w}")
        else:
            tfidf_w, sem_w = 0.5, 0.5

        run_btn = st.button("🚀 Run Screening", use_container_width=True)

    with col_right:
        st.subheader("Results")

        if run_btn:
            if not uploaded_files:
                st.error("Please upload at least one resume PDF.")
                return
            if not jd_text.strip():
                st.error("Please provide a job description.")
                return

            with st.spinner("Parsing resumes…"):
                raw_texts = {}
                for f in uploaded_files:
                    text = parse_resume_bytes(f.read(), f.name)
                    if text:
                        raw_texts[f.name] = text
                    else:
                        st.warning(f"⚠️ Could not extract text from **{f.name}**.")

            if not raw_texts:
                st.error("No readable resumes found.")
                return

            with st.spinner("Preprocessing…"):
                processed_texts = {n: preprocess(t) for n, t in raw_texts.items()}
                processed_jd = preprocess(jd_text)

            with st.spinner("Computing similarity…"):
                if method == "TF-IDF Only":
                    scores = tfidf_similarity(processed_texts, processed_jd)
                elif method == "Semantic Only":
                    scores = semantic_similarity(raw_texts, jd_text)
                    if not scores:
                        st.warning("sentence-transformers not available. Falling back to TF-IDF.")
                        scores = tfidf_similarity(processed_texts, processed_jd)
                else:
                    scores = combined_similarity(
                        processed_texts, processed_jd, tfidf_w, sem_w
                    )

            df = rank_candidates(scores, raw_texts, jd_text)
            st.session_state["ranked_df"] = df
            st.session_state["raw_texts"] = raw_texts
            st.session_state["jd_text"] = jd_text

            st.success(f"✅ Screened **{len(df)}** candidates!")

            display_cols = ["Candidate", "Score (%)", "Matched Skills", "Missing Skills"]
            st.dataframe(
                df[display_cols],
                use_container_width=True,
                height=400,
            )

            csv_name = timestamp_filename("ranked_candidates")
            csv_path = os.path.join(OUTPUTS_DIR, csv_name)
            export_to_csv(df, csv_path)

            csv_bytes = df.to_csv().encode("utf-8")
            st.download_button(
                "⬇️ Download CSV Report",
                data=csv_bytes,
                file_name=csv_name,
                mime="text/csv",
                use_container_width=True,
            )

        elif "ranked_df" in st.session_state:
            df = st.session_state["ranked_df"]
            display_cols = ["Candidate", "Score (%)", "Matched Skills", "Missing Skills"]
            st.dataframe(df[display_cols], use_container_width=True, height=400)
            csv_bytes = df.to_csv().encode("utf-8")
            st.download_button(
                "⬇️ Download CSV Report",
                data=csv_bytes,
                file_name="ranked_candidates.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("Upload resumes and a job description, then click **Run Screening**.")


def analytics_page():
    st.title("📊 Analytics")

    if "ranked_df" not in st.session_state:
        st.info("Run a screening first to see analytics.")
        return

    df = st.session_state["ranked_df"]
    raw_texts = st.session_state.get("raw_texts", {})
    jd_text = st.session_state.get("jd_text", "")

    col1, col2, col3 = st.columns(3)
    col1.metric("Candidates Screened", len(df))
    col2.metric("Top Score", f"{df['Score (%)'].max():.1f}%")
    col3.metric("Avg Score", f"{df['Score (%)'].mean():.1f}%")

    st.markdown("---")

    chart_col, freq_col = st.columns(2, gap="large")

    with chart_col:
        st.subheader("Candidate Score Comparison")
        fig, ax = plt.subplots(figsize=(7, max(3, len(df) * 0.5)))
        colors = ["#4F8EF7" if i == 0 else "#7B9FF9" for i in range(len(df))]
        bars = ax.barh(df["Candidate"][::-1], df["Score (%)"][::-1], color=colors[::-1])
        ax.set_xlabel("Score (%)", color="white")
        ax.set_xlim(0, 100)
        ax.tick_params(colors="white")
        ax.set_facecolor("#1E1E2F")
        fig.patch.set_facecolor("#0F0F1A")
        for bar, val in zip(bars, df["Score (%)"][::-1]):
            ax.text(
                bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", color="white", fontsize=9,
            )
        st.pyplot(fig)
        plt.close(fig)

    with freq_col:
        st.subheader("Skill Frequency Across Resumes")
        freq = skill_frequency(raw_texts)
        if freq:
            top_skills = dict(freq.most_common(15))
            fig2, ax2 = plt.subplots(figsize=(7, max(3, len(top_skills) * 0.5)))
            ax2.barh(list(top_skills.keys())[::-1], list(top_skills.values())[::-1], color="#A78BFA")
            ax2.set_xlabel("Count", color="white")
            ax2.tick_params(colors="white")
            ax2.set_facecolor("#1E1E2F")
            fig2.patch.set_facecolor("#0F0F1A")
            st.pyplot(fig2)
            plt.close(fig2)
        else:
            st.info("No skills detected in uploaded resumes.")

    st.markdown("---")
    st.subheader("Skill Match Detail")
    selected = st.selectbox("Select Candidate", df["Candidate"].tolist())
    row = df[df["Candidate"] == selected].iloc[0]
    c1, c2 = st.columns(2)
    c1.markdown(f"**✅ Matched Skills**\n\n{row['Matched Skills']}")
    c2.markdown(f"**❌ Missing Skills**\n\n{row['Missing Skills']}")


def about_page():
    st.title("ℹ️ About")
    st.markdown("""
### AI-Powered Resume Screening System

This tool automates candidate screening by comparing resumes against job descriptions using:

| Algorithm | Description |
|---|---|
| **TF-IDF + Cosine Similarity** | Measures keyword overlap between resume and JD |
| **Sentence Transformers (SBERT)** | Deep semantic similarity using transformer embeddings |
| **Combined** | Weighted blend of both methods |

### Tech Stack
- **Python 3.10** — Core language
- **Streamlit** — Web dashboard
- **pdfplumber** — PDF text extraction
- **spaCy** — NLP preprocessing & lemmatization
- **NLTK** — Stopword removal
- **scikit-learn** — TF-IDF vectorization
- **sentence-transformers** — Semantic embeddings
- **matplotlib** — Data visualizations
- **pandas** — Data manipulation

### Project Structure
```
resume_screening_project/
├── app/app.py              ← Streamlit dashboard
├── src/                    ← Core modules
│   ├── parser.py           ← PDF extraction
│   ├── preprocessing.py    ← Text cleaning
│   ├── skill_extractor.py  ← Skill detection
│   ├── matcher.py          ← Similarity scoring
│   ├── ranking.py          ← Candidate ranking
│   └── utils.py            ← Helpers
├── data/resumes/           ← Drop your PDFs here
├── outputs/reports/        ← Auto-saved CSV reports
├── main.py                 ← CLI entry point
└── requirements.txt
```
    """)


def main():
    page = sidebar()

    if page == "🏠 Home":
        home_page()
    elif page == "📤 Upload & Screen":
        upload_and_screen_page()
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "ℹ️ About":
        about_page()


if __name__ == "__main__":
    main()

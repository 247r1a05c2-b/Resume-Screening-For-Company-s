# AI-Powered Resume Screening System

Automatically rank job candidates by relevance to a job description using **TF-IDF**, **Cosine Similarity**, and **Sentence Transformers (SBERT)**.

---

## Setup (Anaconda / Conda)

### Step 1 — Create & activate a Conda environment

```bash
conda create -n resume_screen python=3.10 -y
conda activate resume_screen
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### Step 4 — Download NLTK data (auto-downloads on first run, or run manually)

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

---

## Run the Streamlit App

```bash
streamlit run app/app.py
```

Open your browser at `http://localhost:8501`

---

## Run the CLI Pipeline

```bash
python main.py --resumes data/resumes/ --jd data/job_descriptions/sample_jd.txt
```

Optional flags:
- `--output outputs/reports/` — where to save the CSV (default)
- `--top 5` — show top N candidates only

---

## Project Structure

```
resume_screening_project/
│
├── data/
│   ├── resumes/                  ← Put your PDF resumes here
│   ├── job_descriptions/         ← sample_jd.txt included
│   └── processed/                ← Auto-generated processed text
│
├── models/                       ← SBERT model cache (auto-downloaded)
├── notebooks/                    ← Jupyter notebooks (optional exploration)
│
├── src/
│   ├── parser.py                 ← PDF text extraction (pdfplumber)
│   ├── preprocessing.py          ← Text cleaning, tokenization, lemmatization
│   ├── skill_extractor.py        ← Technical skill detection
│   ├── matcher.py                ← TF-IDF & semantic similarity
│   ├── ranking.py                ← Candidate ranking + skill overlap
│   └── utils.py                  ← Shared helper functions
│
├── app/
│   └── app.py                    ← Streamlit dashboard (4-page UI)
│
├── outputs/
│   └── reports/                  ← Auto-saved CSV screening reports
│
├── requirements.txt
├── README.md
└── main.py                       ← CLI entry point
```

---

## Features

| Feature | Details |
|---|---|
| PDF Parsing | pdfplumber — handles multi-page PDFs |
| Preprocessing | Lowercase, remove punctuation, stopwords, lemmatization (spaCy) |
| Skill Extraction | 50+ technical skills detected via regex |
| TF-IDF Matching | sklearn TfidfVectorizer + cosine similarity |
| Semantic Matching | sentence-transformers `all-MiniLM-L6-v2` |
| Combined Score | Configurable weighted blend of TF-IDF + Semantic |
| Ranking | Sorted by score, with matched/missing skill breakdown |
| Visualizations | Score bar chart, skill frequency chart (matplotlib) |
| Export | Download ranked results as CSV |

---

## How to Add Resumes

1. Place PDF resumes in `data/resumes/`
2. Launch the Streamlit app **or** run `main.py`
3. Paste or upload a job description
4. Click **Run Screening**

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `spacy model not found` | Run `python -m spacy download en_core_web_sm` |
| `torch not found` | Run `pip install torch` |
| `No text extracted from PDF` | PDF may be image-based (scanned). Use OCR tools first. |
| Slow first run | SBERT model (~80MB) downloads on first use. Normal behavior. |

---

## Tech Stack

- Python 3.10, Streamlit, pandas, numpy
- scikit-learn, NLTK, spaCy
- pdfplumber, sentence-transformers, matplotlib

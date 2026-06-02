"""
create_sample_data.py
Run this script once to generate sample PDF resumes for testing.

Usage:
    python create_sample_data.py

Requires: fpdf2 (pip install fpdf2)
"""

import os
import sys

try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2 for sample PDF generation...")
    os.system(f"{sys.executable} -m pip install fpdf2 -q")
    from fpdf import FPDF


RESUMES = [
    {
        "filename": "Alice_Chen_Data_Scientist.pdf",
        "name": "Alice Chen",
        "contact": "alice.chen@email.com | linkedin.com/in/alicechen | San Francisco, CA",
        "summary": (
            "Senior Data Scientist with 6 years of experience in Python, machine learning, "
            "and NLP. Proven track record of building and deploying ML models at scale. "
            "Strong background in statistical analysis and deep learning."
        ),
        "skills": [
            "Python", "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
            "TensorFlow", "PyTorch", "scikit-learn", "pandas", "numpy",
            "SQL", "PostgreSQL", "AWS", "Docker", "Git", "Flask", "FastAPI",
            "Apache Spark", "Airflow", "Data Science",
        ],
        "experience": [
            ("Senior Data Scientist", "DataTech Inc.", "2021–Present",
             "Led ML pipeline for customer churn prediction (Python, scikit-learn, AWS). "
             "Built NLP-based document classifier reducing review time by 60%."),
            ("Data Scientist", "Analytics Co.", "2018–2021",
             "Developed recommendation engine using collaborative filtering and neural networks. "
             "Built ETL pipelines with pandas, PostgreSQL, and Airflow."),
        ],
        "education": "M.S. Computer Science — Stanford University (2018)",
    },
    {
        "filename": "Bob_Martinez_ML_Engineer.pdf",
        "name": "Bob Martinez",
        "contact": "bob.martinez@email.com | github.com/bobmartinez | Austin, TX",
        "summary": (
            "Machine Learning Engineer with 5 years specializing in deploying scalable ML systems. "
            "Expert in Python, Docker, Kubernetes, and cloud infrastructure (GCP, AWS). "
            "Passionate about MLOps and production-grade pipelines."
        ),
        "skills": [
            "Python", "Machine Learning", "Docker", "Kubernetes", "AWS", "GCP",
            "TensorFlow", "scikit-learn", "SQL", "MySQL", "Redis",
            "Git", "CI/CD", "Flask", "FastAPI", "Spark", "Data Science",
        ],
        "experience": [
            ("ML Engineer", "CloudML Systems", "2020–Present",
             "Designed MLOps platform using Kubernetes and Docker for model deployment. "
             "Reduced model serving latency by 40% with optimized inference pipelines."),
            ("Data Engineer", "TechStartup", "2019–2020",
             "Built data pipelines using Apache Spark and SQL. "
             "Managed cloud infrastructure on GCP and AWS."),
        ],
        "education": "B.S. Computer Science — University of Texas Austin (2019)",
    },
    {
        "filename": "Carol_Singh_Fullstack_Dev.pdf",
        "name": "Carol Singh",
        "contact": "carol.singh@email.com | portfolio.carolsingh.dev | Remote",
        "summary": (
            "Full-Stack Developer with 4 years experience in React, Node.js, and Python. "
            "Strong background in REST APIs, GraphQL, and SQL databases. "
            "Some exposure to machine learning and data visualization projects."
        ),
        "skills": [
            "Python", "JavaScript", "TypeScript", "React", "Node.js",
            "SQL", "MongoDB", "PostgreSQL", "Docker", "AWS",
            "HTML", "CSS", "GraphQL", "REST API", "Git", "Flask",
        ],
        "experience": [
            ("Senior Full-Stack Developer", "WebCo", "2022–Present",
             "Built customer-facing React dashboards consuming REST APIs and GraphQL endpoints. "
             "Implemented Node.js microservices deployed via Docker on AWS."),
            ("Software Developer", "StartApp", "2020–2022",
             "Developed Python Flask APIs and PostgreSQL database schemas. "
             "Created interactive data visualizations using matplotlib and D3.js."),
        ],
        "education": "B.S. Software Engineering — Georgia Tech (2020)",
    },
    {
        "filename": "David_Kim_Junior_DS.pdf",
        "name": "David Kim",
        "contact": "david.kim@email.com | Seattle, WA",
        "summary": (
            "Junior Data Scientist with 1 year of experience and a strong academic background. "
            "Proficient in Python, pandas, and basic machine learning. "
            "Eager to grow in NLP and deep learning domains."
        ),
        "skills": [
            "Python", "pandas", "numpy", "scikit-learn", "SQL",
            "matplotlib", "Git", "Jupyter", "Machine Learning",
        ],
        "experience": [
            ("Junior Data Scientist", "AnalyticsStartup", "2023–Present",
             "Built classification models using scikit-learn and pandas for customer segmentation. "
             "Created automated reports with matplotlib and Excel."),
        ],
        "education": "B.S. Statistics — University of Washington (2023)",
    },
    {
        "filename": "Eva_Williams_NLP_Specialist.pdf",
        "name": "Eva Williams",
        "contact": "eva.williams@email.com | New York, NY",
        "summary": (
            "NLP Specialist with 5 years of research and industry experience. "
            "Expert in transformer models, text classification, and information extraction. "
            "Strong Python and deep learning skills."
        ),
        "skills": [
            "Python", "NLP", "Natural Language Processing", "Deep Learning",
            "PyTorch", "TensorFlow", "scikit-learn", "SQL", "PostgreSQL",
            "AWS", "Docker", "Git", "Machine Learning", "Data Science",
            "pandas", "numpy", "Flask", "Kubernetes",
        ],
        "experience": [
            ("NLP Engineer", "LanguageAI", "2021–Present",
             "Designed BERT-based text classification system achieving 94% accuracy. "
             "Built information extraction pipelines using spaCy and transformers."),
            ("Research Scientist", "NLP Lab, NYU", "2019–2021",
             "Published 3 papers on entity recognition and semantic similarity. "
             "Implemented custom transformer fine-tuning pipelines with PyTorch."),
        ],
        "education": "Ph.D. Computational Linguistics — NYU (2021)",
    },
]


def create_pdf(resume: dict, output_dir: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    # Name
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 80)
    pdf.cell(0, 12, resume["name"], new_x="LMARGIN", new_y="NEXT")

    # Contact
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, resume["contact"], new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Divider
    pdf.set_draw_color(100, 120, 220)
    pdf.set_line_width(0.5)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(4)

    def section(title):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 30, 80)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_line_width(0.2)
        pdf.set_draw_color(200, 200, 230)
        pdf.line(18, pdf.get_y(), 192, pdf.get_y())
        pdf.ln(2)

    # Summary
    section("PROFESSIONAL SUMMARY")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 6, resume["summary"])
    pdf.ln(3)

    # Skills
    section("TECHNICAL SKILLS")
    pdf.set_font("Helvetica", "", 10)
    skills_text = " · ".join(resume["skills"])
    pdf.multi_cell(0, 6, skills_text)
    pdf.ln(3)

    # Experience
    section("WORK EXPERIENCE")
    for title, company, period, desc in resume["experience"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(20, 20, 60)
        pdf.cell(0, 7, f"{title} — {company}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, period, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(2)

    # Education
    section("EDUCATION")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, resume["education"], new_x="LMARGIN", new_y="NEXT")

    out_path = os.path.join(output_dir, resume["filename"])
    pdf.output(out_path)
    return out_path


def main():
    output_dir = os.path.join("data", "resumes")
    os.makedirs(output_dir, exist_ok=True)

    print("\n Generating sample PDF resumes...")
    print("=" * 50)

    for resume in RESUMES:
        path = create_pdf(resume, output_dir)
        print(f"  Created: {path}")

    print("=" * 50)
    print(f"\n Done! {len(RESUMES)} resumes saved to '{output_dir}/'")
    print("\nNow run:")
    print("  streamlit run app/app.py")
    print("  OR")
    print("  python main.py\n")


if __name__ == "__main__":
    main()

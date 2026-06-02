"""
skill_extractor.py - Skill Extraction Module
Identifies technical skills from resume and job description text.
"""

import re
from collections import Counter

SKILL_LIST = [
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "swift", "kotlin",
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "machine learning", "deep learning", "data science", "artificial intelligence", "nlp",
    "natural language processing", "computer vision", "data analysis", "data engineering",
    "react", "angular", "vue", "node.js", "nodejs", "django", "flask", "fastapi", "spring",
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform", "ansible",
    "git", "github", "gitlab", "ci/cd", "jenkins", "devops",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "matplotlib", "seaborn",
    "spark", "hadoop", "kafka", "airflow", "dbt",
    "html", "css", "rest api", "graphql", "microservices", "agile", "scrum",
    "linux", "bash", "excel", "tableau", "power bi",
]


def extract_skills(text: str, skill_list: list = None) -> list:
    """
    Extract skills found in the given text.

    Args:
        text: Raw or preprocessed text.
        skill_list: Custom list of skills to match against. Uses default if None.

    Returns:
        List of matched skills (lowercase, deduplicated).
    """
    if skill_list is None:
        skill_list = SKILL_LIST

    text_lower = text.lower()
    found = set()

    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)

    return sorted(found)


def skill_frequency(texts: dict, skill_list: list = None) -> Counter:
    """
    Count how often each skill appears across multiple texts.

    Args:
        texts: Dict mapping name to text.
        skill_list: Custom list of skills. Uses default if None.

    Returns:
        Counter of skill -> occurrence count.
    """
    freq = Counter()
    for _, text in texts.items():
        for skill in extract_skills(text, skill_list):
            freq[skill] += 1
    return freq


def skills_overlap(resume_text: str, jd_text: str, skill_list: list = None) -> dict:
    """
    Find matching and missing skills between a resume and a job description.

    Args:
        resume_text: Raw resume text.
        jd_text: Job description text.
        skill_list: Custom skill list. Uses default if None.

    Returns:
        Dict with keys 'matched', 'missing', 'extra'.
    """
    resume_skills = set(extract_skills(resume_text, skill_list))
    jd_skills = set(extract_skills(jd_text, skill_list))

    return {
        "matched": sorted(resume_skills & jd_skills),
        "missing": sorted(jd_skills - resume_skills),
        "extra": sorted(resume_skills - jd_skills),
    }

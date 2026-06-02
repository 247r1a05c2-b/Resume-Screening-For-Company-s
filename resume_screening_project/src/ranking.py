"""
ranking.py - Candidate Ranking Module
Ranks resumes based on similarity scores and skill matching.
"""

import pandas as pd
from src.skill_extractor import extract_skills, skills_overlap


def rank_candidates(
    similarity_scores: dict,
    resume_texts: dict,
    jd_text: str,
) -> pd.DataFrame:
    """
    Build a ranked DataFrame of candidates.

    Args:
        similarity_scores: Dict mapping resume name -> similarity score.
        resume_texts: Dict mapping resume name -> raw text (for skill extraction).
        jd_text: Job description text (for skill overlap).

    Returns:
        DataFrame sorted by score descending, with skill information.
    """
    rows = []
    for name, score in similarity_scores.items():
        raw_text = resume_texts.get(name, "")
        overlap = skills_overlap(raw_text, jd_text)

        rows.append({
            "Candidate": name.replace(".pdf", ""),
            "File": name,
            "Score (%)": round(score * 100, 2),
            "Matched Skills": ", ".join(overlap["matched"]) if overlap["matched"] else "—",
            "Missing Skills": ", ".join(overlap["missing"]) if overlap["missing"] else "—",
            "Matched Count": len(overlap["matched"]),
            "Missing Count": len(overlap["missing"]),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("Score (%)", ascending=False).reset_index(drop=True)
    df.index += 1
    df.index.name = "Rank"
    return df


def top_candidates(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return top N candidates from a ranked DataFrame."""
    return df.head(n)


def export_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Export ranked candidates DataFrame to a CSV file.

    Args:
        df: Ranked candidates DataFrame.
        output_path: File path to save the CSV.
    """
    df.to_csv(output_path)
    print(f"[Ranking] Results saved to: {output_path}")

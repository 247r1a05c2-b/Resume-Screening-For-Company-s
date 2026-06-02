"""
main.py - CLI Entry Point
Run the full pipeline from the command line without Streamlit.

Usage:
    python main.py --resumes data/resumes/ --jd data/job_descriptions/sample_jd.txt
"""

import argparse
import os
import sys

from src.parser import parse_resumes_from_folder, extract_text_from_pdf
from src.preprocessing import preprocess_batch, preprocess
from src.skill_extractor import extract_skills, skill_frequency
from src.matcher import combined_similarity
from src.ranking import rank_candidates, export_to_csv
from src.utils import load_text, timestamp_filename, ensure_dir


def parse_args():
    parser = argparse.ArgumentParser(description="AI Resume Screening System — CLI")
    parser.add_argument(
        "--resumes", default="data/resumes/",
        help="Path to folder containing PDF resumes",
    )
    parser.add_argument(
        "--jd", default="data/job_descriptions/sample_jd.txt",
        help="Path to job description text file",
    )
    parser.add_argument(
        "--output", default="outputs/reports/",
        help="Directory to save results CSV",
    )
    parser.add_argument(
        "--top", type=int, default=None,
        help="Show top N candidates only",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 60)
    print("  AI Resume Screening System")
    print("=" * 60)

    print(f"\n[1/5] Loading job description from: {args.jd}")
    if not os.path.exists(args.jd):
        print(f"  ERROR: JD file not found: {args.jd}")
        sys.exit(1)
    jd_text = load_text(args.jd)
    if not jd_text.strip():
        print("  ERROR: Job description is empty.")
        sys.exit(1)
    print(f"  JD loaded ({len(jd_text.split())} words).")

    print(f"\n[2/5] Parsing resumes from: {args.resumes}")
    raw_texts = parse_resumes_from_folder(args.resumes)
    if not raw_texts:
        print(f"  ERROR: No readable PDFs found in {args.resumes}")
        sys.exit(1)
    print(f"  Parsed {len(raw_texts)} resume(s).")

    print("\n[3/5] Preprocessing texts…")
    processed_resumes = preprocess_batch(raw_texts)
    processed_jd = preprocess(jd_text)

    print("\n[4/5] Computing similarity scores…")
    scores = combined_similarity(processed_resumes, processed_jd)

    print("\n[5/5] Ranking candidates…")
    df = rank_candidates(scores, raw_texts, jd_text)

    if args.top:
        df = df.head(args.top)

    print("\n" + "=" * 60)
    print("  RANKED CANDIDATES")
    print("=" * 60)
    print(df[["Candidate", "Score (%)", "Matched Count", "Missing Count"]].to_string())

    ensure_dir(args.output)
    csv_name = timestamp_filename("ranked_candidates")
    csv_path = os.path.join(args.output, csv_name)
    export_to_csv(df, csv_path)

    print(f"\n✅ Done! Results saved to: {csv_path}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

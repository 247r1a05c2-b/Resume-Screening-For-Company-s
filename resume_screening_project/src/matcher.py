"""
matcher.py - Resume Matching Module
Computes similarity between resumes and a job description using
TF-IDF cosine similarity and sentence-transformer semantic similarity.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer
    _SBERT_MODEL = None

    def _get_sbert():
        global _SBERT_MODEL
        if _SBERT_MODEL is None:
            _SBERT_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        return _SBERT_MODEL

    SBERT_AVAILABLE = True
except ImportError:
    SBERT_AVAILABLE = False
    print("[Matcher] sentence-transformers not available. Semantic similarity disabled.")


def tfidf_similarity(resume_texts: dict, jd_text: str) -> dict:
    """
    Compute TF-IDF cosine similarity between each resume and the job description.

    Args:
        resume_texts: Dict mapping resume name -> preprocessed text.
        jd_text: Preprocessed job description text.

    Returns:
        Dict mapping resume name -> cosine similarity score (0-1).
    """
    names = list(resume_texts.keys())
    corpus = [resume_texts[n] for n in names] + [jd_text]

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        return {name: 0.0 for name in names}

    jd_vector = tfidf_matrix[-1]
    resume_vectors = tfidf_matrix[:-1]

    scores = cosine_similarity(resume_vectors, jd_vector).flatten()
    return {names[i]: round(float(scores[i]), 4) for i in range(len(names))}


def semantic_similarity(resume_texts: dict, jd_text: str) -> dict:
    """
    Compute semantic similarity using sentence-transformers.

    Args:
        resume_texts: Dict mapping resume name -> raw or preprocessed text.
        jd_text: Job description text.

    Returns:
        Dict mapping resume name -> semantic similarity score (0-1).
        Returns empty dict if sentence-transformers is not available.
    """
    if not SBERT_AVAILABLE:
        return {}

    model = _get_sbert()
    names = list(resume_texts.keys())
    texts = [resume_texts[n] for n in names]

    resume_embeddings = model.encode(texts, convert_to_numpy=True)
    jd_embedding = model.encode([jd_text], convert_to_numpy=True)

    scores = cosine_similarity(resume_embeddings, jd_embedding).flatten()
    return {names[i]: round(float(scores[i]), 4) for i in range(len(names))}


def combined_similarity(
    resume_texts: dict,
    jd_text: str,
    tfidf_weight: float = 0.5,
    semantic_weight: float = 0.5,
) -> dict:
    """
    Compute a weighted combination of TF-IDF and semantic similarity.

    Args:
        resume_texts: Dict mapping resume name -> text.
        jd_text: Job description text.
        tfidf_weight: Weight for TF-IDF score.
        semantic_weight: Weight for semantic score.

    Returns:
        Dict mapping resume name -> combined score (0-1).
    """
    tfidf_scores = tfidf_similarity(resume_texts, jd_text)
    semantic_scores = semantic_similarity(resume_texts, jd_text)

    results = {}
    for name in resume_texts:
        t = tfidf_scores.get(name, 0.0)
        s = semantic_scores.get(name, 0.0)

        if semantic_scores:
            combined = tfidf_weight * t + semantic_weight * s
        else:
            combined = t

        results[name] = round(combined, 4)

    return results

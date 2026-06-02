"""
preprocessing.py - Text Preprocessing Module
Cleans and normalizes resume and job description text.
"""

import re
import string
import nltk
import spacy

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))

try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    NLP = None
    print("[Preprocessing] spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")


def lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def remove_punctuation(text: str) -> str:
    """Remove punctuation from text."""
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_stopwords(tokens: list) -> list:
    """Remove stopwords from a list of tokens."""
    return [t for t in tokens if t not in STOP_WORDS]


def tokenize(text: str) -> list:
    """Tokenize text into words."""
    return re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', text)


def lemmatize(tokens: list) -> list:
    """
    Lemmatize tokens using spaCy.

    Args:
        tokens: List of word strings.

    Returns:
        List of lemmatized word strings.
    """
    if NLP is None:
        return tokens
    doc = NLP(" ".join(tokens))
    return [token.lemma_ for token in doc if not token.is_space]


def preprocess(text: str, use_lemmatization: bool = True) -> str:
    """
    Full preprocessing pipeline.

    Steps:
        1. Lowercase
        2. Remove punctuation
        3. Tokenize
        4. Remove stopwords
        5. Lemmatize (optional)

    Args:
        text: Raw input text.
        use_lemmatization: Whether to apply lemmatization.

    Returns:
        Cleaned, space-joined token string.
    """
    text = lowercase(text)
    text = remove_punctuation(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    if use_lemmatization:
        tokens = lemmatize(tokens)
    return " ".join(tokens)


def preprocess_batch(texts: dict, use_lemmatization: bool = True) -> dict:
    """
    Preprocess a dictionary of {name: text} pairs.

    Args:
        texts: Dict mapping name to raw text.
        use_lemmatization: Whether to apply lemmatization.

    Returns:
        Dict mapping name to preprocessed text.
    """
    return {name: preprocess(text, use_lemmatization) for name, text in texts.items()}

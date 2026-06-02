"""
utils.py - Utility Functions
Helper functions used across the project.
"""

import os
import re
import json
from datetime import datetime


def ensure_dir(path: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def save_text(text: str, output_path: str) -> None:
    """Save a string to a text file."""
    ensure_dir(os.path.dirname(output_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[Utils] Saved text to: {output_path}")


def load_text(file_path: str) -> str:
    """Load text from a file."""
    if not os.path.exists(file_path):
        print(f"[Utils] File not found: {file_path}")
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def save_json(data: dict, output_path: str) -> None:
    """Save a dict as JSON."""
    ensure_dir(os.path.dirname(output_path))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_json(file_path: str) -> dict:
    """Load JSON from a file."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def timestamp_filename(base_name: str, extension: str = "csv") -> str:
    """
    Generate a timestamped filename.

    Example: 'results' -> 'results_20240101_120000.csv'
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{ts}.{extension}"


def clean_filename(name: str) -> str:
    """Remove unsafe characters from a filename."""
    return re.sub(r'[^\w\-_. ]', '_', name)


def word_count(text: str) -> int:
    """Return word count of a string."""
    return len(text.split())


def truncate(text: str, max_chars: int = 300) -> str:
    """Truncate text to max_chars and add ellipsis if needed."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."

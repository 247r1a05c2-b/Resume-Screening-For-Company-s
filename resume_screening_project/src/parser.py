"""
parser.py - Resume PDF Parser Module
Extracts text content from PDF resumes using pdfplumber.
"""

import os
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a string. Returns empty string on failure.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[Parser] Error reading '{pdf_path}': {e}")
    return text.strip()


def parse_resumes_from_folder(folder_path: str) -> dict:
    """
    Parse all PDF files in a folder.

    Args:
        folder_path: Path to the folder containing PDF resumes.

    Returns:
        Dictionary mapping filename -> extracted text.
    """
    results = {}
    if not os.path.exists(folder_path):
        print(f"[Parser] Folder not found: {folder_path}")
        return results

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(full_path)
            if text:
                results[filename] = text
            else:
                print(f"[Parser] No text extracted from: {filename}")
    return results


def parse_resume_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Extract text from PDF bytes (e.g., uploaded via Streamlit).

    Args:
        file_bytes: Raw bytes of the PDF file.
        filename: Name of the file (for error messages).

    Returns:
        Extracted text as a string.
    """
    import io
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[Parser] Error parsing bytes for '{filename}': {e}")
    return text.strip()

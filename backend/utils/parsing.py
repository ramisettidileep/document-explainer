"""Normalizes raw input texts into structured pages with boundary tracking."""
import re
from typing import Dict, Any, List

def clean_extracted_text(text: str) -> str:
    # Remove null bytes and non-printable control chars while preserving newlines
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    # Collapse multiple blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def parse_raw_text(raw_text: str, file_name: str = "document.txt") -> Dict[str, Any]:
    cleaned_text = clean_extracted_text(raw_text)
    if not cleaned_text:
        raise ValueError("Document contains no readable text. If this is a scanned image, OCR is required.")

    # Split on explicit form-feeds or page headers inserted by our PDF parser
    raw_pages = re.split(r'\f|--- Page \d+ ---|\n\s*\[Page \d+\]\s*\n', cleaned_text)
    pages: List[Dict[str, Any]] = []

    for idx, page_content in enumerate(raw_pages, start=1):
        clean_content = page_content.strip()
        if clean_content:
            pages.append({
                "page_number": idx,
                "text": clean_content,
                "char_count": len(clean_content)
            })

    if not pages:
        pages = [{"page_number": 1, "text": cleaned_text, "char_count": len(cleaned_text)}]

    return {
        "file_name": file_name,
        "text": cleaned_text,
        "total_pages": len(pages),
        "pages": pages,
        "metadata": {
            "total_chars": len(cleaned_text),
            "estimated_words": len(cleaned_text.split())
        }
    }
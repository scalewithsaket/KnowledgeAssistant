"""
Extracts text from PDF pages while preserving page boundaries.
"""
from pathlib import Path
from pypdf import PdfReader

def extract_pages(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF while preserving page boundaries.

    Returns:
        A list of dictionaries:
        [
            {
                "page_number": 1,
                "text": "..."
            },
            ...
        ]
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip()
                }
            )

    return pages
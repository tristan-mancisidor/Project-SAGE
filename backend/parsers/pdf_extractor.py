"""PDF text extraction using PyMuPDF (fitz)."""

import fitz  # PyMuPDF


def extract_pdf_text(file_path: str) -> str:
    """Extract all text from a PDF file, page by page."""
    doc = fitz.open(file_path)
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            pages.append(f"--- Page {page_num + 1} ---\n{text}")
    doc.close()
    return "\n\n".join(pages)

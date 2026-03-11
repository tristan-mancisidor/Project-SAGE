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


def is_text_extractable(file_path: str) -> bool:
    """Returns True if meaningful text can be extracted (vs. scanned image PDF)."""
    doc = fitz.open(file_path)
    total_chars = 0
    for page_num in range(min(len(doc), 3)):
        total_chars += len(doc[page_num].get_text().strip())
    doc.close()
    return total_chars > 100


def extract_pdf_pages_as_images(file_path: str, max_pages: int = 5) -> list[str]:
    """Render PDF pages as base64-encoded PNG images for vision analysis.
    Used for scanned PDFs where text extraction yields garbage."""
    import base64
    doc = fitz.open(file_path)
    images = []
    for page_num in range(min(len(doc), max_pages)):
        page = doc[page_num]
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        images.append(base64.b64encode(img_bytes).decode())
    doc.close()
    return images

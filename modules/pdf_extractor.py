"""
pdf_extractor.py
----------------
Extracts, cleans, and validates text from PDF resumes using PyMuPDF.

Designed with clear beginner-friendly error classes so that corrupt,
empty, or scanned image-only PDFs are intercepted gracefully.
"""

import io
import re
from typing import Dict, Any, Union

try:
    import pymupdf as fitz
except ImportError:
    import fitz


class PDFExtractionError(Exception):
    """Base exception for all PDF extraction issues."""
    pass


class CorruptPDFError(PDFExtractionError):
    """Raised when the PDF file cannot be opened or parsed."""
    pass


class EmptyPDFError(PDFExtractionError):
    """Raised when the PDF has 0 pages or contains zero bytes."""
    pass


class ScannedPDFError(PDFExtractionError):
    """Raised when the PDF has pages, but no extractable text (scanned image resume)."""
    pass


def clean_extracted_text(raw_text: str) -> str:
    """
    Cleans raw PDF text by normalizing whitespace, removing null bytes,
    and stripping non-standard unprintable control characters.

    Args:
        raw_text: Raw string obtained from PyMuPDF.

    Returns:
        Cleaned, readable string.
    """
    if not raw_text:
        return ""

    # 1. Remove null bytes and unusual control characters (keep newlines and tabs)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', ' ', raw_text)

    # 2. Normalize carriage returns to standard newlines
    cleaned = cleaned.replace('\r\n', '\n').replace('\r', '\n')

    # 3. Collapse multiple horizontal spaces into a single space
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)

    # 4. Collapse three or more consecutive newlines into two
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    return cleaned.strip()


def extract_text_from_pdf(pdf_source: Union[str, bytes, io.BytesIO]) -> Dict[str, Any]:
    """
    Extracts text and metadata from a PDF file path or byte stream.

    Args:
        pdf_source: A file path string, bytes, or BytesIO buffer from Streamlit file uploader.

    Returns:
        A dictionary containing:
            - text: Cleaned full text of the resume
            - page_count: Total number of pages in the PDF
            - word_count: Total words found
            - char_count: Total characters found

    Raises:
        EmptyPDFError: If the file is 0 bytes or has 0 pages.
        CorruptPDFError: If PyMuPDF fails to read or parse the document.
        ScannedPDFError: If the document contains no selectable text (scanned image).
    """
    doc = None
    try:
        # Handle different input types
        if isinstance(pdf_source, str):
            doc = fitz.open(pdf_source)
        elif isinstance(pdf_source, bytes):
            if len(pdf_source) == 0:
                raise EmptyPDFError("The uploaded PDF file is empty (0 bytes).")
            doc = fitz.open(stream=pdf_source, filetype="pdf")
        elif hasattr(pdf_source, "read"):
            # Streamlit UploadedFile or io.BytesIO
            pdf_bytes = pdf_source.read()
            if hasattr(pdf_source, "seek"):
                pdf_source.seek(0)  # Reset pointer for subsequent reads if needed
            if len(pdf_bytes) == 0:
                raise EmptyPDFError("The uploaded PDF file is empty (0 bytes).")
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        else:
            raise PDFExtractionError("Unsupported PDF input type provided.")

    except EmptyPDFError:
        raise
    except Exception as e:
        raise CorruptPDFError(f"Unable to read the PDF file. It may be corrupt or encrypted. Details: {e}")

    try:
        page_count = len(doc)
        if page_count == 0:
            raise EmptyPDFError("The PDF document contains 0 pages.")

        extracted_pages = []
        for page_idx in range(page_count):
            page = doc[page_idx]
            extracted_pages.append(page.get_text("text"))

        full_raw_text = "\n".join(extracted_pages)
        cleaned_text = clean_extracted_text(full_raw_text)

        # Check for scanned image-only PDFs
        # A valid text-based resume should have at least 25 characters and several words
        words = cleaned_text.split()
        if len(cleaned_text) < 25 or len(words) < 5:
            raise ScannedPDFError(
                "No selectable text could be extracted from this PDF. "
                "It appears to be a scanned image or photo. "
                "ResumeIQ requires a text-based PDF (e.g., exported from MS Word, Google Docs, or LaTeX)."
            )

        return {
            "text": cleaned_text,
            "page_count": page_count,
            "word_count": len(words),
            "char_count": len(cleaned_text)
        }

    finally:
        if doc is not None:
            doc.close()

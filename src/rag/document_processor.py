# src/rag/document_processor.py
"""Document processing utilities for SocrAItes.

This module provides a simple PDF loader and chunking logic. In a full
implementation you would use a library like ``PyMuPDF`` or ``pdfplumber``
to extract text, then split it into overlapping chunks suitable for
embedding. For the MVP we supply a minimal placeholder implementation
that returns the raw text split by a fixed number of characters.
"""

from __future__ import annotations

import os
from typing import List

CHUNK_SIZE = 1000  # characters per chunk – adjust as needed
CHUNK_OVERLAP = 200

def load_pdf(file_path: str) -> str:
    """Load a PDF file and return its extracted text.

    The placeholder simply reads the file as binary and decodes it as UTF‑8.
    Replace with proper PDF parsing for production.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")
    # Placeholder: treat the PDF as plain text file.
    with open(file_path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback – ignore errors
        return raw.decode("utf-8", errors="ignore")

def chunk_text(text: str) -> List[str]:
    """Split *text* into overlapping chunks.

    This basic implementation uses a sliding window of ``CHUNK_SIZE``
    characters with an overlap of ``CHUNK_OVERLAP`` characters.
    """
    chunks: List[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + CHUNK_SIZE, length)
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def process_pdf(file_path: str) -> List[str]:
    """Convenience wrapper that loads a PDF and returns chunked text.
    """
    raw_text = load_pdf(file_path)
    return chunk_text(raw_text)

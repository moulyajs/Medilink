# date_extraction.py
"""
import re

# =====================================================
# OCR VERSION
# =====================================================

def extract_date(text):
    print("SECOND extract_date CALLED") ##just for testing
    return "03/07/2024"
# =====================================================
# DOCLING VERSION
# =====================================================

def extract_date_from_docling_tables(tables):
    print("extract_labs_from_docling called")
    return "03/07/2024"
"""
# date_extraction.py

import re
from datetime import datetime

DATE_PATTERNS = [
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}[APMapm]{2}\b"
]

def extract_date(data):

    # OCR lines
    if isinstance(data, list):

        for l in data[:12]:

            text = l.get("text", "")

            for p in DATE_PATTERNS:
                m = re.search(p, text)

                if m:
                    return m.group(0)

        return None

    # Plain text (Docling full_text)
    if isinstance(data, str):

        for p in DATE_PATTERNS:
            m = re.search(p, data)

            if m:
                return m.group(0)

        return None

    return None


def extract_date_from_docling_tables(tables):
    """
    Docling version
    """

    for table in tables:
        rows = table.get("rows", [])

        for row in rows:
            row_text = " ".join(str(x) for x in row)

            if "reported" in row_text.lower():

                for p in DATE_PATTERNS:
                    m = re.search(p, row_text)

                    if m:
                        return m.group(0)

    return None
# date_extraction.py

import re
from datetime import datetime

DATE_PATTERNS = [
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}[APMapm]{2}\b"
]

def extract_date(lines):
    """
    OCR version
    """
    for l in lines[:12]:
        text = l["text"]
        for p in DATE_PATTERNS:
            m = re.search(p, text)
            if m:
                return m.group(0)

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
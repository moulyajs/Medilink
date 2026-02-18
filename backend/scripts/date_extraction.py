import re

DATE_PATTERNS = [
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
    r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b"
]

def extract_date(lines):
    """
    Extract report/collection date from OCR lines
    """
    for l in lines[:12]:  # top area only
        text = l["text"]
        for p in DATE_PATTERNS:
            m = re.search(p, text)
            if m:
                return m.group(0)
    return None

import re
import pdfplumber
from datetime import datetime

# ===============================
# REGEX CONFIG
# ===============================
UNIT_PATTERN = re.compile(
    r"(mg/dl|g/dl|iu/ml|µmol|mmol|%|fl|pg|ng/ml|/cmm|cells|u/l)",
    re.I
)

VALUE_PATTERN = re.compile(r"<\s*\d+\.?\d*|\d+\.?\d*")
RANGE_PATTERN = re.compile(r"(\d+\.?\d*)\s*-\s*(\d+\.?\d*)")
LESS_PATTERN = re.compile(r"<\s*(\d+\.?\d*)")
GREATER_PATTERN = re.compile(r">\s*(\d+\.?\d*)")
UPTO_PATTERN = re.compile(r"upto\s*(\d+\.?\d*)", re.I)

DATE_PATTERN = re.compile(
    r"(\b\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}\b|"
    r"\b\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2}\b|"
    r"\b\d{1,2}[-\s](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-\s]\d{2,4}\b|"
    r"\b\d{1,2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{2,4}\b)",
    re.I
)

BLOCK_WORDS = {
    "interpretation", "reference", "guideline",
    "journal", "method", "explanation",
    "sample", "sex", "age", "coll"
}

# ===============================
# DATE EXTRACTION
# ===============================
def extract_date(text):
    lines = text.split("\n")

    report_date = None
    sample_date = None
    reg_date = None

    for i, line in enumerate(lines):
        lower = line.lower()

        if "report date" in lower:
            if m := DATE_PATTERN.search(line):
                report_date = m.group(0)
            elif i + 1 < len(lines):
                if m := DATE_PATTERN.search(lines[i + 1]):
                    report_date = m.group(0)

        elif "sample date" in lower:
            if m := DATE_PATTERN.search(line):
                sample_date = m.group(0)
            elif i + 1 < len(lines):
                if m := DATE_PATTERN.search(lines[i + 1]):
                    sample_date = m.group(0)

        elif "reg date" in lower:
            if m := DATE_PATTERN.search(line):
                reg_date = m.group(0)
            elif i + 1 < len(lines):
                if m := DATE_PATTERN.search(lines[i + 1]):
                    reg_date = m.group(0)

    return report_date or sample_date or reg_date


def normalize_date(date_str):
    if not date_str:
        return None

    for fmt in ("%d-%b-%Y", "%d %b %Y", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue

    return None


# ===============================
# PDF UTILS
# ===============================
def extract_pdf_pages(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(pdf.pages)]


def parse_reference(text):
    if m := RANGE_PATTERN.search(text):
        return float(m.group(1)), float(m.group(2))
    if m := UPTO_PATTERN.search(text):
        return None, float(m.group(1))
    if m := LESS_PATTERN.search(text):
        return None, float(m.group(1))
    if m := GREATER_PATTERN.search(text):
        return float(m.group(1)), None
    return None, None


# ===============================
# PDF EXTRACTION
# ===============================
def extract_labs_from_pdf(pdf_path):
    pages = extract_pdf_pages(pdf_path)
    results = []

    for page_no, text in pages:
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        date_raw = extract_date("\n".join(lines))
        date_obj = normalize_date(date_raw)

        for i, line in enumerate(lines):

            if any(w in line.lower() for w in BLOCK_WORDS):
                continue

            value_match = VALUE_PATTERN.search(line)
            if not value_match:
                continue

            value = float(value_match.group().replace("<", ""))

            unit_match = UNIT_PATTERN.search(line)
            unit = unit_match.group().lower() if unit_match else None

            if not unit and "/" not in line:
                continue

            test_name = line
            if i > 0 and not any(c.isdigit() for c in lines[i - 1]):
                test_name = lines[i - 1] + " " + line

            context = " ".join(lines[i:i + 4])
            low, high = parse_reference(context)

            if low is None and high is None:
                continue

            status = None
            if low is not None and value < low:
                status = "LOW"
            elif high is not None and value > high:
                status = "HIGH"

            if not status:
                continue

            clean_test = re.split(VALUE_PATTERN, test_name)[0].strip(" :-")

            results.append({
                "test": clean_test,
                "value": value,
                "unit": unit,
                "reference_range": (low, high),
                "status": status,
                "abnormal": True,
                "date": date_obj
            })

    return results


# ===============================
# PUBLIC API (IMPORTANT)
# ===============================
def extract_lab_results(input_data, source="pdf"):
    return extract_labs_from_pdf(input_data)
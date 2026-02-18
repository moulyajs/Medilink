import re
import pdfplumber

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

BLOCK_WORDS = {
    "interpretation", "reference", "guideline",
    "journal", "method", "explanation"
}

# ===============================
# PDF UTILITIES
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
# PDF LAB EXTRACTION
# ===============================
def extract_labs_from_pdf(pdf_path):
    pages = extract_pdf_pages(pdf_path)
    results = []

    for page_no, text in pages:
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        for i, line in enumerate(lines):

            if any(w in line.lower() for w in BLOCK_WORDS):
                continue

            value_match = VALUE_PATTERN.search(line)
            if not value_match:
                continue

            value = float(value_match.group().replace("<", ""))

            has_unit = UNIT_PATTERN.search(line)
            is_ratio = "/" in line
            if not has_unit and not is_ratio:
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
                "reference_range": (low, high),
                "status": status,
                "abnormal": True,
                "page": page_no
            })

    return results


# ===============================
# IMAGE (OCR) LAB EXTRACTION
# ===============================
def extract_labs_from_ocr(lines):
    """
    lines = [
      {"text": "...", "line_no": 1},
      ...
    ]
    """
    results = []

    for i, l in enumerate(lines):
        text = l["text"]

        value_match = VALUE_PATTERN.search(text)
        if not value_match:
            continue

        value = float(value_match.group().replace("<", ""))
        if not UNIT_PATTERN.search(text):
            continue

        test_name = text
        if i > 0 and not any(c.isdigit() for c in lines[i - 1]["text"]):
            test_name = lines[i - 1]["text"] + " " + text

        context = " ".join(x["text"] for x in lines[i:i + 3])
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
            "reference_range": (low, high),
            "status": status,
            "abnormal": True
        })


    return results

def extract_lab_results(source, is_pdf=False):
    """
    Unified lab extractor.
    - If PDF → uses pdfplumber
    - If OCR → uses OCR lines
    """

    if is_pdf:
        return extract_labs_from_pdf(source)

    # OCR case
    return extract_labs_from_ocr(source)


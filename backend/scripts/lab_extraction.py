import re
import pdfplumber

# ===============================
# REGEX CONFIG
# ===============================
UNIT_PATTERN = re.compile(
    r"(mg/dl|g/dl|iu/ml|µmol|mmol|%|fl|pg|ng/ml|cells|u/l|cu\.mm|lakh)",
    re.I
)

VALUE_PATTERN = re.compile(r"<\s*\d+\.?\d*|\d+[\d,]*\.?\d*")

# 🔥 IMPROVED RANGE (handles merged text)
RANGE_PATTERN = re.compile(r"(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)")

LESS_PATTERN = re.compile(r"<\s*(\d+\.?\d*)")
GREATER_PATTERN = re.compile(r">\s*(\d+\.?\d*)")

BLOCK_WORDS = {
    "interpretation", "reference", "guideline",
    "journal", "method", "explanation"
}


# ===============================
# PARSE RANGE (ROBUST)
# ===============================
def parse_reference(text):
    if not text:
        return None, None

    text = text.replace(",", "")

    if m := RANGE_PATTERN.search(text):
        return float(m.group(1)), float(m.group(2))

    if m := LESS_PATTERN.search(text):
        return None, float(m.group(1))

    if m := GREATER_PATTERN.search(text):
        return float(m.group(1)), None

    return None, None


# ===============================
# 🔥 IMAGE OCR EXTRACTION (FINAL FIX)
# ===============================
def extract_labs_from_ocr(rows):
    results = []

    for row in rows:
        cols = row.get("columns", [])

        if len(cols) < 2:
            continue

        test = cols[0].strip()

        # skip headers
        if any(x in test.lower() for x in ["testname", "result", "units", "range"]):
            continue

        # --------------------------
        # VALUE
        # --------------------------
        value_match = VALUE_PATTERN.search(cols[1])
        if not value_match:
            continue

        value_str = value_match.group().replace("<", "").replace(",", "")

        try:
            value = float(value_str)
        except:
            continue

        # --------------------------
        # 🔥 FULL TEXT (CRITICAL FIX)
        # --------------------------
        full_text = " ".join(cols)

        # --------------------------
        # RANGE
        # --------------------------
        low, high = parse_reference(full_text)

        # --------------------------
        # UNIT
        # --------------------------
        unit_match = UNIT_PATTERN.search(full_text)
        unit = unit_match.group() if unit_match else ""

        # --------------------------
        # 🔥 DO NOT SKIP if no range
        # --------------------------
        # (THIS WAS YOUR MAIN BUG)
        status = "UNKNOWN"

        if low is not None or high is not None:
            status = "NORMAL"

            if low is not None and value < low:
                status = "LOW"
            elif high is not None and value > high:
                status = "HIGH"

        results.append({
            "test": test,
            "value": value,
            "unit": unit,
            "reference_range": (low, high),
            "status": status,
            "abnormal": status in ["LOW", "HIGH"]
        })

    return results


# ===============================
# PDF EXTRACTION
# ===============================
def extract_pdf_pages(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(pdf.pages)]


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

            value_str = value_match.group().replace("<", "").replace(",", "")

            try:
                value = float(value_str)
            except:
                continue

            context = " ".join(lines[i:i + 4])
            low, high = parse_reference(context)

            unit_match = UNIT_PATTERN.search(line)
            unit = unit_match.group() if unit_match else ""

            status = "UNKNOWN"

            if low is not None or high is not None:
                status = "NORMAL"

                if low is not None and value < low:
                    status = "LOW"
                elif high is not None and value > high:
                    status = "HIGH"

            results.append({
                "test": line,
                "value": value,
                "unit": unit,
                "reference_range": (low, high),
                "status": status,
                "abnormal": status in ["LOW", "HIGH"],
                "page": page_no
            })

    return results


# ===============================
# PUBLIC API
# ===============================
def extract_lab_results(input_data, source="image"):
    if source == "pdf":
        return extract_labs_from_pdf(input_data)

    return extract_labs_from_ocr(input_data)
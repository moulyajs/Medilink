import pdfplumber
import re

# ===============================
# CONFIG
# ===============================
PDF_PATH = "data/sterling_labReport.pdf"

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
    "interpretation", "reference", "guideline", "journal",
    "foundation", "study", "method", "explanation"
}

# ===============================
# PDF EXTRACTION
# ===============================
def extract_pages(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(pdf.pages)]


# ===============================
# REFERENCE PARSING
# ===============================
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
# CORE LOGIC (ChatGPT-style)
# ===============================
def extract_abnormal(page_text, page_no):
    results = []
    lines = [l.strip() for l in page_text.split("\n") if l.strip()]

    for i, line in enumerate(lines):

        # Skip interpretation / citation blocks
        if any(w in line.lower() for w in BLOCK_WORDS):
            continue

        # Detect numeric value
        value_match = VALUE_PATTERN.search(line)
        if not value_match:
            continue

        value = float(value_match.group().replace("<", ""))

        # Unit OR ratio (ratios are unitless)
        has_unit = UNIT_PATTERN.search(line)
        is_ratio = "/" in line

        if not has_unit and not is_ratio:
            continue

        # Reconstruct vertically split test names
        test_name = line
        if i > 0 and not any(c.isdigit() for c in lines[i - 1]):
            test_name = lines[i - 1] + " " + line

        # Look ahead for reference range
        window = " ".join(lines[i:i + 4])
        low, high = parse_reference(window)

        if low is None and high is None:
            continue

        # Determine abnormality
        status = None
        if low is not None and value < low:
            status = "LOW"
        elif high is not None and value > high:
            status = "HIGH"

        if not status:
            continue

        clean_name = re.split(VALUE_PATTERN, test_name)[0].strip(" :-")

        results.append({
            "page": page_no,
            "test": clean_name,
            "value": value,
            "range": f"{low or ''}-{high or ''}".strip("-"),
            "status": status
        })

    return results


# ===============================
# MAIN
# ===============================
def main():
    pages = extract_pages(PDF_PATH)
    all_results = []

    for page_no, text in pages:
        all_results.extend(extract_abnormal(text, page_no))

    print("\n🔴 Abnormal Findings\n")

    if not all_results:
        print("No abnormal values detected.")
        return

    for r in all_results:
        arrow = "↑" if r["status"] == "HIGH" else "↓"
        print(
            f"Page {r['page']} | {r['test']}: "
            f"{r['value']} {arrow} (Ref: {r['range']})"
        )


if __name__ == "__main__":
    main()

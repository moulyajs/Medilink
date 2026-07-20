import re
from datetime import datetime
from date_extraction import extract_date
from date_extraction import extract_date_from_docling_tables
# ===============================
# REGEX CONFIG
# ===============================

UNIT_PATTERN = re.compile(
    r"""
    (mg/dl|
    g/dl|
    gm/dl|
    iu/ml|
    uiu/ml|
    µmol|
    mmol|
    %|
    fl|
    pg|
    ng/ml|
    cells/cu\.mm|
    cells/cumm|
    mill/cu\.mm|
    cells|
    u/l)
    """,
    re.I | re.X
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



def normalize_date(date_str):
    if not date_str:
        return None

    for fmt in (
        "%d-%b-%Y", "%d %b %Y",
        "%d/%m/%Y", "%d-%m-%Y",
        "%Y-%m-%d", "%Y/%m/%d"
    ):
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue

    return None


# ===============================
# REFERENCE PARSER
# ===============================
def parse_reference(text):
    if not text:
        return None, None

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
# OCR / DOCLING LINE PARSER
# ===============================
def extract_labs_from_lines(lines):
    """
    lines format:
    [
        {"text": "...", "page": 1},
        ...
    ]
    """
    if not lines:
        return []

    text_lines = []
    for item in lines:
        if isinstance(item, dict):
            txt = item.get("text", "").strip()
        else:
            txt = str(item).strip()

        if txt:
            text_lines.append(txt)

    if not text_lines:
        return []

    results = []

    date_raw = extract_date("\n".join(text_lines))
    date_obj = normalize_date(date_raw)
    print("Date raw",date_raw)
    for i, line in enumerate(text_lines):

        if any(w in line.lower() for w in BLOCK_WORDS):
            continue

        value_match = VALUE_PATTERN.search(line)
        if not value_match:
            continue

        try:
            value = float(value_match.group().replace("<", "").strip())
        except:
            continue

        unit_match = UNIT_PATTERN.search(line)
        unit = unit_match.group().lower() if unit_match else None

        if not unit and "/" not in line:
            continue

        test_name = line
        if i > 0 and not any(c.isdigit() for c in text_lines[i - 1]):
            test_name = text_lines[i - 1] + " " + line

        context_window = text_lines[i:i + 4]
        context = " ".join(context_window)

        low, high = parse_reference(context)

        if low is None and high is None:
            continue

        status = None
        if low is not None and value < low:
            status = "LOW"
        elif high is not None and value > high:
            status = "HIGH"

        

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
# TABLE PARSER FOR DOCLING TABLES
# ===============================
def extract_labs_from_docling_tables(tables):
    """
    tables format from docling.py:
    [
        {
            "table_index": 0,
            "rows": [
                ["Test", "Value", "Unit", "Range"],
                ...
            ]
        }
    ]
    """
    results = []

    if not tables:
        return results
    for table in tables:
        rows = table.get("rows", [])
        if not rows or len(rows) < 2:
            continue

        # skip header row
        for row in rows[1:]:
            row_text = " ".join(str(x) for x in row if x is not None).strip()
            if not row_text:
                continue

            value_match = VALUE_PATTERN.search(row_text)
            if not value_match:
                continue

            try:
                value = float(value_match.group().replace("<", "").strip())
            except:
                continue

            unit_match = UNIT_PATTERN.search(row_text)
            unit = unit_match.group().lower() if unit_match else None

            low, high = parse_reference(row_text)
            if low is None and high is None:
                continue

            status = "NORMAL"
            abnormal = False

            if low is not None and value < low:
                status = "LOW"
                abnormal = True

            elif high is not None and value > high:
                status = "HIGH"
                abnormal = True

            # take first cell as test name if available
            test_name = str(row[0]).strip() if row else "Unknown Test"

            results.append({
                "test": test_name,
                "value": value,
                "unit": unit,
                "reference_range": (low, high),
                "status": status,
                "abnormal": abnormal,
                "date":None
            })

    return results


# ===============================
# DOCLING PARSER
# ===============================
# ===============================
# DOCLING PARSER
# ===============================
def extract_labs_from_docling(docling_data):
    """
    docling_data:
    {
        "full_text": str,
        "lines": [...],
        "tables": [...],
        "doc_type": ...
    }
    """
    if not isinstance(docling_data, dict):
        return []

    tables = docling_data.get("tables", [])
    full_text = docling_data.get("full_text", "")

    # Extract report date from the entire PDF text
    report_date = normalize_date(
        extract_date(full_text)
    )
    print("Report date",report_date)
    results = extract_labs_from_docling_tables(tables)

    # Assign the extracted date to every lab
    for lab in results:
        lab["date"] = report_date

    return results


# ===============================
# PUBLIC API
# ===============================
def extract_lab_results(input_data, source="ocr"):
    """
    source:
      - "ocr"     -> input_data = visit_lines
      - "docling" -> input_data = parse_pdf_with_docling(...) output
    """
    if source == "docling":
        return extract_labs_from_docling(input_data)

    return extract_labs_from_lines(input_data)
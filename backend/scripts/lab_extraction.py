import re
from datetime import datetime

from scripts.date_extraction import extract_date
from scripts.date_extraction import extract_date_from_docling_tables


# ============================================================
# REGEX CONFIG
# ============================================================

UNIT_PATTERN = re.compile(
    r"""
    (mg/dl|
    mg/l|
    g/dl|
    gm/dl|
    gms%|
    iu/ml|
    uiu/ml|
    µmol|
    umol|
    mmol|
    %|
    fl|
    pg|
    ng/ml|
    cells/cu\.mm|
    cells/cumm|
    mill/cu\.mm|
    cells|
    u/l|
    iu|
    mg|
    g/dl)
    """,
    re.I | re.X
)


# Supports:
# 7
# 7.2
# 7,200
# 253,000
# <5
VALUE_PATTERN = re.compile(
    r"<\s*\d+(?:,\d{3})*(?:\.\d+)?"
    r"|\d+(?:,\d{3})*(?:\.\d+)?"
)


RANGE_PATTERN = re.compile(
    r"(\d+(?:,\d{3})*(?:\.\d+)?)"
    r"\s*-\s*"
    r"(\d+(?:,\d{3})*(?:\.\d+)?)"
)


LESS_PATTERN = re.compile(
    r"<\s*(\d+(?:,\d{3})*(?:\.\d+)?)"
)


GREATER_PATTERN = re.compile(
    r">\s*(\d+(?:,\d{3})*(?:\.\d+)?)"
)


UPTO_PATTERN = re.compile(
    r"upto\s*(\d+(?:,\d{3})*(?:\.\d+)?)",
    re.I
)


DATE_PATTERN = re.compile(
    r"(\b\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}\b|"
    r"\b\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2}\b|"
    r"\b\d{1,2}[-\s](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-\s]\d{2,4}\b|"
    r"\b\d{1,2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{2,4}\b)",
    re.I
)


BLOCK_WORDS = {
    "interpretation",
    "reference",
    "guideline",
    "journal",
    "method",
    "explanation",
    "sample",
    "sex",
    "age",
    "coll"
}


# ============================================================
# HELPERS
# ============================================================

def clean_number(value):
    """
    Convert values such as:
        7,200   -> 7200.0
        253,000 -> 253000.0
        11.9    -> 11.9
    """

    if value is None:
        return None

    value = str(value).replace(",", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


# ============================================================
# DATE EXTRACTION
# ============================================================

def normalize_date(date_str):
    if not date_str:
        return None

    date_str = str(date_str).strip()

    # Remove time if present
    date_str = re.split(
        r"\s+\d{1,2}:\d{2}",
        date_str
    )[0].strip()

    for fmt in (
        "%d-%b-%Y",
        "%d %b %Y",
        "%d-%B-%Y",
        "%d %B %Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
    ):
        try:
            return datetime.strptime(
                date_str,
                fmt
            ).date()
        except ValueError:
            continue

    return None


# ============================================================
# REFERENCE PARSER
# ============================================================

def parse_reference(text):
    if not text:
        return None, None

    # Example: 11.5-16.4
    match = RANGE_PATTERN.search(text)

    if match:
        low = clean_number(match.group(1))
        high = clean_number(match.group(2))

        return low, high

    # Example: upto 10
    match = UPTO_PATTERN.search(text)

    if match:
        high = clean_number(match.group(1))

        return None, high

    # Example: < 5
    match = LESS_PATTERN.search(text)

    if match:
        high = clean_number(match.group(1))

        return None, high

    # Example: > 10
    match = GREATER_PATTERN.search(text)

    if match:
        low = clean_number(match.group(1))

        return low, None

    return None, None


# ============================================================
# STATUS CALCULATION
# ============================================================

def calculate_status(value, low, high):

    if value is None:
        return "NORMAL", False

    if low is not None and value < low:
        return "LOW", True

    if high is not None and value > high:
        return "HIGH", True

    return "NORMAL", False


# ============================================================
# OCR / FULL-TEXT LINE PARSER
# ============================================================

def extract_labs_from_lines(lines):
    """
    lines format:

    [
        {"text": "...", "page": 1},
        ...
    ]

    This is also used as the fallback when
    Docling does not return structured tables.
    """

    if not lines:
        return []

    text_lines = []

    for item in lines:

        if isinstance(item, dict):
            txt = item.get(
                "text",
                ""
            ).strip()

        else:
            txt = str(item).strip()

        if txt:
            text_lines.append(txt)

    if not text_lines:
        return []

    results = []

    # ========================================================
    # REPORT DATE
    # ========================================================

    full_text = "\n".join(text_lines)

    date_raw = extract_date(
        full_text
    )

    date_obj = normalize_date(
        date_raw
    )

    print(
        "Date raw:",
        date_raw
    )

    print(
        "Date object:",
        date_obj
    )

    # ========================================================
    # PROCESS EACH LINE
    # ========================================================

    for i, line in enumerate(text_lines):

        lower_line = line.lower()

        # Skip obvious non-lab lines
        if any(
            word in lower_line
            for word in BLOCK_WORDS
        ):
            continue

        # ----------------------------------------------------
        # Find numeric value
        # ----------------------------------------------------

        value_match = VALUE_PATTERN.search(
            line
        )

        if not value_match:
            continue

        raw_value = value_match.group()

        value = clean_number(
            raw_value.replace("<", "")
        )

        if value is None:
            continue

        # ----------------------------------------------------
        # Find unit
        # ----------------------------------------------------

        unit_match = UNIT_PATTERN.search(
            line
        )

        unit = (
            unit_match.group().lower()
            if unit_match
            else None
        )

        # ----------------------------------------------------
        # Build test name
        # ----------------------------------------------------

        test_name = line

        if i > 0:

            previous_line = text_lines[
                i - 1
            ]

            # If previous line looks like a test name
            if (
                not any(
                    c.isdigit()
                    for c in previous_line
                )
                and previous_line
            ):
                test_name = (
                    previous_line
                    + " "
                    + line
                )

        # ----------------------------------------------------
        # Reference range context
        # ----------------------------------------------------

        context_window = text_lines[
            i:i + 4
        ]

        context = " ".join(
            context_window
        )

        low, high = parse_reference(
            context
        )

        # No reference range means
        # we cannot safely classify it
        if low is None and high is None:
            continue

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        status, abnormal = calculate_status(
            value,
            low,
            high
        )

        # ----------------------------------------------------
        # Clean test name
        # ----------------------------------------------------

        clean_test = re.split(
            VALUE_PATTERN,
            test_name
        )[0].strip(
            " :-"
        )

        if not clean_test:
            continue

        # Avoid obviously bad names
        if len(clean_test) < 2:
            continue

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        results.append(
            {
                "test": clean_test,
                "value": value,
                "unit": unit,
                "reference_range": (
                    low,
                    high
                ),
                "status": status,
                "abnormal": abnormal,
                "date": date_obj
            }
        )

    return results


# ============================================================
# TABLE PARSER FOR DOCLING TABLES
# ============================================================

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

        rows = table.get(
            "rows",
            []
        )

        if not rows or len(rows) < 2:
            continue

        # ====================================================
        # HEADER
        # ====================================================

        header = [
            str(x).strip().lower()
            if x is not None
            else ""
            for x in rows[0]
        ]

        # ====================================================
        # DATA ROWS
        # ====================================================

        for row in rows[1:]:

            if not row:
                continue

            cells = [
                str(x).strip()
                if x is not None
                else ""
                for x in row
            ]

            row_text = " ".join(
                cells
            ).strip()

            if not row_text:
                continue

            # ------------------------------------------------
            # Find numeric value
            # ------------------------------------------------

            value_match = VALUE_PATTERN.search(
                row_text
            )

            if not value_match:
                continue

            raw_value = value_match.group()

            value = clean_number(
                raw_value.replace("<", "")
            )

            if value is None:
                continue

            # ------------------------------------------------
            # Unit
            # ------------------------------------------------

            unit_match = UNIT_PATTERN.search(
                row_text
            )

            unit = (
                unit_match.group().lower()
                if unit_match
                else None
            )

            # ------------------------------------------------
            # Reference range
            # ------------------------------------------------

            low, high = parse_reference(
                row_text
            )

            if low is None and high is None:
                continue

            # ------------------------------------------------
            # Status
            # ------------------------------------------------

            status, abnormal = calculate_status(
                value,
                low,
                high
            )

            # ------------------------------------------------
            # Test name
            # ------------------------------------------------

            test_name = (
                cells[0]
                if cells
                else "Unknown Test"
            )

            # If first cell is not useful,
            # try to find a better name.
            if (
                not test_name
                or test_name.lower()
                in {
                    "test",
                    "test name",
                    "parameter",
                    "investigation"
                }
            ):

                test_name = (
                    cells[0]
                    if cells
                    else "Unknown Test"
                )

            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            results.append(
                {
                    "test": test_name,
                    "value": value,
                    "unit": unit,
                    "reference_range": (
                        low,
                        high
                    ),
                    "status": status,
                    "abnormal": abnormal,
                    "date": None
                }
            )

    return results


# ============================================================
# DOCLING PARSER
# ============================================================

def extract_labs_from_docling(docling_data):
    """
    docling_data:

    {
        "full_text": str,
        "lines": [...],
        "tables": [...],
        "doc_type": ...
    }

    Extraction strategy:

    1. Try structured Docling tables.
    2. If no labs are found, use full-text/line extraction.
    3. Assign report date to all extracted labs.
    """

    if not isinstance(
        docling_data,
        dict
    ):
        return []

    tables = docling_data.get(
        "tables",
        []
    )

    full_text = docling_data.get(
        "full_text",
        ""
    )

    lines = docling_data.get(
        "lines",
        []
    )

    # ========================================================
    # REPORT DATE
    # ========================================================

    report_date = normalize_date(
        extract_date(full_text)
    )

    print(
        "Report date:",
        report_date
    )

    # ========================================================
    # FIRST: TABLE EXTRACTION
    # ========================================================

    results = extract_labs_from_docling_tables(
        tables
    )

    print(
        "Labs extracted from Docling tables:",
        len(results)
    )

    # ========================================================
    # FALLBACK: FULL TEXT
    # ========================================================

    if not results:

        print(
            "⚠️ No labs found in Docling tables."
        )

        print(
            "⚠️ Trying full-text lab extraction..."
        )

        # ----------------------------------------------------
        # Use existing Docling lines
        # ----------------------------------------------------

        if lines:

            text_lines = lines

        # ----------------------------------------------------
        # Otherwise create lines from full text
        # ----------------------------------------------------

        elif full_text:

            text_lines = [
                {
                    "text": line,
                    "page": 1
                }
                for line in full_text.splitlines()
                if line.strip()
            ]

        else:

            text_lines = []

        # ----------------------------------------------------
        # Extract labs
        # ----------------------------------------------------

        results = extract_labs_from_lines(
            text_lines
        )

        print(
            "Labs extracted from full text:",
            len(results)
        )

    # ========================================================
    # ASSIGN REPORT DATE
    # ========================================================

    for lab in results:

        if not lab.get("date"):
            lab["date"] = report_date

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print(
        "FINAL LAB COUNT:",
        len(results)
    )

    for lab in results:
        print(
            "LAB:",
            lab
        )

    return results


# ============================================================
# PUBLIC API
# ============================================================

def extract_lab_results(
    input_data,
    source="ocr"
):
    """
    source:

      "ocr"
          input_data = visit_lines

      "docling"
          input_data =
          parse_pdf_with_docling(...) output
    """

    if source == "docling":

        return extract_labs_from_docling(
            input_data
        )

    return extract_labs_from_lines(
        input_data
    )
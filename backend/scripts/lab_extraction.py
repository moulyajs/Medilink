import re

def extract_lab_results(ocr_lines):
    results = []
    i = 0
    in_lab_section = False

    lab_section_headers = [
        "investigation",
        "result",
        "reference",
        "reference value",
        "unit"
    ]

    lab_section_ends = [
        "interpretation",
        "end of report",
        "verified by",
        "signed by",
        "thanks",
        "generated on",
        "page"
    ]

    while i < len(ocr_lines):
        text = ocr_lines[i]["text"].strip()
        text_lower = text.lower()

        # --- ENTER / EXIT LAB SECTION ---
        if any(h in text_lower for h in lab_section_headers):
            in_lab_section = True
            i += 1
            continue

        if any(e in text_lower for e in lab_section_ends):
            in_lab_section = False
            i += 1
            continue

        if not in_lab_section:
            i += 1
            continue

        # --- SKIP KNOWN NON-TEST LINES ---
        skip_contains = [
            "count",
            "indices",
            "differential",
            "sample type",
            "blood"
        ]

        if any(s in text_lower for s in skip_contains):
            i += 1
            continue

        # --- TEST NAME CANDIDATE ---
        test_candidate = re.match(r"^[A-Za-z][A-Za-z\s\(\)\/\-]{3,}$", text)

        if test_candidate:
            test_name = text

            # 🔑 CRITICAL CHECK:
            # Next line MUST contain a numeric value
            if i + 1 >= len(ocr_lines):
                i += 1
                continue

            next_text = ocr_lines[i + 1]["text"]

            value_match = re.search(r"\b\d+(\.\d+)?\b", next_text)
            if not value_match:
                i += 1
                continue

            value = value_match.group()
            unit = None
            ref_range = None
            flag = None

            # Look further for unit and reference range
            for j in range(i + 2, min(i + 6, len(ocr_lines))):
                follow_text = ocr_lines[j]["text"]

                rng = re.search(
                    r"(low|high|borderline)?\s*(\d+(\.\d+)?\s*-\s*\d+(\.\d+)?)",
                    follow_text,
                    re.I
                )
                if rng and ref_range is None:
                    ref_range = rng.group(2)
                    if rng.group(1):
                        flag = rng.group(1).capitalize()

                u = re.search(
                    r"(g\/dl|mg\/dl|mill\/cumm|cumm|%)",
                    follow_text,
                    re.I
                )
                if u and unit is None:
                    unit = u.group(1)

            results.append({
                "test": test_name,
                "value": value,
                "unit": unit,
                "reference_range": ref_range,
                "flag": flag
            })

            i += 4
            continue

        i += 1

    return results
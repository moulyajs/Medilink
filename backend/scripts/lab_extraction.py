# scripts/lab_extraction.py
import re

UNIT_REGEX = r"(mg/dl|g/dl|mmol/l|iu/l|u/l|%|ng/ml|pg/ml)"
HEADER_WORDS = {
    "test", "result", "unit", "units",
    "normal", "normal values", "reference"
}

def clean_unit(text):
    t = text.lower().replace(" ", "")
    t = t.replace("di", "dl").replace("d1", "dl")
    return t

def is_junk(text):
    t = text.lower()
    return any(x in t for x in [
        "www", "http", "email", "phone", "technician",
        "report", "end of report", "sample", "lab"
    ])

def extract_lab_results(lines):
    results = []
    in_table = False

    i = 0
    while i < len(lines):
        text = lines[i]["text"].strip()

        # Enter table
        if any(h in text.lower() for h in HEADER_WORDS):
            in_table = True
            i += 1
            continue

        if not in_table or is_junk(text):
            i += 1
            continue

        # ---- Test name ----
        if not re.fullmatch(r"[A-Za-z][A-Za-z\s\/\-\(\)]{3,40}", text):
            i += 1
            continue

        test = text
        value = unit = ref = None

        # Look ahead safely
        for j in range(i + 1, min(i + 6, len(lines))):
            nxt = lines[j]["text"]

            if value is None:
                m = re.search(r"(<|>)?\s*\d+(\.\d+)?", nxt)
                if m:
                    value = m.group().strip()
                    continue

            if unit is None:
                u = re.search(UNIT_REGEX, clean_unit(nxt))
                if u:
                    unit = u.group(1)

            if ref is None:
                r1 = re.search(r"\d+(\.\d+)?\s*-\s*\d+(\.\d+)?", nxt)
                r2 = re.search(r"(upto|<|>)\s*\d+(\.\d+)?", nxt, re.I)
                if r1:
                    ref = r1.group()
                elif r2:
                    ref = r2.group()

        if value:
            results.append({
                "test": test,
                "value": value,
                "unit": unit,
                "reference_range": ref,
                "flag": None
            })

        i += 1

    return results

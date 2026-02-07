# lab_extraction.py
import re

UNIT_REGEX = r"(mg/dl|g/dl|iu/l|u/l|mmol/l|mill/cumm|cumm|%|ng/ml|pg/ml)"

def normalize_text(t):
    t = t.lower()
    t = t.replace(" ", "")
    t = t.replace("di", "dl")
    t = t.replace("d1", "dl")
    t = t.replace("mg/di", "mg/dl")
    t = t.replace("mg/d1", "mg/dl")
    return t


def looks_like_test_name(text):
    t = text.strip()
    t_low = t.lower()

    # ❌ URLs, emails, phones
    if re.search(r"(www\.|http|\.com|@|\+91|\d{3}[- ]\d{3})", t_low):
        return False

    # ❌ units only
    if re.fullmatch(r"(mg|g|iu|mmol|dl|ml|%)\s*/?\s*(dl|l)?", t_low):
        return False

    # ❌ reference / explanatory text
    if re.search(r"(upto|normal|low|high|moderate|risk|factor)", t_low):
        return False

    # ❌ admin / footer junk
    if any(w in t_low for w in [
        "lab", "technician", "doctor", "mbbs", "md",
        "email", "mobile", "phone", "address",
        "india", "pvt", "ltd", "software"
    ]):
        return False

    # ❌ table headers
    if t_low in {"test", "result", "unit", "units", "normal values"}:
        return False

    # must contain alphabets
    if not re.search(r"[a-zA-Z]", t):
        return False

    # overly long junk lines
    if len(t) > 40:
        return False

    return True


def extract_lab_results(ocr_lines):
    results = []
    used_indices = set()

    for i in range(len(ocr_lines)):
        if i in used_indices:
            continue

        text = ocr_lines[i]["text"].strip()

        if not looks_like_test_name(text):
            continue

        # 🔍 find numeric value near the test
        value = None
        value_line = None

        for j in range(i + 1, min(i + 6, len(ocr_lines))):
            candidate = ocr_lines[j]["text"]
            m = re.search(r"(<|>)?\s*\d+(\.\d+)?", candidate)
            if m:
                value = m.group().strip()
                value_line = j
                break

        # ❌ no value → skip
        if not value:
            continue

        # ❌ skip reference-only values like <130
        if value.startswith("<") or value.startswith(">"):
            continue

        unit = None
        ref_range = None
        flag = None

        for k in range(value_line + 1, min(value_line + 7, len(ocr_lines))):
            follow = ocr_lines[k]["text"]
            norm = normalize_text(follow)

            # unit (skip ratios like LDL/HDL)
            if unit is None and "/" not in text:
                u = re.search(UNIT_REGEX, norm)
                if u:
                    unit = u.group(1)

            # reference range
            if ref_range is None:
                r1 = re.search(r"\d+(\.\d+)?\s*-\s*\d+(\.\d+)?", follow)
                r2 = re.search(r"(upto|<|>)\s*\d+(\.\d+)?", follow, re.I)
                if r1:
                    ref_range = r1.group()
                elif r2:
                    ref_range = r2.group()

            # abnormal flag
            if any(w in follow.lower() for w in ["high", "low", "borderline"]):
                flag = follow.strip()

        results.append({
            "test": text,
            "value": value,
            "unit": unit,
            "reference_range": ref_range,
            "flag": flag
        })

        used_indices.update(range(i, value_line + 1))

    return results

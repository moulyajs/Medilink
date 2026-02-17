import re

STATUS_WORDS = {"low", "high", "borderline", "normal"}

def normalize_test_name(name):
    name = name.strip()
    name = re.sub(r"\([^)]*\)", "", name)  # remove (Hb)
    name = name.title()
    return name
def parse_range(text):
    if not text:
        return None
    m = re.search(r"(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)", text)
    if not m:
        return None
    return [float(m.group(1)), float(m.group(3))]
def infer_unit(value, ref_range, unit):
    if unit:
        return unit

    try:
        v = float(value)
    except:
        return None

    if ref_range and ref_range[1] <= 100:
        return "%"
    return None
def detect_status(value, ref_range, flag):
    if flag:
        return flag.lower()

    if not ref_range:
        return None

    try:
        v = float(value)
    except:
        return None

    if v < ref_range[0]:
        return "low"
    if v > ref_range[1]:
        return "high"
    return "normal"
def normalize_lab_results(raw_results):
    normalized = []
    pending_parent = None

    for r in raw_results:
        test = r["test"].strip().lower()

        # ❌ Skip pure labels
        if test in STATUS_WORDS:
            continue

        test_name = normalize_test_name(r["test"])
        ref_range = parse_range(r.get("reference_range"))
        unit = infer_unit(r.get("value"), ref_range, r.get("unit"))
        status = detect_status(r.get("value"), ref_range, r.get("flag"))

        result = {
            "test": test_name,
            "value": float(r["value"]) if r.get("value") else None,
            "unit": unit,
            "reference_range": ref_range,
            "status": status
        }

        # 🧠 Hierarchy detection
        if result["value"] is None:
            pending_parent = {
                "test": test_name,
                "children": []
            }
            normalized.append(pending_parent)
        elif pending_parent and unit == "%":
            pending_parent["children"].append(result)
        else:
            normalized.append(result)

    return normalized
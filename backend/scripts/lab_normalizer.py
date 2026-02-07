# lab_normalizer.py
import re

STATUS_WORDS = {"low", "high", "borderline", "normal"}


def normalize_test_name(name):
    name = name.strip()
    name = re.sub(r"\([^)]*\)", "", name)  # remove (Hb)
    return name.title()


def parse_range(text):
    if not text:
        return None
    m = re.search(r"(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)", text)
    if not m:
        return None
    return [float(m.group(1)), float(m.group(3))]


def safe_float(val):
    try:
        return float(val)
    except:
        return None


def infer_unit(value, ref_range, unit):
    if unit:
        return unit
    if ref_range and ref_range[1] <= 100:
        return "%"
    return None


def detect_status(value, ref_range, flag):
    if flag:
        return flag.lower()
    if value is None or not ref_range:
        return None
    if value < ref_range[0]:
        return "low"
    if value > ref_range[1]:
        return "high"
    return "normal"


def is_valid_result(test, value):
    if value is None:
        return False
    if re.search(r"(www|lab|technician|software)", test.lower()):
        return False
    return True


def normalize_lab_results(raw_results):
    normalized = []

    for r in raw_results:
        test_raw = r.get("test", "").strip().lower()

        # ❌ skip pure labels
        if test_raw in STATUS_WORDS:
            continue

        value = safe_float(r.get("value"))
        test_name = normalize_test_name(r.get("test", ""))

        if not is_valid_result(test_name, value):
            continue

        ref_range = parse_range(r.get("reference_range"))
        unit = infer_unit(value, ref_range, r.get("unit"))
        status = detect_status(value, ref_range, r.get("flag"))

        normalized.append({
            "test": test_name,
            "value": value,
            "unit": unit,
            "reference_range": ref_range,
            "status": status
        })

    return normalized

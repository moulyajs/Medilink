# lab_normalizer.py
import re


def clean_name(name):
    if not name:
        return None
    name = re.sub(r"\s{2,}", " ", name.strip())
    return name.title()


def parse_range(text):
    """
    Returns:
    - (low, high)
    - None if range is invalid
    """
    if not text:
        return None

    # <130  → (None, 130)
    m1 = re.search(r"<\s*(\d+(\.\d+)?)", text)
    if m1:
        return (None, float(m1.group(1)))

    # >200 → (200, None)
    m2 = re.search(r">\s*(\d+(\.\d+)?)", text)
    if m2:
        return (float(m2.group(1)), None)

    # 150 - 250
    m = re.search(r"(\d+(\.\d+)?)\s*[-–]\s*(\d+(\.\d+)?)", text)
    if m:
        return (float(m.group(1)), float(m.group(3)))

    return None


def normalize_unit(unit):
    if not unit:
        return None

    u = unit.lower().replace(" ", "")
    m = re.search(r"(mg/dl|g/dl|mmol/l|%|ng/ml|iu/l|u/l)", u)

    return m.group(1) if m else None


def detect_status(value, ref):
    if value is None or not ref:
        return "Unknown"

    low, high = ref

    if low is not None and value < low:
        return "Low"

    if high is not None and value > high:
        return "High"

    return "Normal"


def normalize_lab_results(raw_results):
    normalized = []

    for r in raw_results:
        test = clean_name(r.get("test"))
        if not test:
            continue

        # value
        try:
            value = float(r.get("value"))
        except:
            continue

        unit = normalize_unit(r.get("unit"))
        ref = parse_range(r.get("reference_range"))
        status = detect_status(value, ref)

        normalized.append({
            "test": test,
            "value": value,
            "unit": unit,
            "reference_range": ref,
            "status": status,
            "abnormal": status in ("High", "Low")
        })

    return normalized

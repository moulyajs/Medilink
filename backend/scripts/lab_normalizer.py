# lab_normalizer.py
from test_normalizer import normalize_test

import re


def clean_name(name):

    name = name.strip()

    name = re.sub(r"\s{2,}", " ", name)

    return name.title()

def detect_status(value, ref):

    if value is None or not ref:
        return None

    low, high = ref

    margin = (high - low) * 0.05

    if value < low:
        return "low"

    if value > high:
        return "high"

    if abs(value - low) <= margin or abs(value - high) <= margin:
        return "borderline"

    return "normal"



def parse_range(text):

    if not text:
        return None

    # <130
    m1 = re.search(r"<\s*(\d+(\.\d+)?)", text)

    if m1:
        return [0.0, float(m1.group(1))]

    # >200
    m2 = re.search(r">\s*(\d+(\.\d+)?)", text)

    if m2:
        return [float(m2.group(1)), float("inf")]

    # 150 - 250
    m = re.search(r"(\d+(\.\d+)?)\s*[-–]\s*(\d+(\.\d+)?)", text)

    if not m:
        return None

    return [
        float(m.group(1)),
        float(m.group(3))
    ]


def normalize_unit(unit):

    if not unit:
        return None

    u = unit.lower().replace(" ", "")

    m = re.search(
    r"(mg/dl|g/dl|mmol/l|%|ng/ml|fl|pg|/cmm|million/cmm|microlu/ml)",
    u
)


    if m:
        return m.group(1)

    return None







def normalize_lab_results(raw_results):

    normalized = []

    for r in raw_results:

        test = normalize_test(r.get("test"))
        value = float(r.get("value"))

        raw_text = r.get("raw_text", "").lower()

        # ✅ Initialize ref FIRST
        ref = None

        # 1️⃣ Explicit H/L/Borderline
        status = detect_flag_from_text(raw_text)

        # 2️⃣ Range-based fallback
        if status is None:

            ref = parse_range(
                r.get("reference_range") or raw_text
            )

            status = detect_status(value, ref)

        # 3️⃣ Still unknown
        if status is None:
            status = "unknown"

        normalized.append({
            "test": test,
            "value": value,
            "unit": r.get("unit"),
            "reference_range": ref,
            "status": status
        })

    return normalized



def detect_flag_from_text(text):

    t = text.lower()

    if any(x in t for x in [" low", "(low)", " l "]):
        return "low"

    if any(x in t for x in [" high", "(high)", " h "]):
        return "high"

    if "borderline" in t:
        return "borderline"

    return None


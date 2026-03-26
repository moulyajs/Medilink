# lab_normalizer.py

def normalize_lab_results(raw_results):
    normalized = []

    for r in raw_results:
        normalized.append({
            "test": r.get("test"),
            "value": r.get("value"),
            "unit": r.get("unit"),
            "reference_range": r.get("reference_range"),
            "status": r.get("status"),
            "abnormal": r.get("abnormal", False),
            "date": r.get("date")
        })

    return normalized

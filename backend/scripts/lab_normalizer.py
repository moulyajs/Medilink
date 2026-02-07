import re

def normalize_lab_results(raw):
    out = []

    for r in raw:
        try:
            value = float(r["value"])
        except:
            continue

        out.append({
            "test": r["test"].title(),
            "value": value,
            "unit": r.get("unit"),
            "reference_range": None,
            "status": None
        })

    return out

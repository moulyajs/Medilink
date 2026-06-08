# ===============================
# CLEAN + NORMALIZE LAB RESULTS
# ===============================

IGNORE_TESTS = {
    "age", "age/sex", "sex", "pat id", "patient id",
    "bill no", "bill date", "name"
}


def normalize_lab_results(labs):
    cleaned = []
    seen = set()

    for lab in labs:
        test = lab.get("test", "").strip().lower()

        # --------------------------
        # ❌ REMOVE NON-LAB ROWS
        # --------------------------
        if not test:
            continue

        if any(x in test for x in IGNORE_TESTS):
            continue

        # --------------------------
        # (same test + same value)
        # --------------------------
        key = (test, lab.get("value"))

        if key in seen:
            continue

        seen.add(key)

        # --------------------------
        # ✅ STANDARDIZE OUTPUT
        # --------------------------
        cleaned.append({
            "test": lab.get("test"),
            "value": lab.get("value"),
            "unit": lab.get("unit"),
            "reference_range": lab.get("reference_range"),
            "status": lab.get("status"),
            "abnormal": lab.get("abnormal")
        })

    return cleaned
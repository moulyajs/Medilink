def classify_document(ocr_lines):
    """
    Robust medical document classification using strong signals.
    """
    text = " ".join([l["text"].lower() for l in ocr_lines])

    # --- STRONG LAB SIGNALS (highest priority) ---
    lab_keywords = [
        "reference value",
        "investigation",
        "result",
        "unit",
        "cbc",
        "complete blood count",
        "platelet",
        "hemoglobin",
        "wbc",
        "rbc",
        "differential"
    ]

    # --- STRONG DISCHARGE SIGNALS ---
    discharge_keywords = [
        "discharge summary",
        "final diagnosis",
        "hospital course",
        "admitted on",
        "discharged on"
    ]

    # --- PRESCRIPTION SIGNALS (lowest priority) ---
    prescription_keywords = [
        "inj.", "inj ", "tab.", "cap.", "syp.", "tablet", "capsule"
    ]

    if any(k in text for k in lab_keywords):
        return "LAB_REPORT"

    if any(k in text for k in discharge_keywords):
        return "DISCHARGE_SUMMARY"

    if any(k in text for k in prescription_keywords):
        return "PRESCRIPTION"

    return "UNKNOWN"

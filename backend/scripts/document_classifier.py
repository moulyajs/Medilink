def classify_document(ocr_lines):
    """
    STRICT medical document classification.
    Lab reports REQUIRE table-like structure.
    """

    lines = [l["text"].lower() for l in ocr_lines]
    text = " ".join(lines)

    # ---- STRONG STRUCTURAL LAB SIGNAL ----
    table_headers = {"test", "result", "unit", "units", "normal values", "reference range"}
    header_hits = sum(1 for l in lines if l.strip() in table_headers)

    numeric_rows = 0
    for i in range(len(lines) - 1):
        if any(c.isdigit() for c in lines[i]) and any(u in lines[i+1] for u in ["mg", "dl", "mmol", "%"]):
            numeric_rows += 1

    if header_hits >= 2 and numeric_rows >= 2:
        return "LAB_REPORT"

    # ---- DISCHARGE / H&P ----
    if any(k in text for k in [
        "history of present illness",
        "physical exam",
        "assessment and plan",
        "review of systems",
        "problem list"
    ]):
        return "CLINICAL_NOTE"

    # ---- PRESCRIPTION ----
    if any(k in text for k in ["tab.", "cap.", "inj.", "rx", "tablet", "capsule"]):
        return "PRESCRIPTION"

    return "UNKNOWN"

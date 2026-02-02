def generate_summary(entities, prescriptions=None, lab_results=None):
    summary = []

    # ---- Patient identity ----
    if "patient_name" in entities:
        summary.append(f"Patient {entities['patient_name']}")

    if "age" in entities and "gender" in entities:
        summary.append(f"is a {entities['age']}-year-old {entities['gender']}")

    if "hospital" in entities:
        summary.append(f"treated at {entities['hospital']}.")

    # ---- Medication summary (RAW, USER-REVIEW MODE) ----
    if prescriptions:
        meds = []

        for p in prescriptions:
            drug = p.get("drug")
            dose = p.get("dose")
            freq = p.get("frequency")

            parts = []

            if drug:
                parts.append(drug)

            if dose:
                parts.append(dose)

            if freq:
                parts.append(freq)

            if parts:
                meds.append(" ".join(parts))

        if meds:
            meds_text = "; ".join(meds)
            summary.append(f"Prescribed medications include {meds_text}.")

    # ---- Lab summary (unchanged) ----
    if lab_results:
        abnormal = []
        normal = []

        for r in lab_results:
            # Skip parent containers like "Complete Blood Count"
            if "children" in r:
                continue

            test = r.get("test")
            value = r.get("value")
            unit = r.get("unit")
            status = r.get("status")

            if not test or value is None:
                continue

            # Format: Hemoglobin (10.2 g/dl)
            value_text = f"{value}"
            if unit:
                value_text += f" {unit}"

            test_text = f"{test} ({value_text})"

            if status in ("high", "low"):
                abnormal.append(f"{test_text} is {status}")
            elif status == "normal":
                normal.append(test_text)

        if abnormal:
            summary.append("Abnormal lab findings include " + ", ".join(abnormal) + ".")

        if normal:
            summary.append("Other parameters are within normal range.")

    return " ".join(summary)

# clinical_summary.py


def generate_summary(entities, prescriptions=None, lab_results=None):
    summary = []
    # ---- Patient identity (robust) ----
    identity = []

    if "patient_name" in entities:
        identity.append(f"Patient {entities['patient_name']}")
    else:
        identity.append("The patient")

    if "age" in entities and "gender" in entities:
        identity.append(f"is a {entities['age']}-year-old {entities['gender']}")

    if "hospital" in entities:
        identity.append(f"treated at {entities['hospital']}.")

    summary.append(" ".join(identity))

    # ---- Medications ----
    if prescriptions:
        meds = []
        for p in prescriptions:
            parts = []
            if p.get("drug"):
                parts.append(p["drug"])
            if p.get("dose"):
                parts.append(p["dose"])
            if p.get("frequency"):
                parts.append(p["frequency"])
            if parts:
                meds.append(" ".join(parts))

        if meds:
            summary.append(
                "Prescribed medications include " + "; ".join(meds) + "."
            )

    # ---- Lab Results ----
    if lab_results:
        abnormal = []
        normal = []

        for r in lab_results:
            if "children" in r:
                continue

            test = r.get("test")
            value = r.get("value")
            unit = r.get("unit")
            status = r.get("status","").lower()

            if not test or value is None:
                continue

            value_text = f"{value}"
            if unit:
                value_text += f" {unit}"

            test_text = f"{test} ({value_text})"

            if status in ("high", "low"):
                abnormal.append(f"{test_text} is {status}")
            elif status == "normal":
                normal.append(test_text)

        if abnormal:
            summary.append(
                "Abnormal lab findings include " + ", ".join(abnormal) + "."
            )

        if normal:
            summary.append("Other parameters are within normal range.")

    return " ".join(summary)

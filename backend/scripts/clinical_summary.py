# clinical_summary.py

def generate_summary(entities, prescriptions=None, lab_results=None):
    summary = []

    # ---- Patient identity ----
    if "patient_name" in entities:
        summary.append(f"Patient {entities['patient_name']}")

    if "age" in entities and "gender" in entities:
        summary.append(f"is a {entities['age']}-year-old {entities['gender']}")

    if "hospital" in entities:
        summary.append(f"treated at {entities['hospital']}.")

    # ---- Medication summary ----
    if prescriptions:
        meds = []
        for p in prescriptions:
            drug = p.get("drug")
            dose = p.get("dose")
            freq = p.get("frequency")
            parts = [x for x in [drug, dose, freq] if x]
            if parts:
                meds.append(" ".join(parts))
        if meds:
            summary.append(f"Prescribed medications include: " + "; ".join(meds) + ".")

    # ---- Lab summary ----
    if lab_results:
        abnormal = []
        normal = []
        for r in lab_results:
            if "value" not in r or r["value"] is None:
                continue
            val = f"{r['value']}"
            if r.get("unit"):
                val += f" {r['unit']}"
            test_text = f"{r['test']} ({val})"
            if r.get("flag") in ("High", "Low", "Borderline"):
                abnormal.append(f"{test_text} is {r['flag']}")
            else:
                normal.append(test_text)
        if abnormal:
            summary.append("Abnormal lab findings include: " + ", ".join(abnormal) + ".")
        if normal:
            summary.append("Other parameters are within normal range.")

    return " ".join(summary)

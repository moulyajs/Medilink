# clinical_summary.py

def generate_summary(demographics, medicines, labs, clinical_facts):
    parts = []

    age = demographics.get("age")
    gender = demographics.get("gender")

    if age and gender:
        parts.append(f"Patient is a {age}-year-old {gender}.")
    else:
        parts.append("Patient details were not fully available.")

    # Symptoms
    symptoms = clinical_facts.get("symptoms", [])
    clean_symptoms = [
        s for s in symptoms
        if len(s) < 80 and not s.lower().startswith(("report", "follow", "investigation"))
    ]

    if clean_symptoms:
        parts.append(
            "Reported symptoms include " +
            ", ".join({s.lstrip('- ').strip() for s in clean_symptoms}) + "."
        )

    # Diagnosis
    diagnoses = clinical_facts.get("diagnoses", [])
    if diagnoses:
        parts.append("Provisional diagnosis is " + "; ".join(diagnoses) + ".")

    # Medicines
    if medicines:
        meds = []
        for m in medicines:
            meds.append(f"{m['drug']} ({m['dose']})")
        parts.append("Prescribed medications include " + ", ".join(meds) + ".")

    # Labs
    if labs:
        abnormal = [l for l in labs if l.get("flag") == "abnormal"]
        if abnormal:
            parts.append("Some laboratory values were abnormal and require follow-up.")

    if not medicines and not diagnoses:
        parts.append("Clinical correlation and follow-up are advised.")

    return " ".join(parts)

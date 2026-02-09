# clinical_summary.py
# clinical_summary.py
# scripts/clinical_summary.py
from phi3_summarizer import generate_phi3_summary


def generate_summary(demographics, medicines, labs, clinical_facts):
    """
    Generate a grounded clinical summary using Phi-3.
    """

    patient_block = {
        "Name": demographics.get("patient_name", "Unknown"),
        "Age": demographics.get("age", "Unknown"),
        "Gender": demographics.get("gender", "Unknown"),
        "Hospital": demographics.get("hospital", "Unknown")
    }

    meds_block = [
        f"{m.get('drug')} | Dose: {m.get('dose','N/A')} | Frequency: {m.get('frequency','N/A')}"
        for m in medicines
    ]

    abnormal_labs = [
        f"{l.get('test')} = {l.get('value')} {l.get('unit','')} (Ref: {l.get('reference_range','N/A')})"
        for l in labs
        if l.get("abnormal") or l.get("status") in ("High", "Low")
    ]

    facts_block = clinical_facts.get("abnormal_findings", [])

    prompt = f"""
You are a clinical documentation assistant.

Write a clear, factual, patient-safe clinical summary using ONLY the data provided below.
DO NOT invent diseases, symptoms, or diagnoses.
If information is missing, state it as unavailable.

PATIENT DETAILS:
{patient_block}

PRESCRIBED MEDICINES:
{meds_block if meds_block else "None"}

ABNORMAL LAB RESULTS:
{abnormal_labs if abnormal_labs else "None"}

CLINICAL FACTS:
{facts_block if facts_block else "None"}

Write the summary in 5–7 sentences.
Avoid speculative language.
"""

    return generate_phi3_summary(prompt)

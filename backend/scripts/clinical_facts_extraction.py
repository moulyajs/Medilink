# scripts/clinical_facts_extraction.py
import re

DIAGNOSIS_KEYWORDS = [
    "syndrome", "disease", "arthritis", "lupus", "anemia",
    "leukopenia", "lymphoma", "sjogren", "sle"
]

SYMPTOM_KEYWORDS = [
    "pain", "weakness", "fatigue", "headache", "nausea",
    "vomiting", "weight loss", "night sweats", "fever",
    "dry mouth", "dry eye", "lightheadedness"
]

ABNORMAL_KEYWORDS = [
    "decreased", "elevated", "low", "high", "positive", "negative"
]

def extract_clinical_facts(text):
    text_lower = text.lower()
    lines = text.split("\n")

    diagnoses = set()
    symptoms = set()
    abnormalities = set()

    for line in lines:
        l = line.lower()

        # ---- Diagnoses ----
        for d in DIAGNOSIS_KEYWORDS:
            if d in l:
                diagnoses.add(line.strip())

        # ---- Symptoms ----
        for s in SYMPTOM_KEYWORDS:
            if s in l:
                symptoms.add(line.strip())

        # ---- Abnormal findings ----
        if any(k in l for k in ABNORMAL_KEYWORDS):
            if re.search(r"\d", l):
                abnormalities.add(line.strip())

    return {
        "diagnoses": list(diagnoses),
        "symptoms": list(symptoms),
        "abnormal_findings": list(abnormalities)
    }

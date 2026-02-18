# scripts/clinical_facts_extraction.py
import re

ABNORMAL_MARKERS = [
    "high", "low", "positive", "negative", "reactive", "non reactive", "abnormal"
]

IGNORE_PHRASES = [
    "reference", "range", "interpretation",
    "associated with", "may be", "can be",
    "recommended", "should be", "used to",
    "patients with", "studies suggest",
    "evaluation of", "treatment of"
]


def is_patient_specific(line):
    """
    Filters out textbook explanations and lab methodology text.
    """
    if len(line) > 120:
        return False

    l = line.lower()

    if any(p in l for p in IGNORE_PHRASES):
        return False

    # must contain a number OR explicit result
    return bool(re.search(r"\d", l) or any(k in l for k in ABNORMAL_MARKERS))


def extract_clinical_facts(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    abnormal_findings = set()

    for line in lines:
        l = line.lower()

        if any(k in l for k in ABNORMAL_MARKERS):
            if is_patient_specific(line):
                abnormal_findings.add(line)

    return {
        # lab reports should NOT infer diagnoses or symptoms
        "diagnoses": [],
        "symptoms": [],
        "abnormal_findings": sorted(abnormal_findings)
    }

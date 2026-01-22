# scripts/prescription_validator.py

import re
from difflib import SequenceMatcher

# -------------------------------------------------
# Canonical Drug Registry (expand over time)
# -------------------------------------------------
DRUG_REGISTRY = {
    "amphotericin b": {
        "route": "iv",
        "allowed_units": ["mg", "vial"],
        "forbidden_units": ["g"],
        "high_risk": True,
        "max_safe_dose_mg": 150
    }
}

# -------------------------------------------------
# Normalization helpers
# -------------------------------------------------
def normalize_name(name):
    if not name:
        return ""
    name = name.lower()
    name = name.replace(".", "").replace(",", "")
    name = " ".join(name.split())
    return name

# -------------------------------------------------
# Tokenization (NO stop-word hacks)
# -------------------------------------------------
def tokenize(name):
    """
    Break name into meaningful tokens.
    Keeps logic generic and OCR-robust.
    """
    return [
        t for t in normalize_name(name).split()
        if len(t) >= 4
    ]

def token_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# -------------------------------------------------
# Drug matching (TOKEN-DOMINANT MATCHING)
# -------------------------------------------------
def match_drug(ocr_name):
    ocr_tokens = tokenize(ocr_name)

    best_match = None
    best_score = 0.0

    for canonical in DRUG_REGISTRY:
        canon_tokens = tokenize(canonical)

        for ocr_t in ocr_tokens:
            for canon_t in canon_tokens:
                score = token_similarity(ocr_t, canon_t)
                if score > best_score:
                    best_score = score
                    best_match = canonical

    canon_token_count = len(tokenize(best_match)) if best_match else 0
    if best_score >= 0.75:
        return best_match, best_score
    if canon_token_count == 1 and best_score >= 0.7:
        return best_match, best_score
    elif best_score >= 0.6:
        return None, best_score   # uncertain match
    else:
        return None, 0.0          # unknown drug

# -------------------------------------------------
# Dose parsing
# -------------------------------------------------
def parse_dose(dose_text):
    if not dose_text:
        return None, None

    m = re.search(
        r"(\d+(\.\d+)?)\s*(mg|g|ml|mcg|iu)",
        dose_text.lower()
    )
    if not m:
        return None, None

    return float(m.group(1)), m.group(3)

# -------------------------------------------------
# Dose safety validation
# -------------------------------------------------
def validate_dose(drug_info, dose_value, unit):
    warnings = []

    if unit in drug_info.get("forbidden_units", []):
        warnings.append("unit_not_allowed_for_drug")

    if drug_info.get("route") == "iv" and unit == "g":
        warnings.append("iv_drug_in_grams")

    max_dose = drug_info.get("max_safe_dose_mg")
    if unit == "mg" and max_dose and dose_value > max_dose:
        warnings.append("dose_exceeds_safe_limit")

    return warnings

# -------------------------------------------------
# Main validation entry point
# -------------------------------------------------
def validate_prescriptions(prescriptions):
    validated = []

    for p in prescriptions:
        original_name = p.get("drug") or p.get("name")
        dose_text = p.get("dose") or p.get("dosage")

        entry = {
            "drug_original": original_name,
            "drug_normalized": None,
            "dose_raw": dose_text,
            "frequency": p.get("frequency"),
            "status": "ok",
            "warnings": [],
            "confidence": 1.0
        }

        # ---- Drug identification ----
        canonical, score = match_drug(original_name)

        if not canonical:
            entry["status"] = "uncertain_drug"
            entry["confidence"] = score
            validated.append(entry)
            continue

        entry["drug_normalized"] = canonical
        entry["confidence"] = score
        drug_info = DRUG_REGISTRY[canonical]

        # ---- Dose validation ----
        dose_value, unit = parse_dose(dose_text)

        if unit:
            warnings = validate_dose(drug_info, dose_value, unit)
            if warnings:
                entry["status"] = "unsafe_ocr"
                entry["warnings"].extend(warnings)
                entry["confidence"] *= 0.5
        else:
            entry["warnings"].append("dose_unparseable")
            entry["confidence"] *= 0.7

        validated.append(entry)

    return validated

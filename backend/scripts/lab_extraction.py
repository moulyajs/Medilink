#lab_extraction.py
#lab_extraction.py
# lab_extraction.py
import re


NUMBER = re.compile(r"^\d+(\.\d+)?$")
RANGE = re.compile(r"^(\d+(\.\d+)?)\s*[-–]\s*(\d+(\.\d+)?)$")
LT = re.compile(r"^<\s*(\d+(\.\d+)?)$")
UNIT = re.compile(
    r"(g/dl|mg/dl|mmol/l|ng/ml|%|/cmm|iu/l|u/l|pg|fl)",
    re.I
)

# words that should NEVER appear in test names
BAD_WORDS = {
    "process", "method", "calculated", "derived",
    "impedance", "colorimetric", "chemiluminescence",
    "electrical", "binding", "reaction",
    "page", "report", "final", "status",
    "laboratory", "pathology", "immunoassay",
    "test", "unit", "result", "range", "interval",
    "serum", "plasma", "blood", "urine"
}

# words that SHOULD appear in real tests
GOOD_HINTS = {
    "hemoglobin", "rbc", "wbc", "platelet",
    "neutrophil", "lymphocyte", "monocyte", "eosinophil",
    "bilirubin", "sgpt", "sgot", "alt", "ast",
    "urea", "creatinine", "uric", "calcium",
    "cholesterol", "hdl", "ldl", "vldl",
    "triglyceride", "protein", "albumin", "globulin",
    "tsh", "thyroid", "vitamin", "iron", "ferritin",
    "glucose", "hba1c", "microalbumin", "psa"
}


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def looks_like_real_test(name):
    lname = name.lower()

    # block bad words anywhere
    for b in BAD_WORDS:
        if b in lname:
            return False

    # must contain at least one medical hint
    return any(h in lname for h in GOOD_HINTS)


def reference_is_reasonable(value, ref):
    if not ref:
        return True

    try:
        val = float(value)
    except:
        return False

    m = RANGE.match(ref)
    if m:
        low, high = float(m.group(1)), float(m.group(3))

        # % reference but absolute value
        if high <= 100 and val > 500:
            return False

    return True


def extract_lab_results(lines):

    tokens = [clean(l["text"]) for l in lines]
    results = []

    i = 0
    n = len(tokens)

    while i < n:

        t = tokens[i]

        # candidate test name
        if (
            len(t) >= 4
            and re.match(r"^[A-Za-z][A-Za-z ()/-]+$", t)
            and looks_like_real_test(t)
        ):

            test = t
            value = None
            unit = None
            ref = None

            for j in range(i + 1, min(i + 8, n)):
                w = tokens[j]

                if not value and NUMBER.match(w):
                    value = w
                    continue

                if not unit and UNIT.search(w):
                    unit = w
                    continue

                if not ref and (RANGE.match(w) or LT.match(w)):
                    ref = w
                    continue

            if value and reference_is_reasonable(value, ref):
                results.append({
                    "test": test,
                    "value": float(value),
                    "unit": unit,
                    "reference_range": ref
                })

        i += 1

    return results

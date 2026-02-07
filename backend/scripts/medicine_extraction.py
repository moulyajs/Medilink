# medicine_extraction.py

import re

DOSAGE_PATTERN = re.compile(
    r"(?P<drug>(tablet|tab|capsule|cap|syrup)?\s*[A-Za-z][A-Za-z\s\+\-]{2,})"
    r"\s+(?P<dose>\d+(\.\d+)?\s*(mg|ml|mcg|g|iu))",
    re.IGNORECASE
)

BLACKLIST = [
    "hospital", "clinic", "address", "phone", "doctor",
    "registration", "patient", "date", "age", "gender",
    "diagnosis", "investigation", "advice", "instruction",
    "warning", "follow", "signature"
]


def extract_medicines(lines):
    medicines = []

    for line in lines:
        text = line["text"].strip()

        lower = text.lower()
        if any(b in lower for b in BLACKLIST):
            continue

        match = DOSAGE_PATTERN.search(text)
        if not match:
            continue

        drug = match.group("drug")
        dose = match.group("dose")

        # Clean drug name
        drug = re.sub(r"^(tablet|tab|capsule|cap|syrup)\s*", "", drug, flags=re.I)
        drug = re.sub(r"\s+", " ", drug).strip().title()

        medicines.append({
            "drug": drug,
            "dose": dose,
            "frequency": None
        })

    return medicines

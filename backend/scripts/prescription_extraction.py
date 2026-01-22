import re

def extract_prescriptions(ocr_lines):
    medicines = []
    i = 0

    while i < len(ocr_lines):
        text = ocr_lines[i]["text"]
        text_lower = text.lower()

        # --- DRUG ANCHOR FIRST (VERY IMPORTANT) ---
        drug_anchor = re.search(
            r"(inj\.?|tab\.?|cap\.?|syp\.?)\s*([A-Za-z][A-Za-z\s]{3,})",
            text,
            re.I
        )

        if drug_anchor:
            medicine = {
                "raw_lines": [text],
                "drug": drug_anchor.group(2).strip()
            }

            # Look ahead for dose & frequency
            for j in range(i + 1, min(i + 4, len(ocr_lines))):
                next_text = ocr_lines[j]["text"]
                medicine["raw_lines"].append(next_text)

                dose = re.search(
                    r"(\d+(\.\d+)?\s*(mg|g|ml|mcg|iu))",
                    next_text,
                    re.I
                )
                freq = re.search(
                    r"(once|twice|daily|/day|bd|od|tds|vials)",
                    next_text,
                    re.I
                )

                if dose:
                    medicine["dose"] = dose.group(1)
                if freq:
                    medicine["frequency"] = freq.group(1)

            medicines.append(medicine)
            i += 3
            continue

        # --- NOW APPLY SKIP FILTERS (TOKEN-BASED) ---
        skip_markers = [
            "mr.", "ms.", "mrs.", "yrs", "year", "male", "female",
            "dr.", "hospital", "road", "tel", "www", "managed by",
            "uhid", "date", "doa"
        ]

        if any(marker in text_lower for marker in skip_markers):
            i += 1
            continue

        i += 1

    return medicines

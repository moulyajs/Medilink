import re


DOSE_PATTERN = r"(\d+\s*(mg|g|ml|mcg|iu))"
FREQ_PATTERN = r"(od|bd|tds|qid|once|twice|day|daily|vial|vials)"


def extract_prescriptions(ocr_lines):

    medicines = []

    i = 0

    while i < len(ocr_lines):

        text = ocr_lines[i]["text"]
        low = text.lower()

        # -----------------------------
        # Detect medicine anchor
        # -----------------------------
        if re.search(r"\b(inj|tab|cap|syp)\.?\b", low):

            med = {
                "raw_lines": [text],
                "drug": re.sub(r"\b(inj|tab|cap|syp)\.?\b", "", text, flags=re.I).strip()
            }

            # -----------------------------
            # Look next 3 lines (noise safe)
            # -----------------------------
            for j in range(i+1, min(i+4, len(ocr_lines))):

                nxt = ocr_lines[j]["text"]
                low2 = nxt.lower()

                med["raw_lines"].append(nxt)

                # Loose dose match
                d = re.search(DOSE_PATTERN, low2)

                if d:
                    med["dose"] = d.group(1)

                # Loose frequency match
                f = re.search(FREQ_PATTERN, low2)

                if f:
                    med["frequency"] = f.group(1)

                # Special: vials/day OCR noise
                if "vial" in low2 and "day" in low2:
                    med["frequency"] = "vials/day"

            medicines.append(med)

            i += 3
            continue

        i += 1

    return medicines

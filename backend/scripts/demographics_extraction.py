
#demograhics_extraction.py
import re

def extract_demographics(ocr_lines, doc_type):
    """
    Extract patient identity safely using OCR line structure.
    """
    data = {}

    # Look only in the first ~20 lines (identity is always early)
    candidate_lines = ocr_lines[:20]

    for i, line in enumerate(candidate_lines):
        text = line["text"]

        # --- Patient Name ---
        if "mr" in text.lower() or "ms" in text.lower():
            # Avoid picking doctor names
            if "dr" not in text.lower():
                name = re.sub(r"(mr|ms|mrs)\.?\s*", "", text, flags=re.I)
                if len(name.split()) >= 2:
                    data["patient_name"] = name.strip()

        # --- Age ---
        age_match = re.search(r"(\d{1,3})\s*(yrs?|years?)", text, re.I)
        if age_match:
            data["age"] = age_match.group(1)

        # --- Gender ---
        if "male" in text.lower():
            data["gender"] = "Male"
        elif "female" in text.lower():
            data["gender"] = "Female"

        # --- Patient IDs ---
        if "pid" in text.lower():
            pid = re.search(r"pid\s*[:\-]?\s*(\w+)", text, re.I)
            if pid:
                data["pid"] = pid.group(1)

        if "uhid" in text.lower():
            uhid = re.search(r"uhid\s*[:\-]?\s*(\w+)", text, re.I)
            if uhid:
                data["uhid"] = uhid.group(1)

        if re.search(r"\bip\s*no\b", text, re.I):
            ip = re.search(r"ip\s*no?\s*[:\-]?\s*([\w/]+)", text, re.I)
            if ip:
                data["ip_no"] = ip.group(1)


    return data

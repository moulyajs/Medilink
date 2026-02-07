import re

def extract_demographics(ocr_lines, doc_type):
    data = {}

    for l in ocr_lines[:25]:
        text = l["text"]

        # Name (label-based only)
        if ":" in text and any(k in text.lower() for k in ["patient name", "name"]):
            val = text.split(":", 1)[1].strip()
            if len(val.split()) >= 2:
                data["patient_name"] = val

        # Age
        m = re.search(r"(\d{1,3})\s*(yrs?|years?)", text, re.I)
        if m:
            data["age"] = m.group(1)

        # Gender
        if re.search(r"\bmale\b", text, re.I):
            data["gender"] = "Male"
        elif re.search(r"\bfemale\b", text, re.I):
            data["gender"] = "Female"

    return data

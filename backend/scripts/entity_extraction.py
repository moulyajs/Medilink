import re

def extract_entities(text, top_lines):
    data = {}

    # -------- Patient Name --------
    name = re.search(r"(Mr|Mrs|Ms)\.?\s([A-Za-z ]+)", text)
    if name:
        data["patient_name"] = name.group(2).strip()

    # -------- Age & Gender --------
    age_gender = re.search(
        r"(\d+)\s*Yrs\s*/\s*(Male|Female)",
        text,
        re.IGNORECASE
    )
    if age_gender:
        data["age"] = age_gender.group(1)
        data["gender"] = age_gender.group(2) 

    # -------- Patient ID --------
    pid = re.search(
        r"(IP|UHID)\s*No?\s*:?\s*([\w/]+)",
        text,
        re.IGNORECASE
    )
    if pid:
        data["patient_id"] = pid.group(2)

    # -------- Hospital Name (LINE-BASED) --------
    hospital_pattern = re.compile(
        r"([A-Z][A-Za-z\s]+(?:Hospital|Medical Center|Clinic|Healthcare|Institute))"
    )

    for line in top_lines:
        match = hospital_pattern.search(line)
        if match:
            data["hospital"] = match.group(1).strip()
            break

    return data

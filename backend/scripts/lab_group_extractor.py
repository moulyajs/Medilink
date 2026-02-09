import re

def is_group_header(text):
    text = text.strip()

    if len(text) < 4:
        return False

    # Headers should not contain numbers
    if re.search(r"\d", text):
        return False

    keywords = [
        "PROFILE", "TEST", "PANEL",
        "COUNT", "FUNCTION", "ASSAY",
        "EXAMINATION"
    ]

    if any(k in text.upper() for k in keywords):
        return True

    # ALL CAPS short lines are usually headers
    if text.isupper() and len(text.split()) <= 6:
        return True

    return False


def extract_lab_groups(lines):
    groups = {}
    current_group = None

    for line in lines:
        text = line["text"].strip()

        if is_group_header(text):
            current_group = text.title()
            groups[current_group] = []
            continue

        if current_group:
            groups[current_group].append(text)

    return groups

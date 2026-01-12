# scripts/medicine_extraction.py
import re

def extract_medicines(text):
    """
    Phase-1 safe dynamic medicine extraction.
    Works even if OCR text is one long block.
    """
    medicine_list = []

    # Step 1: Split text by medicine indicators
    indicators = ["Inj.", "Tab.", "Cap.", "Syp.", "Tablet", "Syrup"]
    pattern_split = "(" + "|".join(re.escape(ind) for ind in indicators) + ")"
    chunks = re.split(pattern_split, text)

    # Step 2: Process each chunk that looks like a medicine entry
    for i in range(1, len(chunks), 2):
        # Combine indicator + text
        chunk = chunks[i] + " " + chunks[i+1] if i+1 < len(chunks) else chunks[i]
        chunk = chunk.strip()

        # Skip non-medicine chunks
        skip_words = ["Dr", "Hospital", "IP", "UHID", "EICU", "Managed", "Tel", "www"]
        if any(skip in chunk for skip in skip_words):
            continue

        # Regex to extract name, dosage, frequency
        match = re.search(
            r'(?P<name>[A-Za-z\s]{3,})\s*(?P<dosage>\d+mg|\d+g)?\s*(?P<freq>TDS|BD|OD|/day|per day|once daily|twice daily)?',
            chunk
        )
        if match:
            name = match.group("name").strip()
            dosage = match.group("dosage") if match.group("dosage") else ""
            freq = match.group("freq") if match.group("freq") else ""
            medicine_list.append({"name": name, "dosage": dosage, "frequency": freq})

    return medicine_list

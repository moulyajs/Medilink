# medicine_extraction.py
import re

def extract_medicines(ocr_lines):
    """
    Extract medicines from OCR lines of prescription documents.
    Returns a list of dicts: {"drug": ..., "dose": ..., "frequency": ...}
    """
    medicine_list = []

    # Combine all lines into one text
    text = " ".join([l["text"] for l in ocr_lines])

    # Indicators for medicines
    indicators = ["Inj.", "Tab.", "Cap.", "Syp.", "Tablet", "Syrup", "Cough Syrup"]
    pattern_split = "(" + "|".join(re.escape(ind) for ind in indicators) + ")"
    chunks = re.split(pattern_split, text)

    for i in range(1, len(chunks), 2):
        chunk = chunks[i] + " " + chunks[i+1] if i+1 < len(chunks) else chunks[i]
        chunk = re.sub(r"\s+", " ", chunk.strip())

        # Remove admin text
        chunk = re.split(r"\b(Dr\.|Hospital|Tel|www|Managed|UHID|IP No|Address|Date)\b", chunk, flags=re.I)[0]

        # Dosage
        dosage_match = re.search(r"\d+\s*(mg|g|ml|IU)", chunk, re.I)
        dosage = dosage_match.group(0) if dosage_match else ""

        # Frequency
        freq_match = re.search(r"(?:b?vials?/day|/day|OD|BD|TDS|once daily|twice daily|three times daily|night)", chunk, re.I)
        frequency = freq_match.group(0) if freq_match else ""

        # Medicine name
        name_match = re.search(r"(Tablet|Tab\.|Capsule|Cap\.|Injection|Inj\.|Syrup|Syp\.|Cough Syrup)\s+([A-Za-z][A-Za-z\s\+\-]{3,})", chunk, re.I)

        if name_match:
            name = name_match.group(2)
            name = re.sub(r"\b(song|dose|daily)\b", "", name, flags=re.I)
            name = re.sub(r"\s+", " ", name).strip()

            medicine_list.append({
                "drug": name,
                "dose": dosage,
                "frequency": frequency
            })

    return medicine_list

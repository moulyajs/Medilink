import re

def extract_medicines(text):
    medicine_list = []

    indicators = ["Inj.", "Tab.", "Cap.", "Syp.", "Tablet", "Syrup"]
    pattern_split = "(" + "|".join(re.escape(ind) for ind in indicators) + ")"
    chunks = re.split(pattern_split, text)

    for i in range(1, len(chunks), 2):
        chunk = chunks[i] + " " + chunks[i+1] if i+1 < len(chunks) else chunks[i]
        chunk = re.sub(r"\s+", " ", chunk.strip())

        # ✂️ CUT OFF admin text instead of skipping
        chunk = re.split(
            r"\b(Dr\.|Hospital|Tel|www|Managed|UHID|IP No)\b",
            chunk,
            flags=re.I
        )[0]

        # -------- Dosage (anywhere) --------
        dosage_match = re.search(r"\d+\s*(mg|g|ml|IU)", chunk, re.I)
        dosage = dosage_match.group(0) if dosage_match else ""

        # -------- Frequency (OCR tolerant) --------
        freq_match = re.search(
            r"(?:b?vials?/day|/day|OD|BD|TDS|once daily|twice daily)",
            chunk,
            re.I
        )
        frequency = freq_match.group(0) if freq_match else ""

        # -------- Medicine name --------
        name_match = re.search(
            r"(Inj\.|Tab\.|Cap\.|Syp\.)\s*([A-Za-z][A-Za-z\s\-]{5,})",
            chunk
        )

        if name_match:
            name = name_match.group(2)

            # Clean OCR garbage
            name = re.sub(r"\b(song|dose|daily)\b", "", name, flags=re.I)
            name = re.sub(r"\s+", " ", name).strip()

            medicine_list.append({
                "name": name,
                "dosage": dosage,
                "frequency": frequency
            })

    return medicine_list

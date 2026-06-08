import numpy as np


def parse_table_from_ocr(ocr_result):
    words = []

    # Extract all words with positions
    for line in ocr_result[0]:
        bbox = line[0]
        text = line[1][0]

        x = (bbox[0][0] + bbox[2][0]) / 2
        y = (bbox[0][1] + bbox[2][1]) / 2

        words.append({
            "text": text,
            "x": x,
            "y": y
        })

    if not words:
        return []

 
    # Step 1: Cluster rows by Y

    words.sort(key=lambda w: w["y"])

    rows = []
    current_row = [words[0]]

    for w in words[1:]:
        if abs(w["y"] - current_row[-1]["y"]) < 15:
            current_row.append(w)
        else:
            rows.append(current_row)
            current_row = [w]

    rows.append(current_row)

    # -----------------------------
    # Step 2: Sort each row by X
    # -----------------------------
    structured = []

    for row in rows:
        row = sorted(row, key=lambda w: w["x"])

        # Keep columns separate
        structured.append({
            "columns": [w["text"] for w in row],
            "text": " | ".join(w["text"] for w in row)
        })

    return structured
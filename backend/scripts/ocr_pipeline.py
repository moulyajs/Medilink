import re
from paddocr import run_ocr


# -----------------------------
# Helpers
# -----------------------------

def clean_text(text):

    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text


# -----------------------------
# Row grouping
# -----------------------------

def group_blocks_by_rows(blocks, y_threshold=18):

    rows = []

    for b in blocks:

        if b["bbox"] is None:
            continue

        pts = list(b["bbox"])
        y_center = sum(p[1] for p in pts) / 4

        placed = False

        for row in rows:

            if abs(row["y"] - y_center) <= y_threshold:
                row["blocks"].append(b)
                placed = True
                break

        if not placed:
            rows.append({
                "y": y_center,
                "blocks": [b]
            })

    rows.sort(key=lambda r: r["y"])

    for row in rows:
        row["blocks"].sort(
            key=lambda b: min(p[0] for p in b["bbox"])
        )

    return rows



# -----------------------------
# Main OCR
# -----------------------------

def ocr_process(image_path, min_conf=0.6):

    blocks = run_ocr(image_path)

    blocks = [
        b for b in blocks
        if b["confidence"] >= min_conf
    ]

    rows = group_blocks_by_rows(blocks)

    lines = []

    line_no = 1

    for row in rows:

        # FULL FREE TEXT LINE
        text = " ".join(
            b["text"] for b in row["blocks"]
        )

        lines.append({
            "line_no": line_no,
            "text": text,
            "confidence": round(
                sum(b["confidence"] for b in row["blocks"]) / len(row["blocks"]),
                2
            ),
            "bbox": row["blocks"][0]["bbox"]
        })

        line_no += 1


    raw_text = "\n".join(l["text"] for l in lines)

    return {
        "lines": lines,
        "raw_text": raw_text,
        "blocks": blocks
    }

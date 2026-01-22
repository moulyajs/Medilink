import re
from paddocr import run_ocr

def clean_text_with_lines(texts, scores, threshold=0.6):
    structured_lines = []
    seen = set()
    line_no = 1

    for text, score in zip(texts, scores):
        if score < threshold:
            continue

        text = text.strip()
        if len(text) <= 2:
            continue

        # VERY LIGHT CLEANING (do NOT destroy symbols)
        text = re.sub(r"\s+", " ", text)

        if text in seen:
            continue
        seen.add(text)

        structured_lines.append({
            "line_no": line_no,
            "text": text,
            "score": round(float(score), 2)
        })
        line_no += 1

    top_lines = [l["text"] for l in structured_lines[:5]]
    raw_text = " ".join([l["text"] for l in structured_lines])

    return {
        "lines": structured_lines,
        "raw_text": raw_text,
        "top_lines": top_lines
    }

def ocr_process(image_path):
    texts, scores = run_ocr(image_path)
    return clean_text_with_lines(texts, scores)

import re
from paddocr import run_ocr

def clean_text_with_lines(texts, scores, threshold=0.7):
    """
    Returns:
    - full_clean_text
    - top_lines (for hospital extraction)
    """

    # Step 1: Confidence filtering
    lines = [
        text.strip()
        for text, score in zip(texts, scores)
        if score >= threshold and len(text.strip()) > 2
    ]

    # Step 2: Remove duplicates but keep order
    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)

    # Step 3: Clean characters
    cleaned_lines = []
    for line in unique_lines:
        line = re.sub(r"[^a-zA-Z0-9:/.,\- ]+", " ", line)
        line = re.sub(r"\s+", " ", line)
        cleaned_lines.append(line.strip())

    # Step 4: Top 5 lines (usually hospital info)
    top_lines = cleaned_lines[:5]

    full_text = " ".join(cleaned_lines)

    return full_text, top_lines


def ocr_process(image_path):
    texts, scores = run_ocr(image_path)
    return clean_text_with_lines(texts, scores)

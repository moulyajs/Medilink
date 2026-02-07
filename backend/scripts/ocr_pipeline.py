# ocr_pipeline.py

import re
from paddocr import run_ocr
from pdf2image import convert_from_path
import tempfile
from pathlib import Path
import sys
from document_classifier import classify_document


# -----------------------------
# Document type detection
# -----------------------------
# ocr_pipeline.py

def detect_document_type(text):
    text = text.lower()

    lab_keywords = [
        "lipid profile",
        "cholesterol",
        "hdl",
        "ldl",
        "vldl",
        "triglycerides",
        "normal values",
        "reference",
        "mg/dl",
        "upto",
        "investigation",
        "test result"
    ]

    prescription_keywords = [
        "tab.", "inj.", "cap.", "syp.", "rx", "tablet", "capsule"
    ]

    # ⚠️ LAB MUST BE CHECKED FIRST
    if any(k in text for k in lab_keywords):
        return "lab_report"

    if any(k in text for k in prescription_keywords):
        return "prescription"

    return "unknown"

# -----------------------------
# Clean OCR output
# -----------------------------
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

# -----------------------------
# OCR process (images + PDFs)
# -----------------------------
def ocr_process(file_path):
    """
    Supports both images (jpg/png) and PDF (multi-page)
    Returns OCR structured lines, raw text, and document type.
    """
    all_texts = []
    all_scores = []

    # Optional: specify poppler path for Windows
    poppler_path = None
    if sys.platform.startswith("win"):
        # Update this path to your Poppler bin folder
        poppler_path = r"C:\Users\Najmus Seher\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

    # PDF input
    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path, poppler_path=poppler_path)
        for idx, page in enumerate(pages, 1):
            # Create temporary path for each page
            tmp_file = Path(tempfile.gettempdir()) / f"ocr_page_{idx}.png"
            page.save(tmp_file, "PNG")  # Save page as image
            texts, scores = run_ocr(str(tmp_file))
            all_texts.extend(texts)
            all_scores.extend(scores)
            # Delete temp image after OCR
            tmp_file.unlink(missing_ok=True)
    else:
        # Image input
        texts, scores = run_ocr(file_path)
        all_texts = texts
        all_scores = scores

    cleaned = clean_text_with_lines(all_texts, all_scores)
    doc_type = classify_document(cleaned["lines"]).lower()
    return cleaned["lines"], cleaned["top_lines"], doc_type

from document_classifier import classify_document
from date_extraction import extract_date
from tesseract_ocr import run_ocr
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
import re
import sys

DOSE_REGEX = r"\b\d{1,4}\s*(mg|ml|g|mcg|iu)\b"
FREQ_REGEX = r"\b(od|bd|tds|qid|hs|once|twice|daily|day|vial|vials)\b"
FORM_REGEX = r"\b(inj|tab|cap|iv|syp|syr|vial|amp)\b"


# --------------------------------------------------
# Clean OCR text
# --------------------------------------------------
def clean_text_with_lines(texts, scores, threshold=0.6):
    lines = []
    seen = set()
    line_no = 1

    for t, s in zip(texts, scores):
        if s < threshold:
            continue

        t = re.sub(r"\s+", " ", t.strip())

        if len(t) < 3 or t in seen:
            continue

        seen.add(t)
        lines.append({
            "line_no": line_no,
            "text": t,
            "score": round(float(s), 2)
        })
        line_no += 1

    return lines, [l["text"] for l in lines[:5]]


# --------------------------------------------------
# Prescription inference (unchanged)
# --------------------------------------------------
def infer_prescription(lines):
    score = 0
    for l in lines:
        t = l["text"].lower()
        if re.search(DOSE_REGEX, t):
            score += 1
        if re.search(FORM_REGEX, t):
            score += 1
        if re.search(FREQ_REGEX, t):
            score += 1
    return score >= 2


# --------------------------------------------------
# 🔥 FIXED OCR PROCESS (PAGE-WISE)
# --------------------------------------------------
def ocr_process(file_path):
    poppler_path = None
    if sys.platform.startswith("win"):
        poppler_path = r"C:\Users\Najmus Seher\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

    pages_data = []

    # -------- PDF INPUT --------
    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path, poppler_path=poppler_path)

        for i, page in enumerate(pages):
            tmp = Path(tempfile.gettempdir()) / f"page_{i}.png"
            page.save(tmp, "PNG")

            texts, scores = run_ocr(str(tmp))
            lines, top_lines = clean_text_with_lines(texts, scores)

            doc_type = classify_document(lines)
            date = extract_date(lines)

            # Handwritten prescription fallback
            if doc_type == "unknown" and infer_prescription(lines):
                print(f"⚠️ Page {i+1}: overridden to PRESCRIPTION (handwritten)")
                doc_type = "PRESCRIPTION"

            pages_data.append({
                "page_no": i + 1,
                "lines": lines,
                "top_lines": top_lines,
                "doc_type": doc_type,
                "date": date
            })

            tmp.unlink(missing_ok=True)

    # -------- IMAGE INPUT --------
    else:
        texts, scores = run_ocr(file_path)
        print("\n===== RAW OCR =====")
        for t, s in zip(texts, scores):
            print(f"{s:.2f} -> {t}")
        print("===================\n")

        lines, top_lines = clean_text_with_lines(texts, scores)
        print("\n===== CLEANED OCR =====")
        for l in lines:
            print(l["text"])
        print("=======================\n")
        doc_type = classify_document(lines)
        date = extract_date(lines)

        if doc_type == "unknown" and infer_prescription(lines):
            doc_type = "PRESCRIPTION"

        pages_data.append({
            "page_no": 1,
            "lines": lines,
            "top_lines": top_lines,
            "doc_type": doc_type,
            "date": date
        })

    return pages_data

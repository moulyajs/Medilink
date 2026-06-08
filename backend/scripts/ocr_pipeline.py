from document_classifier import classify_document
from date_extraction import extract_date
from paddocr import run_ocr
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
import re
import sys

from layout_parser import parse_table_from_ocr


def clean_text_with_lines(lines):
    cleaned = []
    seen = set()
    line_no = 1

    for l in lines:
        t = re.sub(r"\s+", " ", l["text"].strip())

        if len(t) < 3 or t in seen:
            continue

        seen.add(t)

        cleaned.append({
            "line_no": line_no,
            "text": t,
            "score": 1.0
        })

        line_no += 1

    return cleaned, [l["text"] for l in cleaned[:5]]


def ocr_process(file_path):
    poppler_path = None
    if sys.platform.startswith("win"):
        poppler_path = r"C:\Users\Najmus Seher\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

    pages_data = []

    # -------- IMAGE INPUT --------
    if not file_path.lower().endswith(".pdf"):

        # ---------------------------------
        # STEP 1: Initial OCR (NO preprocessing)
        # ---------------------------------
        texts, scores, raw = run_ocr(file_path, return_raw=True)

        box_count = len(raw[0]) if raw and raw[0] else 0
        print(f"\nInitial OCR boxes: {box_count}")

        # ---------------------------------
        # STEP 2: Choose preprocessing
        # ---------------------------------
        if box_count < 10:
            print("📝 Handwritten / low-quality detected")

            from image_preprocessing import preprocess_handwritten
            processed_img = preprocess_handwritten(file_path)

        else:
            print("📄 Printed document detected")

            from image_preprocessing import preprocess_printed
            processed_img = preprocess_printed(file_path)

        # ---------------------------------
        # STEP 3: OCR again (processed)
        # ---------------------------------
        texts, scores, raw = run_ocr(processed_img, return_raw=True)

        # 🔥 FALLBACK if preprocessing ruined it
        new_box_count = len(raw[0]) if raw and raw[0] else 0
        print(f"After preprocessing OCR boxes: {new_box_count}")

        if new_box_count < 10:
            print("⚠️ Fallback to original image")
            texts, scores, raw = run_ocr(file_path, return_raw=True)

        # ---------------------------------
        # STEP 4: Layout parsing
        # ---------------------------------
        structured_lines = parse_table_from_ocr(raw)
        print("\n=== RAW STRUCTURED OUTPUT ===")
        for row in structured_lines[:30]:
             print(row)
        # ---------------------------------
        # STEP 5: Clean lines (FIXED INDENT)
        # ---------------------------------
        cleaned = []
        line_no = 1

        for row in structured_lines:
            cols = row.get("columns", [])

            if not cols:
                continue

            cleaned.append({
                "line_no": line_no,
                "text": " ".join(cols),   # combined text
                "columns": cols           # 🔥 keep structured columns
            })

            line_no += 1

        lines = cleaned
        top_lines = [l["text"] for l in lines[:5]]

        print("\n=== DEBUG: FINAL LINES ===")
        for l in lines[:10]:
            print(l)

        # ---------------------------------
        # STEP 6: Classification
        # ---------------------------------
        doc_type = classify_document(lines).lower()
        date = extract_date(lines)

        pages_data.append({
            "page_no": 1,
            "lines": lines,
            "raw_rows": structured_lines,   # 🔥 ADD THIS LINE
            "top_lines": top_lines,
            "doc_type": doc_type,
            "date": date
        })

    return pages_data
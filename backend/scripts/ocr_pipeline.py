from document_classifier import classify_document
from date_extraction import extract_date
from paddocr import run_ocr
from pdf2image import convert_from_path
from pathlib import Path
import tempfile
import re
import sys
import shutil
from docker_poppler import pdf_to_images_docker

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


def ocr_process(file_path):

    pages_data = []

    # ------------------------------------
    # PLATFORM DETECTION
    # ------------------------------------
    is_windows = sys.platform.startswith("win")

    # ------------------------------------
    # PDF INPUT
    # ------------------------------------
    if file_path.lower().endswith(".pdf"):

        # ==============================
        # WINDOWS → LOCAL POPPLER
        # ==============================
        if is_windows:

            poppler_path = r"models\poppler-25.12.0\Library\bin"

            pages = convert_from_path(
                file_path,
                poppler_path=poppler_path
            )

            tmp_dir = Path(tempfile.mkdtemp())

            image_paths = []

            for i, page in enumerate(pages):
                img_path = tmp_dir / f"page_{i}.png"
                page.save(img_path, "PNG")
                image_paths.append(str(img_path))

        # ==============================
        # MAC / LINUX → DOCKER POPPLER
        # ==============================
        else:

            tmp_dir = Path(tempfile.mkdtemp())

            image_paths = pdf_to_images_docker(
                file_path,
                str(tmp_dir)
            )
            print("DEBUG: Images generated:", image_paths)

        # --------------------------------
        # OCR ON EACH PAGE
        # --------------------------------
        for i, img_path in enumerate(image_paths):

            texts, scores = run_ocr(img_path)

            lines, top_lines = clean_text_with_lines(
                texts,
                scores
            )

            doc_type = classify_document(lines)
            date = extract_date(lines)

            # Handwritten fallback
            if doc_type == "unknown" and infer_prescription(lines):
                print(f"⚠️ Page {i+1}: overridden to PRESCRIPTION")
                doc_type = "prescription"

            pages_data.append({
                "page_no": i + 1,
                "lines": lines,
                "top_lines": top_lines,
                "doc_type": doc_type,
                "date": date
            })

        # --------------------------------
        # CLEAN TEMP FILES
        # --------------------------------
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # ------------------------------------
    # IMAGE INPUT (NO PDF)
    # ------------------------------------
    else:

        texts, scores = run_ocr(file_path)

        lines, top_lines = clean_text_with_lines(
            texts,
            scores
        )

        # 🔍 DEBUG OCR OUTPUT
        print("\n===== FULL OCR TEXT (PAGE {}) =====")
        for l in lines:
            print(l["text"])
        print("===================================\n")
        doc_type = classify_document(lines)
        date = extract_date(lines)

        if doc_type == "unknown" and infer_prescription(lines):
            doc_type = "prescription"

        pages_data.append({
            "page_no": 1,
            "lines": lines,
            "top_lines": top_lines,
            "doc_type": doc_type,
            "date": date
        })

    return pages_data
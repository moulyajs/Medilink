# ============================================================
# DOCLING PDF PIPELINE
# ============================================================

import re
from typing import List, Dict, Any

from docling.document_converter import DocumentConverter


# ============================================================
# HELPER: SPLIT TEXT INTO OCR-LIKE LINES
# ============================================================

def _text_to_lines(text: str, page_num: int = 1) -> List[Dict[str, Any]]:
    """
    Convert raw text into the same line format used by OCR pipeline.
    """
    lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lines.append({
            "text": line,
            "page": page_num
        })

    return lines


# ============================================================
# HELPER: SIMPLE DOC TYPE DETECTOR
# ============================================================

def detect_doc_type_from_text(full_text: str) -> str:
    """
    Basic heuristic doc-type detector for PDFs.
    You can improve this later.
    """
    text = full_text.lower()

    lab_keywords = [
        "haemoglobin", "hemoglobin", "rbc", "wbc", "platelet",
        "creatinine", "glucose", "cholesterol", "bilirubin",
        "lab report", "investigation", "biochemistry"
    ]

    prescription_keywords = [
        "tablet", "capsule", "take once daily", "rx", "prescription",
        "mg", "after food", "before food"
    ]

    discharge_keywords = [
        "discharge summary", "admission", "diagnosis", "hospital course"
    ]

    ecg_keywords = [
        "ecg", "heart rate", "bpm", "qrs", "qt", "tachycardia"
    ]

    def score(keywords):
        return sum(1 for k in keywords if k in text)

    scores = {
        "LAB_REPORT": score(lab_keywords),
        "PRESCRIPTION": score(prescription_keywords),
        "DISCHARGE_SUMMARY": score(discharge_keywords),
        "ECG_REPORT": score(ecg_keywords),
    }

    best_type = max(scores, key=scores.get)

    if scores[best_type] == 0:
        return "UNKNOWN"

    return best_type


# ============================================================
# HELPER: TABLE NORMALIZATION
# ============================================================

def _normalize_docling_tables(doc) -> List[Dict[str, Any]]:
    """
    Try to extract tables from a Docling document into a simple structure.
    This is written defensively because Docling object structure can vary slightly
    depending on version.

    Output format:
    [
        {
            "table_index": 0,
            "rows": [
                ["Test", "Value", "Unit", "Range"],
                ["Hemoglobin", "13.2", "g/dL", "12-15"]
            ]
        }
    ]
    """
    normalized_tables = []

    # Try common docling table attributes
    possible_tables = []

    if hasattr(doc, "tables") and doc.tables:
        possible_tables = doc.tables
    elif hasattr(doc, "document") and hasattr(doc.document, "tables"):
        possible_tables = doc.document.tables

    for idx, table in enumerate(possible_tables):
        rows = []

        # Case 1: table.export_to_dataframe() exists
        if hasattr(table, "export_to_dataframe"):
            try:
                df = table.export_to_dataframe()
                rows = [list(df.columns)] + df.fillna("").astype(str).values.tolist()
            except Exception:
                pass

        # Case 2: fallback to generic row/cell extraction
        if not rows:
            if hasattr(table, "data") and table.data:
                try:
                    for row in table.data:
                        if isinstance(row, list):
                            rows.append([str(cell).strip() for cell in row])
                        else:
                            rows.append([str(row).strip()])
                except Exception:
                    pass

        if rows:
            normalized_tables.append({
                "table_index": idx,
                "rows": rows
            })

    return normalized_tables


# ============================================================
# MAIN DOCLING PARSER
# ============================================================

def parse_pdf_with_docling(file_path: str) -> Dict[str, Any]:
    """
    Parse a PDF using Docling and return a structure that can plug into
    the rest of the Medilink pipeline.

    Returns:
    {
        "full_text": str,
        "lines": [ {"text": ..., "page": ...}, ... ],
        "tables": [ {"table_index": ..., "rows": [...]}, ... ],
        "doc_type": str
    }
    """
    converter = DocumentConverter()
    result = converter.convert(file_path)

    # result.document is the Docling document in most standard flows
    doc = result.document if hasattr(result, "document") else result

    # ---------------------------
    # FULL TEXT
    # ---------------------------
    full_text = ""

    # Best effort extraction
    if hasattr(doc, "export_to_markdown"):
        try:
            full_text = doc.export_to_markdown()
        except Exception:
            full_text = ""

    if not full_text and hasattr(doc, "text"):
        full_text = str(doc.text)

    if not full_text:
        full_text = str(doc)

    # ---------------------------
    # OCR-LIKE LINES
    # ---------------------------
    lines = _text_to_lines(full_text, page_num=1)

    # ---------------------------
    # TABLES
    # ---------------------------
    tables = _normalize_docling_tables(doc)

    # ---------------------------
    # DOC TYPE
    # ---------------------------
    doc_type = detect_doc_type_from_text(full_text)

    return {
        "full_text": full_text,
        "lines": lines,
        "tables": tables,
        "doc_type": doc_type
    }
# ============================================================
# DOCLING PDF PIPELINE
# ============================================================

from typing import List, Dict, Any

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption
)
from docling.datamodel.pipeline_options import PdfPipelineOptions


# ------------------------------------------------------------
# PDF OPTIONS
# ------------------------------------------------------------
pipeline_options = PdfPipelineOptions()

# Keep OCR OFF for now.
# Your Docker installation currently throws:
# Unsupported configuration: torch.PP-OCRv6.det.small
pipeline_options.do_ocr = False


# ============================================================
# HELPER: SPLIT TEXT INTO OCR-LIKE LINES
# ============================================================

def _text_to_lines(text: str, page_num: int = 1) -> List[Dict[str, Any]]:
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
# DOC TYPE DETECTOR
# ============================================================

def detect_doc_type_from_text(full_text: str) -> str:

    text = full_text.lower()

    lab_keywords = [
        "haemoglobin", "hemoglobin",
        "rbc", "wbc",
        "platelet",
        "creatinine",
        "glucose",
        "cholesterol",
        "bilirubin",
        "lab report",
        "investigation",
        "biochemistry"
    ]

    prescription_keywords = [
        "tablet",
        "capsule",
        "take once daily",
        "rx",
        "prescription",
        "after food",
        "before food"
    ]

    discharge_keywords = [
        "discharge summary",
        "admission",
        "diagnosis",
        "hospital course"
    ]

    ecg_keywords = [
        "ecg",
        "heart rate",
        "bpm",
        "qrs",
        "qt",
        "tachycardia"
    ]

    def score(words):
        return sum(1 for w in words if w in text)

    scores = {
        "LAB_REPORT": score(lab_keywords),
        "PRESCRIPTION": score(prescription_keywords),
        "DISCHARGE_SUMMARY": score(discharge_keywords),
        "ECG_REPORT": score(ecg_keywords),
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "UNKNOWN"

    return best


# ============================================================
# TABLE NORMALIZATION
# ============================================================

def _normalize_docling_tables(doc):

    normalized_tables = []

    possible_tables = []

    if hasattr(doc, "tables") and doc.tables:
        possible_tables = doc.tables

    elif hasattr(doc, "document") and hasattr(doc.document, "tables"):
        possible_tables = doc.document.tables

    for idx, table in enumerate(possible_tables):

        rows = []

        # -------------------------------
        # export_to_dataframe()
        # -------------------------------
        if hasattr(table, "export_to_dataframe"):
            try:
                df = table.export_to_dataframe()

                rows = (
                    [list(df.columns)]
                    + df.fillna("").astype(str).values.tolist()
                )

            except Exception:
                pass

        # -------------------------------
        # table.data
        # -------------------------------
        if not rows:

            if hasattr(table, "data") and table.data:

                try:

                    for row in table.data:

                        if isinstance(row, list):
                            rows.append(
                                [str(c).strip() for c in row]
                            )

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
# MAIN PARSER
# ============================================================

def parse_pdf_with_docling(file_path: str):

    converter = DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    result = converter.convert(file_path)

    doc = result.document if hasattr(result, "document") else result

    # =====================================================
    # DEBUG
    # =====================================================
    # print("\n================ TABLE DEBUG ================\n")

    # if hasattr(doc, "tables"):

    #     print("Number of tables:", len(doc.tables))

    #     for i, table in enumerate(doc.tables):

    #         print("\nTABLE", i)
    #         print("TYPE :", type(table))
    #         print("\nTABLE.DATA TYPE:")
    #         print(type(table.data))

    #         print("\nTABLE.DATA:")
    #         print(table.data)

    #         print("\nTABLE.JSON:")
    #         try:
    #             print(table.model_dump())
    #         except Exception as e:
    #             print(e)
    #         print("\nATTRIBUTES:")
    #         print(dir(table))

    #         if hasattr(table, "export_to_dataframe"):
    #             try:
    #                 df = table.export_to_dataframe()

    #                 print("\nDATAFRAME SHAPE:", df.shape)
    #                 print(df.head())

    #             except Exception as e:
    #                 print("\nexport_to_dataframe FAILED:")
    #                 print(e)

    # else:

    #     print("Document has NO tables attribute.")

    # print("\n=============================================\n")

    # =====================================================
    # FULL TEXT
    # =====================================================

    full_text = ""
    # print("\n========== FULL TEXT ==========")
    # print(full_text[:5000])
    # print("===============================\n")
    if hasattr(doc, "export_to_markdown"):
        try:
            full_text = doc.export_to_markdown()
        except Exception:
            pass

    if not full_text and hasattr(doc, "text"):
        full_text = str(doc.text)

    if not full_text:
        full_text = str(doc)

    # =====================================================
    # LINES
    # =====================================================

    lines = _text_to_lines(full_text)

    # =====================================================
    # TABLES
    # =====================================================

    tables = _normalize_docling_tables(doc)

    # =====================================================
    # DOC TYPE
    # =====================================================

    doc_type = detect_doc_type_from_text(full_text)

    return {

        "full_text": full_text,
        "lines": lines,
        "tables": tables,
        "doc_type": doc_type

    }
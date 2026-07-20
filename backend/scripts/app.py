# ============================================================
# SYSTEM PATH SETUP
# ============================================================

import os
import sys
import uuid

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# ============================================================
# IMPORTS
# ============================================================

from sqlalchemy import text
from database import SessionLocal

from visit_grouper import group_by_date
from duplicate_detector import is_duplicate_report
from demographics_extraction import extract_demographics
from prescription_extraction import extract_prescriptions
from lab_extraction import (
    extract_lab_results,
    extract_date,
    normalize_date
)
from lab_normalizer import normalize_lab_results
#from clinical_facts_extraction import extract_clinical_facts
from ecg_extraction import extract_ecg_findings
from anomaly_detection import detect_patient_anomalies
#from user_review import review_prescriptions
# from clinical_summary import generate_summary

from uploader import upload_file

from record_saver import save_patient, save_lab_results
from timeline_saver import add_timeline_event

from dicom_viewer import (
    load_dicom,
    show_dicom_image,
    extract_dicom_metadata
)

# NEW: DOCLING PDF PARSER
from docling_pipeline import parse_pdf_with_docling

# RAG
from chunking.chunk_router import build_chunks
from embedding import embed_chunks
from vector_store import insert_chunks


# ============================================================
# ECG DETECTOR
# ============================================================

def looks_like_ecg(lines):
    text = " ".join(l["text"].lower() for l in lines)

    keywords = [
        "ecg", "hr", "bpm", "qrs", "qt",
        "tachycardia", "bundle branch",
        "axis deviation", "st", "t wave"
    ]

    return sum(k in text for k in keywords) >= 3


# ============================================================
# ARGUMENT HANDLING
# ============================================================

if len(sys.argv) < 3:
    print("Usage: python app.py <file_path> <patient_id>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    patient_id = str(uuid.UUID(sys.argv[2]))
except ValueError:
    print("❌ Invalid patient_id. Must be a valid UUID.")
    sys.exit(1)

is_pdf = file_path.lower().endswith(".pdf")
is_dicom = file_path.lower().endswith(".dcm")

print("\n======================================")
print("🚀 STARTING MEDICAL AI PIPELINE")
print("======================================\n")

# ============================================================
# STEP 0: UPLOAD FILE
# ============================================================

print("📤 Uploading file...")

document_id, stored_name = upload_file(file_path, patient_id)

print("✅ Document stored:", document_id)

# ============================================================
# STEP 1: DICOM HANDLING
# ============================================================

if is_dicom:

    print("\n🩻 INPUT TYPE: DICOM")

    ds = load_dicom(file_path)
    metadata = extract_dicom_metadata(ds)

    print("\n=== DICOM METADATA ===")
    print(metadata)

    print("\nDisplaying image...")
    show_dicom_image(ds)

    add_timeline_event(
        patient_id,
        document_id,
        "DICOM",
        "DICOM imaging file uploaded",
        None
    )

    print("🎉 DICOM PROCESSING COMPLETED")
    sys.exit(0)

# ============================================================
# STEP 2: OCR / DOCLING
# ============================================================

pages = []
pdf_data = None

if not is_pdf:

    print("🔍 Running OCR...")
    from ocr_pipeline import ocr_process
    pages = ocr_process(file_path)
    visits = group_by_date(pages)

else:

    print("📄 Running Docling PDF parser...")
    pdf_data = parse_pdf_with_docling(file_path)

    # Make PDF look like a single "visit" so downstream code stays similar
    visits = {
        "PDF_VISIT": [
            {
                "lines": pdf_data.get("lines", []),
                "doc_type": pdf_data.get("doc_type", "UNKNOWN"),
                "tables": pdf_data.get("tables", []),
                "full_text": pdf_data.get("full_text", "")
            }
        ]
    }

print(f"\nINPUT TYPE: {'PDF' if is_pdf else 'IMAGE'}")
print(f"TOTAL VISITS: {len(visits)}")

# ============================================================
# STEP 3: VISIT-WISE PROCESSING
# ============================================================

all_extracted_data = {
    "LAB_REPORT": [],
    "PRESCRIPTION": [],
    "CLINICAL_NOTE": [],
    "RADIOLOGY": []
}
last_visit_date = None

for visit_date, visit_pages in visits.items():

    last_visit_date = visit_date

    print("\n" + "=" * 60)
    print("VISIT DATE:", visit_date)
    print("=" * 60)

    visit_lines = []
    doc_types = set()

    pdf_tables = []
    pdf_full_text = ""

    # ----------------------------------------
    # IMAGE FLOW
    # ----------------------------------------
    if not is_pdf:

        for p in visit_pages:
            visit_lines.extend(p["lines"])
            doc_types.add(p["doc_type"])

        if not doc_types:
            print("⚠ No document types detected. Skipping.")
            continue

        if "LAB_REPORT" in doc_types:
            primary_doc_type = "LAB_REPORT"
        elif "PRESCRIPTION" in doc_types:
            primary_doc_type = "PRESCRIPTION"
        else:
            primary_doc_type = list(doc_types)[0]

        entities = extract_demographics(visit_lines, primary_doc_type)

    # ----------------------------------------
    # PDF FLOW (DOCLING)
    # ----------------------------------------
    else:
        pdf_page = visit_pages[0] if visit_pages else {}

        visit_lines = pdf_page.get("lines", [])
        pdf_tables = pdf_page.get("tables", [])
        # print(pdf_tables)
        pdf_full_text = pdf_page.get("full_text", "")
        primary_doc_type = pdf_page.get("doc_type", "UNKNOWN")

        entities = extract_demographics(visit_lines, primary_doc_type)

    print("\n👤 DEMOGRAPHICS")
    print(entities)

    save_patient(
        patient_id,
        entities.get("dob"),
        entities.get("gender")
    )

    # ----------------------------------------
    # PRESCRIPTIONS
    # ----------------------------------------
    """
    medicines = []

    if not is_pdf and "PRESCRIPTION" in doc_types:
        medicines = extract_prescriptions(visit_lines)
        if medicines:
            all_extracted_data["PRESCRIPTION"].extend(
                medicines
            )

    elif is_pdf and primary_doc_type == "PRESCRIPTION":
        medicines = extract_prescriptions(visit_lines)
        if medicines:
            all_extracted_data["PRESCRIPTION"].extend(
                medicines
            )
    #reviewed_medicines = review_prescriptions(medicines)

    print("\n💊 PRESCRIPTIONS")
    print(medicines)
"""
    # ----------------------------------------
    # LAB RESULTS
    # ----------------------------------------
    normalized_labs = []

    if is_pdf and primary_doc_type == "LAB_REPORT":

        print("📄 Extracting labs from Docling PDF output...")
        print("\n========== PDF FULL TEXT ==========")
        print(pdf_full_text[:1500])      # print first 1500 characters
        print("==================================")

        print("Extracted report date:",
            normalize_date(extract_date(pdf_full_text)))
        raw_labs = extract_lab_results(
            {
                "lines": visit_lines,
                "tables": pdf_tables,
                "full_text": pdf_full_text
            },
            source="docling"
        )

    elif "LAB_REPORT" in doc_types:

        raw_labs = extract_lab_results(visit_lines)

    else:
        raw_labs = []

    normalized_labs = normalize_lab_results(raw_labs)

    print("\n🧪 LAB RESULTS")
    print(normalized_labs)
    if is_duplicate_report(patient_id, normalized_labs):

        print("\n⚠ Duplicate report detected.")
        print("Skipping save...\n")

        continue
    if normalized_labs:
        print("\n=== FINAL LABS ===")
        for lab in normalized_labs:
            print(lab)
        save_lab_results(
            patient_id,
            document_id,
            normalized_labs
        )
        all_extracted_data["LAB_REPORT"].extend(
    normalized_labs
)

    print("\n🔍 Checking historical lab trends...")

    anomalies = detect_patient_anomalies(
        patient_id,
        normalized_labs
    )

    print("\n📈 PATIENT LAB TRENDS")

    if not anomalies:
        print("No significant trend detected.")

    else:
        for a in anomalies:

            print("--------------------------------")

            print("Test :", a["test_name"])

            print("Current :", a["current_value"])

            print("Baseline :", a["baseline"])

            print("History :", a["history"])

            print("% Change :", a["percent_change"])

            print("Trend :", a["trend"])
    # ----------------------------------------
    # ECG
    # ----------------------------------------
    ecg_data = None

    if not is_pdf and visit_lines and looks_like_ecg(visit_lines):
        ecg_data = extract_ecg_findings(visit_lines)

    print("\n🫀 ECG FINDINGS")
    print(ecg_data)

    # ----------------------------------------
    # CLINICAL FACTS
    # ----------------------------------------
    ## uncomment when u want to clinical notes
    """
    if is_pdf:
        full_text = pdf_full_text.strip()
    else:
        full_text = "\n".join(l["text"] for l in visit_lines) if visit_lines else ""

    if full_text:
        clinical_facts = extract_clinical_facts(full_text)
    else:
        clinical_facts = {}

    print("\n🧠 CLINICAL FACTS")
    print(clinical_facts)

    if clinical_facts:

        all_extracted_data["CLINICAL_NOTE"].append(
        {
            "report_date": visit_date,
            "facts": clinical_facts
        }
    )

    # ----------------------------------------
    # SUMMARY (LEFT COMMENTED)
    # ----------------------------------------
    # summary = generate_summary(
    #     entities,
    #     reviewed_medicines,
    #     normalized_labs
    # )
    #
    # print("\nSUMMARY:")
    # print(summary)

    # ----------------------------------------
    # TIMELINE
    # ----------------------------------------
    add_timeline_event(
        patient_id,
        document_id,
        primary_doc_type,
        visit_date
    )

    print("📅 Timeline updated")
"""
# ============================================================
# STEP 4: RAG INGESTION
# ============================================================

print("\n📦 Creating RAG chunks...")

all_chunks = []

# ----------------------------------
# LAB REPORTS
# ----------------------------------

if all_extracted_data["LAB_REPORT"]:

    chunks = build_chunks(
        doc_type="LAB_REPORT",
        extracted_data=
            all_extracted_data["LAB_REPORT"],

        patient_id=patient_id,
        document_id=document_id
    )

    all_chunks.extend(chunks)

# ----------------------------------
# PRESCRIPTIONS
# ----------------------------------
"""
if all_extracted_data["PRESCRIPTION"]:

    chunks = build_chunks(
        doc_type="PRESCRIPTION",
        extracted_data=
            all_extracted_data["PRESCRIPTION"],

        patient_id=patient_id,
        document_id=document_id
    )

    all_chunks.extend(chunks)
    """
# ----------------------------------
# CLINICAL NOTES
# ----------------------------------

if all_extracted_data["CLINICAL_NOTE"]:

    chunks = build_chunks(
        doc_type="CLINICAL_NOTE",
        extracted_data=
            all_extracted_data["CLINICAL_NOTE"],
        patient_id=patient_id,
        document_id=document_id,
        


    )

    all_chunks.extend(chunks)
# ----------------------------------
# STORE
# ----------------------------------

if all_chunks:

    print(
        f"🧩 Total chunks created: "
        f"{len(all_chunks)}"
    )

    embeddings = embed_chunks(all_chunks)

    insert_chunks(
        all_chunks,
        embeddings
    )

    print(
        "✅ RAG ingestion completed"
    )

else:

    print(
        "⚠ No chunks created"
    )

print("\n======================================")
print("🎉 PIPELINE COMPLETED")
print("======================================\n")
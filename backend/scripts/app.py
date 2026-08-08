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

from ocr_pipeline import ocr_process
from visit_grouper import group_by_date

from demographics_extraction import extract_demographics
from prescription_extraction import extract_prescriptions
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from clinical_facts_extraction import extract_clinical_facts
from ecg_extraction import extract_ecg_findings

from user_review import review_prescriptions
#from clinical_summary import generate_summary

from uploader import upload_file

#from record_saver import save_patient, save_lab_results
from record_saver import (
    save_patient,
    save_lab_results,
    save_medical_record
)

from timeline_saver import add_timeline_event

from dicom_viewer import (
    load_dicom,
    show_dicom_image,
    extract_dicom_metadata
)

# ============================================================
# ECG DETECTOR
# ============================================================

def looks_like_ecg(lines):

    text = " ".join(l["text"].lower() for l in lines)

    keywords = [
        "ecg","hr","bpm","qrs","qt",
        "tachycardia","bundle branch",
        "axis deviation","st","t wave"
    ]

    return sum(k in text for k in keywords) >= 3


# ============================================================
# ARGUMENT HANDLING
# ============================================================

if len(sys.argv) < 3:
    print("Usage: python app.py <file_path> <patient_id>")
    sys.exit(1)

file_path = sys.argv[1]

patient_id = sys.argv[2]

if not patient_id:
    print("❌ Patient ID is required.")
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
# STEP 2: OCR
# ============================================================

pages = []

if not is_pdf:

    print("🔍 Running OCR...")

    pages = ocr_process(file_path)

    visits = group_by_date(pages)

else:

    visits = {"PDF_VISIT": []}

print(f"\nINPUT TYPE: {'PDF' if is_pdf else 'IMAGE'}")
print(f"TOTAL VISITS: {len(visits)}")

# ============================================================
# STEP 3: VISIT-WISE PROCESSING
# ============================================================

for visit_date, visit_pages in visits.items():

    print("\n" + "=" * 60)
    print("VISIT DATE:", visit_date)
    print("=" * 60)

    visit_lines = []
    doc_types = set()

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

    else:

        primary_doc_type = "LAB_REPORT"
        visit_lines = []
        entities = {}

    print("\n👤 DEMOGRAPHICS")
    print(entities)

    #save_patient(
    #    patient_id,
    #    entities.get("dob"),
     #   entities.get("gender")
    #)

    # ----------------------------------------
    # PRESCRIPTIONS
    # ----------------------------------------

    medicines = []

    if not is_pdf and "PRESCRIPTION" in doc_types:
        medicines = extract_prescriptions(visit_lines)

    reviewed_medicines = review_prescriptions(medicines)

    print("\n💊 PRESCRIPTIONS")
    print(reviewed_medicines)

    # ----------------------------------------
    # LAB RESULTS
    # ----------------------------------------

    normalized_labs = []

    if is_pdf:

        print("📄 Extracting labs directly from PDF...")

        raw_labs = extract_lab_results(file_path, source="pdf")

    elif "LAB_REPORT" in doc_types:

        raw_labs = extract_lab_results(visit_lines)

    else:

        raw_labs = []

    normalized_labs = normalize_lab_results(raw_labs)

    print("\n🧪 LAB RESULTS")
    print(normalized_labs)

    #save_lab_results(
    #    patient_id,
    #    document_id,
    #    normalized_labs
    #)

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

    if visit_lines:
        full_text = "\n".join(l["text"] for l in visit_lines)
        clinical_facts = extract_clinical_facts(full_text)
    else:
        clinical_facts = {}

    print("\n🧠 CLINICAL FACTS")
    print(clinical_facts)

    medical_record_id = save_medical_record(
        patient_id=patient_id,
        file_id=document_id,
        document_type=primary_doc_type,
        labs=normalized_labs,
        clinical_facts=clinical_facts
    )
    save_lab_results(
        patient_id,
        document_id,
        normalized_labs
    )

    print("✅ Lab Results Saved")

    add_timeline_event(
        patient_id,
        document_id,
        primary_doc_type,
        visit_date
    )

    print("📅 Timeline updated")

print("\n======================================")
print("🎉 PIPELINE COMPLETED")
print("======================================\n")

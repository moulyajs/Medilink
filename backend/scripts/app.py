# scripts/app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import text
from database import SessionLocal

from document_ocr import run_document_ocr
from entity_extraction import extract_entities
#from ner_extraction import ner_entities
from medicine_extraction import extract_medicines
from clinical_summary import generate_summary
from document_classifier import classify_document
from demographics_extraction import extract_demographics
from prescription_extraction import extract_prescriptions
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from user_review import review_prescriptions
from simple_explainer import explain_simple

from uploader import upload_file
from records_saver import save_medical_record
from timeline_saver import add_timeline_event


# -----------------------------
# Utils
# -----------------------------

def merge_pages(pages):

    all_lines = []
    all_text = []

    for p in pages:

        all_text.append(f"\n=== PAGE {p['page']} ===\n")

        for l in p["lines"]:
            l["page"] = p["page"]
            all_lines.append(l)

        all_text.append(p["raw_text"])

    return all_lines, "\n".join(all_text)


# -----------------------------
# Argument Handling
# -----------------------------

if len(sys.argv) < 3:
    print("Usage: python app.py <file_path> <patient_id>")
    sys.exit(1)

file_path = sys.argv[1]
patient_id = int(sys.argv[2])

print("\n======================================")
print("🚀 STARTING MEDICAL AI PIPELINE")
print("======================================\n")


# -----------------------------
# Step 0: Upload File
# -----------------------------

print("📤 Uploading file to MinIO + DB...")

file_db_id, stored_name = upload_file(file_path, patient_id)

print("✅ File stored as:", stored_name)


# -----------------------------
# Step 1: OCR
# -----------------------------

print("\n🔎 Running OCR...")

pages = run_document_ocr(file_path)

print("PAGES PROCESSED:", len(pages))
for p in pages:
    print(f"Page {p['page']} -> {len(p['lines'])} lines")

lines, text = merge_pages(pages)

print("\nOCR TEXT PREVIEW:\n", text[:800])


# -----------------------------
# Step 2: Document Classification
# -----------------------------

doc_type = classify_document(lines)

print("\n📄 DOCUMENT TYPE:", doc_type)


# -----------------------------
# Step 3: Demographics
# -----------------------------

entities = extract_demographics(lines, doc_type)

print("\n👤 DEMOGRAPHICS:", entities)


# -----------------------------
# Step 4: Prescription Extraction
# -----------------------------

if doc_type == "PRESCRIPTION":
    medicines = extract_prescriptions(lines)
else:
    medicines = []

reviewed_medicines = review_prescriptions(medicines)

print("\n💊 PRESCRIPTIONS:", reviewed_medicines)


# -----------------------------
# Step 5: Lab Extraction
# -----------------------------

if doc_type == "LAB_REPORT":
    lab_results = extract_lab_results(lines)
    normalized_lab_results = normalize_lab_results(lab_results)
else:
    lab_results = []
    normalized_lab_results = []

print("\n🧪 LAB RESULTS:", normalized_lab_results)

if doc_type == "LAB_REPORT" and len(normalized_lab_results) < 2:
    print("⚠️ Low confidence extraction detected.")


# -----------------------------
# Step 6: NER
# -----------------------------

#ner = ner_entities(text)

#print("\n🧠 NER OUTPUT:", ner)

#if ner.get("organizations"):
#    for org in ner["organizations"]:
#        if "accuris" in org.lower():
#            entities["hospital"] = org
#            break


# -----------------------------
# Step 7: Clinical Summary
# -----------------------------

summary = generate_summary(
    entities,
    reviewed_medicines,
    normalized_lab_results
)

print("\n📋 CLINICAL SUMMARY:\n", summary)


# -----------------------------
# Step 8: Patient Explanation
# -----------------------------

simple_text = explain_simple(summary)

print("\n🗣️ PATIENT EXPLANATION:\n", simple_text)


# -----------------------------
# Step 9: Save Medical Record
# -----------------------------

print("\n💾 Saving medical record to database...")

clinical_facts = {
    #"ner": ner,
    "doc_type": doc_type
}

record_id = save_medical_record(
    patient_id=patient_id,
    file_id=file_db_id,
    doc_type=doc_type,

    demographics=entities,
    prescriptions=reviewed_medicines,
    labs=normalized_lab_results,
    clinical_facts=clinical_facts,

    summary=summary,
    explanation=simple_text
)

print("✅ Medical record saved with ID:", record_id)


# -----------------------------
# Step 10: Add Timeline Event
# -----------------------------

add_timeline_event(
    patient_id=patient_id,
    record_id=record_id,
    event_type=doc_type,
    short_summary=summary
)

print("📅 Timeline updated")


# -----------------------------
# Step 11: Update File Status
# -----------------------------

db = SessionLocal()

db.execute(
    text("UPDATE files SET status='processed' WHERE id=:id"),
    {"id": file_db_id}
)

db.commit()
db.close()

print("📁 File status updated to 'processed'")


# -----------------------------
# DONE
# -----------------------------

print("\n======================================")
print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
print("======================================\n")

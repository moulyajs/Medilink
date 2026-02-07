# scripts/app.py

from ocr_pipeline import ocr_process
from demographics_extraction import extract_demographics
from medicine_extraction import extract_medicines
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from user_review import review_prescriptions
from ner_extraction import ner_entities
from clinical_summary import generate_summary
from clinical_facts_extraction import extract_clinical_facts


# -----------------------------
# Step 0: Input File
# -----------------------------
file_path = "data/labrec.png"
lines, top_lines, doc_type = ocr_process(file_path)
print("DEBUG → doc_type =", doc_type)

# 🔥 Robust fallback for handwritten prescriptions
if doc_type.lower() == "unknown":
    doc_type = "prescription"
    print("⚠️ doc_type overridden to PRESCRIPTION (handwritten fallback)")


# -----------------------------
# Step 1: OCR Output
# -----------------------------
print("\n=== OCR STRUCTURED LINES ===")
for l in lines:
    print(f"[Line {l['line_no']}] {l['text']}")


# -----------------------------
# Step 2: Demographics
# -----------------------------
entities = extract_demographics(lines, doc_type)
print("\n=== DEMOGRAPHICS ===")
print(entities)

patient_name = entities.get("patient_name", "").lower()
doctor_name = entities.get("doctor_name", "").lower()


# -----------------------------
# Step 3: Medicines (FINAL SAFE MODE)
# -----------------------------
medicines = extract_medicines(lines)

# 🚫 FINAL HARD FILTER — NEVER allow human names as drugs
filtered_medicines = []
for m in medicines:
    drug_lower = m["drug"].lower()

    if patient_name and patient_name in drug_lower:
        continue
    if doctor_name and doctor_name in drug_lower:
        continue

    filtered_medicines.append(m)

print("\n=== PRESCRIPTIONS (RAW) ===")
for m in filtered_medicines:
    print(m)

reviewed_medicines = review_prescriptions(filtered_medicines)

print("\n=== PRESCRIPTIONS (AFTER REVIEW) ===")
for m in reviewed_medicines:
    print(m)


# -----------------------------
# Step 4: Lab Extraction
# -----------------------------
lab_results = extract_lab_results(lines) if doc_type == "lab_report" else []

print("\n=== LAB RESULTS (RAW) ===")
for r in lab_results:
    print(r)

normalized_lab_results = normalize_lab_results(lab_results) if lab_results else []


# -----------------------------
# Step 5: Clinical Facts
# -----------------------------
full_text = "\n".join(l["text"] for l in lines)
clinical_facts = extract_clinical_facts(full_text)

print("\n=== CLINICAL FACTS ===")
print(clinical_facts)


# -----------------------------
# Step 6: NER
# -----------------------------
ner = ner_entities(full_text)
print("\n=== NER OUTPUT ===")
print(ner)


# -----------------------------
# Step 7: Clinical Summary
# -----------------------------
summary = generate_summary(
    entities,
    reviewed_medicines,
    normalized_lab_results,
    clinical_facts
)

print("\n=== CLINICAL SUMMARY ===")
print(summary)


# -----------------------------
# Step 8: Final Entities
# -----------------------------
print("\n=== FINAL ENTITIES ===")
print(entities)

# scripts/app.py

from ocr_pipeline import ocr_process
from entity_extraction import extract_entities
from ner_extraction import ner_entities
from medicine_extraction import extract_medicines
from clinical_summary import generate_summary
from document_classifier import classify_document
from demographics_extraction import extract_demographics
from prescription_extraction import extract_prescriptions
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from user_review import review_prescriptions


# -----------------------------
# Step 1: OCR + Cleaning
# -----------------------------
image_path = "../data/nanavati.png"
ocr_output = ocr_process(image_path)

lines = ocr_output["lines"]
text = ocr_output["raw_text"]
top_lines = ocr_output["top_lines"]

print("\nOCR STRUCTURED LINES:")
for l in lines:
    print(l)

print("\nRAW TEXT:\n", text)

doc_type = classify_document(lines)
print("\nDOCUMENT TYPE:", doc_type)

# -----------------------------
# Step 2: Rule-based extraction
# -----------------------------
entities = extract_demographics(lines, doc_type)
print("\nDEMOGRAPHICS:", entities)

if doc_type == "PRESCRIPTION":
    medicines = extract_prescriptions(lines)
else:
    medicines = []

print("\nPRESCRIPTIONS (RAW EXTRACTION):", medicines)

# -----------------------------
# USER REVIEW STEP (HUMAN-IN-THE-LOOP)
# -----------------------------
reviewed_medicines = review_prescriptions(medicines)

print("\nPRESCRIPTIONS (AFTER USER REVIEW):")
for m in reviewed_medicines:
    print(m)
# Step 3: Lab extraction 
# -----------------------------
if doc_type == "LAB_REPORT":
    lab_results = extract_lab_results(lines)
else:
    lab_results = []

print("\nLAB RESULTS:", lab_results)

if doc_type == "LAB_REPORT":
    normalized_lab_results = normalize_lab_results(lab_results)
else:
    normalized_lab_results = []

print("\nNORMALIZED LAB RESULTS (CLINICAL FACTS):")
for r in normalized_lab_results:
    print(r)

# -----------------------------
# Step 4: NER refinement (hybrid)
# -----------------------------
ner = ner_entities(text)
print("\nNER OUTPUT:\n", ner)

# Update hospital if NER gives better name
if ner["organizations"]:
    ner_hospital = ner["organizations"][0]
    if "hospital" not in entities or len(ner_hospital) > len(entities.get("hospital", "")):
        entities["hospital"] = ner_hospital

# -----------------------------
# Step 5: Clinical Summary
# -----------------------------
# Now summary uses RAW medicines, not validated ones
summary = generate_summary(
    entities,
    reviewed_medicines,                  # raw extracted prescriptions
    normalized_lab_results
)

print("\nCLINICAL SUMMARY:\n", summary)

# -----------------------------
# Step 6: Final Entities
# -----------------------------
print("\nFINAL ENTITIES:\n", entities)

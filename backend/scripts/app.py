# scripts/app.py

from ocr_pipeline import ocr_process
from demographics_extraction import extract_demographics
from medicine_extraction import extract_medicines
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from user_review import review_prescriptions
from ner_extraction import ner_entities
from clinical_summary import generate_summary

# -----------------------------
# Step 0: Input File
# -----------------------------
file_path = "data/max_lab_report.pdf"  # Supports .jpg, .png, .pdf
lines, top_lines, doc_type = ocr_process(file_path)
print("DEBUG → doc_type =", doc_type)

# -----------------------------
# Step 1: OCR Output
# -----------------------------
print("\n=== OCR STRUCTURED LINES ===")
for l in lines:
    print(f"[Line {l['line_no']}] {l['text']}")

print("\n=== TOP 5 LINES ===")
for l in top_lines:
    print(l)

print("\n=== DOCUMENT TYPE DETECTED ===")
print(doc_type)

# -----------------------------
# Step 2: Demographics Extraction
# -----------------------------
entities = extract_demographics(lines, doc_type)
print("\n=== DEMOGRAPHICS ===")
print(entities)

# -----------------------------
# Step 3: Prescription / Medicines Extraction
# -----------------------------
if doc_type.lower() == "prescription":
    medicines = extract_medicines(lines)
else:
    medicines = []

print("\n=== PRESCRIPTIONS (RAW EXTRACTION) ===")
for m in medicines:
    print(m)

# -----------------------------
# Step 4: Human-in-the-loop Review
# -----------------------------
reviewed_medicines = review_prescriptions(medicines)
print("\n=== PRESCRIPTIONS (AFTER USER REVIEW) ===")
for m in reviewed_medicines:
    print(m)

# -----------------------------
# Step 5: Lab Extraction & Normalization
# -----------------------------
lab_results = []

if doc_type.lower() == "lab_report":
    # Extract numeric lab results
    lab_results = extract_lab_results(lines)
elif doc_type.lower() == "prescription":
    lab_results = []  # no lab extraction from prescription


print("\n=== LAB RESULTS (RAW) ===")
for r in lab_results:
    print(r)

# Normalize lab values if numeric
normalized_lab_results = normalize_lab_results(lab_results) if lab_results else []
print("\n=== NORMALIZED LAB RESULTS (CLINICAL FACTS) ===")
for r in normalized_lab_results:
    print(r)

# -----------------------------
# Step 6: NER Refinement (Hybrid)
# -----------------------------
full_text = " ".join([l["text"] for l in lines])
ner = ner_entities(full_text)
print("\n=== NER OUTPUT ===")
print(ner)

# Add hospital info if missing
if "hospital" not in entities and ner.get("organizations"):
    for org in ner["organizations"]:
        if any(x in org.lower() for x in ["hospital", "clinic", "medical"]):
            entities["hospital"] = org
            break

# -----------------------------
# Step 7: Clinical Summary
# -----------------------------
summary = generate_summary(
    entities,
    reviewed_medicines,
    normalized_lab_results
)
print("\n=== CLINICAL SUMMARY ===")
print(summary)

# -----------------------------
# Step 8: Final Entities
# -----------------------------
print("\n=== FINAL ENTITIES ===")
print(entities)

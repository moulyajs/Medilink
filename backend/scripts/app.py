# scripts/app.py

from ocr_pipeline import ocr_process
from entity_extraction import extract_entities
from ner_extraction import ner_entities
from medicine_extraction import extract_medicines
from clinical_summary import generate_summary

# -----------------------------
# Step 1: OCR + Cleaning
# -----------------------------
image_path = "data/pdf2.pdf"

text, top_lines, doc_type = ocr_process(image_path)

print("DOCUMENT TYPE:", doc_type)
print("\nCLEANED TEXT:\n", text)

# 🚨 STOP EARLY FOR LAB REPORTS
if doc_type == "lab_report":
    print("\nLAB REPORT DETECTED")
    print("SUMMARY: Laboratory investigation report. No medications prescribed.")
    print("FINAL ENTITIES: {}")
    exit()

# -----------------------------
# Step 2: Rule-based extraction
# -----------------------------
entities = extract_entities(text, top_lines)
print("\nRULE-BASED ENTITIES:\n", entities)

# -----------------------------
# Step 3: NER refinement (SAFE HYBRID)
# -----------------------------
ner = ner_entities(text)
print("\nNER OUTPUT:\n", ner)

# ✅ DO NOT override rule-based hospital
if "hospital" not in entities and ner["organizations"]:
    for org in ner["organizations"]:
        if "hospital" in org.lower() or "clinic" in org.lower() or "medical" in org.lower():
            entities["hospital"] = org
            break

# -----------------------------
# Step 4: Medicine Extraction (Prescription only)
# -----------------------------
medicines = extract_medicines(text)
print("\nMEDICINES:\n", medicines)

# -----------------------------
# Step 5: Clinical Summary
# -----------------------------
summary = generate_summary(entities, medicines)
print("\nCLINICAL SUMMARY:\n", summary)

# -----------------------------
# Step 6: Final Entities
# -----------------------------
print("\nFINAL ENTITIES:\n", entities)

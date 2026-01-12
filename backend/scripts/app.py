# scripts/app.py

from ocr_pipeline import ocr_process
from entity_extraction import extract_entities
from ner_extraction import ner_entities
from medicine_extraction import extract_medicines
from clinical_summary import generate_summary

# -----------------------------
# Step 1: OCR + Cleaning
# -----------------------------
image_path = "data/cleannavyatri.jpg"
text, top_lines = ocr_process(image_path)
print("\nCLEANED TEXT:\n", text)

# -----------------------------
# Step 2: Rule-based extraction
# -----------------------------
entities = extract_entities(text, top_lines)
print("\nRULE-BASED ENTITIES:\n", entities)

# -----------------------------
# Step 3: NER refinement (hybrid)
# -----------------------------
ner = ner_entities(text)
print("\nNER OUTPUT:\n", ner)

# Update hospital if NER gives better name
if ner["organizations"]:
    ner_hospital = ner["organizations"][0]
    if "hospital" not in entities or len(ner_hospital) > len(entities.get("hospital", "")):
        entities["hospital"] = ner_hospital

# -----------------------------
# Step 4: Dynamic Medicine Extraction
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

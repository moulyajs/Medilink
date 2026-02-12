# scripts/app.py

import sys

from document_ocr import run_document_ocr

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
from simple_explainer import explain_simple


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
# Main
# -----------------------------

if len(sys.argv) < 2:
    print("Usage: python app.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]


# -----------------------------
# Step 1: OCR (Image + PDF)
# -----------------------------

pages = run_document_ocr(file_path)

print("\nPAGES PROCESSED:", len(pages))
for p in pages:
    print(f"Page {p['page']} -> {len(p['lines'])} lines")


lines, text = merge_pages(pages)

print("\nOCR STRUCTURED LINES:")
for l in lines:
    print(f"[P{l['page']}] {l['text']}")


print("\nRAW TEXT (Preview):\n", text[:1000])


# -----------------------------
# Step 2: Document Type
# -----------------------------

doc_type = classify_document(lines)

print("\nDOCUMENT TYPE:", doc_type)


# -----------------------------
# Step 3: Demographics
# -----------------------------

entities = extract_demographics(lines, doc_type)

print("\nDEMOGRAPHICS:", entities)


# -----------------------------
# Step 4: Prescriptions
# -----------------------------

if doc_type == "PRESCRIPTION":
    medicines = extract_prescriptions(lines)
else:
    medicines = []

print("\nPRESCRIPTIONS (RAW):", medicines)


# Human review
reviewed_medicines = review_prescriptions(medicines)

print("\nPRESCRIPTIONS (REVIEWED):")
for m in reviewed_medicines:
    print(m)


# -----------------------------
# Step 5: Lab Extraction
# -----------------------------

# Step 5: Lab Extraction (Page-wise)
from collections import defaultdict

if doc_type == "LAB_REPORT":

    lab_results = extract_lab_results(lines)

else:
    lab_results = []


print("\nLAB RESULTS:", lab_results)


if doc_type == "LAB_REPORT":
    normalized_lab_results = normalize_lab_results(lab_results)
else:
    normalized_lab_results = []

print("\nNORMALIZED LAB RESULTS:")

for r in normalized_lab_results:
    print(r)


# Confidence check
if doc_type == "LAB_REPORT" and len(normalized_lab_results) < 2:
    print("⚠️ Warning: Low confidence extraction. Consider LLM fallback.")


# -----------------------------
# Step 6: NER
# -----------------------------

ner = ner_entities(text)

print("\nNER OUTPUT:\n", ner)


# Improve hospital name
if ner.get("organizations"):

    for org in ner["organizations"]:

        if "accuris" in org.lower():
            entities["hospital"] = org
            break


# -----------------------------
# Step 7: Summary
# -----------------------------

summary = generate_summary(
    entities,
    reviewed_medicines,
    normalized_lab_results
)

print("\nCLINICAL SUMMARY:\n", summary)

# -----------------------------
# Step 9: Simple Explanation
# -----------------------------

simple_text = explain_simple(summary)

print("\nPATIENT-FRIENDLY EXPLANATION:\n")
print(simple_text)

# -----------------------------
# Step 8: Final Output
# -----------------------------

print("\nFINAL ENTITIES:\n", entities)

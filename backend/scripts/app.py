# scripts/app.py
# scripts/app.py

from ocr_pipeline import ocr_process
from visit_grouper import group_by_date

from demographics_extraction import extract_demographics
from medicine_extraction import extract_medicines
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from user_review import review_prescriptions
from ner_extraction import ner_entities
from clinical_summary import generate_summary
from clinical_facts_extraction import extract_clinical_facts
from ecg_extraction import extract_ecg_findings

def looks_like_ecg(lines):
    text = " ".join(l["text"].lower() for l in lines)
    ecg_keywords = [
        "ecg", "hr", "bpm", "qrs", "qt", "tachycardia",
        "bundle branch", "axis deviation", "st", "t wave"
    ]
    return sum(k in text for k in ecg_keywords) >= 3

# -----------------------------
# Step 0: Input File
# -----------------------------
file_path = "data/sterling_labReport.pdf"

pages = ocr_process(file_path)
visits = group_by_date(pages)

print(f"\nTOTAL PAGES: {len(pages)}")
print(f"TOTAL VISITS DETECTED: {len(visits)}")


# -----------------------------
# Step 1: Process VISIT-WISE
# -----------------------------
for visit_date, visit_pages in visits.items():

    print("\n" + "=" * 60)
    print(f"VISIT DATE: {visit_date}")
    print("=" * 60)

    # ---------------------------------
    # Combine lines for this visit
    # ---------------------------------
    visit_lines = []
    doc_types = set()

    for p in visit_pages:
        visit_lines.extend(p["lines"])
        doc_types.add(p["doc_type"])

    # ---------------------------------
    # OCR DEBUG
    # ---------------------------------
    print("\n=== OCR STRUCTURED LINES ===")
    for l in visit_lines:
        print(f"[Line {l['line_no']}] {l['text']}")

    # ---------------------------------
    # Step 2: Demographics
    # ---------------------------------
    primary_doc_type = "lab_report" if "lab_report" in doc_types else list(doc_types)[0]

    entities = extract_demographics(visit_lines, primary_doc_type)

    print("\n=== DEMOGRAPHICS ===")
    print(entities)

    patient_name = entities.get("patient_name", "").lower()
    doctor_name = entities.get("doctor_name", "").lower()

    # ---------------------------------
    # Step 3: Medicines (VISIT SAFE)
    # ---------------------------------
    medicines = []
    if "prescription" in doc_types:
        medicines = extract_medicines(visit_lines)

        # 🚫 HARD FILTER: human names ≠ drugs
        filtered_medicines = []
        for m in medicines:
            drug_lower = m["drug"].lower()
            if patient_name and patient_name in drug_lower:
                continue
            if doctor_name and doctor_name in drug_lower:
                continue
            filtered_medicines.append(m)

        medicines = review_prescriptions(filtered_medicines)

    print("\n=== PRESCRIPTIONS ===")
    for m in medicines:
        print(m)

    # ---------------------------------
    # Step 4: Lab Extraction (VISIT SAFE)
    # ---------------------------------
    labs = []
    if "lab_report" in doc_types:
        raw_labs = extract_lab_results(visit_lines)
        labs = normalize_lab_results(raw_labs)

    print("\n=== LAB RESULTS ===")
    for l in labs:
        print(l)

    abnormal_labs = [l for l in labs if l.get("abnormal", False)]

    print("\n=== ABNORMAL LABS ===")
    for l in abnormal_labs:
        print(l)

    # ---------------------------------
    # Step 4B: ECG Extraction (VISIT SAFE)
    # ---------------------------------
    ecg = None
    if looks_like_ecg(visit_lines):
        ecg = extract_ecg_findings(visit_lines)

    print("\n=== ECG FINDINGS ===")
    if ecg:
        print(ecg)
    else:
        print("No ECG data detected")

    # ---------------------------------
    # Step 5: Clinical Facts
    # ---------------------------------
    full_text = "\n".join(l["text"] for l in visit_lines)
    clinical_facts = extract_clinical_facts(full_text)

    print("\n=== CLINICAL FACTS ===")
    print(clinical_facts)

    # ---------------------------------
    # Step 6: NER
    # ---------------------------------
    # ner = ner_entities(full_text)

    # print("\n=== NER OUTPUT ===")
    # print(ner)

    # ---------------------------------
    # Step 7: Summary (VISIT-WISE)
    # ---------------------------------
    # summary = generate_summary(
    #     demographics=entities,
    #     medicines=medicines,
    #     labs=labs,
    #     clinical_facts=clinical_facts
    # )

    # print("\n=== CLINICAL SUMMARY ===")
    # print(summary)

    # ---------------------------------
    # Step 8: Final Entities
    # ---------------------------------
    print("\n=== FINAL ENTITIES ===")
    print(entities)

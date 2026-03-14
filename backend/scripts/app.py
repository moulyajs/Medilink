from ocr_pipeline import ocr_process
from visit_grouper import group_by_date

from demographics_extraction import extract_demographics
from medicine_extraction import extract_medicines
from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results
from user_review import review_prescriptions
from clinical_facts_extraction import extract_clinical_facts
from ecg_extraction import extract_ecg_findings

# ✅ NEW: DICOM imports
from dicom_viewer import load_dicom, show_dicom_image, extract_dicom_metadata


# ---------------------------------
# ECG detector
# ---------------------------------
def looks_like_ecg(lines):
    text = " ".join(l["text"].lower() for l in lines)
    keywords = [
        "ecg", "hr", "bpm", "qrs", "qt",
        "tachycardia", "bundle branch",
        "axis deviation", "st", "t wave"
    ]
    return sum(k in text for k in keywords) >= 3


# ---------------------------------
# Step 0: INPUT
# ---------------------------------
file_path = "data/knee1.dcm"

is_pdf = file_path.lower().endswith(".pdf")
is_dicom = file_path.lower().endswith(".dcm")


# ---------------------------------
# ✅ NEW: DICOM HANDLING
# ---------------------------------
if is_dicom:
    print("\nINPUT TYPE: DICOM")

    ds = load_dicom(file_path)

    metadata = extract_dicom_metadata(ds)

    print("\n=== DICOM METADATA ===")
    print(metadata)

    print("\nDisplaying DICOM image...")
    show_dicom_image(ds)

    # Stop further processing
    exit()


# ---------------------------------
# Step 1: OCR (only for images)
# ---------------------------------
pages = []
if not is_pdf:
    pages = ocr_process(file_path)
    visits = group_by_date(pages)
else:
    visits = {"PDF_VISIT": []}

print(f"\nINPUT TYPE: {'PDF' if is_pdf else 'IMAGE'}")
print(f"TOTAL VISITS DETECTED: {len(visits)}")


# ---------------------------------
# Step 2: VISIT-WISE PROCESSING
# ---------------------------------
for visit_date, visit_pages in visits.items():

    print("\n" + "=" * 60)
    print(f"VISIT DATE: {visit_date}")
    print("=" * 60)

    visit_lines = []
    doc_types = set()

    for p in visit_pages:
        visit_lines.extend(p["lines"])
        doc_types.add(p["doc_type"])

    # ---------------------------------
    # DEMOGRAPHICS (OCR based)
    # ---------------------------------
    entities = {}
    if visit_lines:
        primary_doc_type = (
            "lab_report"
            if "lab_report" in doc_types
            else list(doc_types)[0]
        )
        entities = extract_demographics(visit_lines, primary_doc_type)

    print("\n=== DEMOGRAPHICS ===")
    print(entities)

    patient_name = entities.get("patient_name", "").lower()
    doctor_name = entities.get("doctor_name", "").lower()

    # ---------------------------------
    # PRESCRIPTIONS (IMAGE ONLY)
    # ---------------------------------
    medicines = []
    if "prescription" in doc_types:
        medicines = extract_medicines(visit_lines)

        filtered = []
        for m in medicines:
            drug = m["drug"].lower()
            if patient_name and patient_name in drug:
                continue
            if doctor_name and doctor_name in drug:
                continue
            filtered.append(m)

        medicines = review_prescriptions(filtered)

    print("\n=== PRESCRIPTIONS ===")
    for m in medicines:
        print(m)

    # ---------------------------------
    # LAB EXTRACTION
    # ---------------------------------
    labs = []

    if is_pdf:
        raw_labs = extract_lab_results(file_path, source="pdf")
    else:
        if "lab_report" in doc_types:
            raw_labs = extract_lab_results(visit_lines, source="image")
        else:
            raw_labs = []

    labs = normalize_lab_results(raw_labs)

    print("\n=== LAB RESULTS ===")
    for l in labs:
        print(l)

    abnormal_labs = [l for l in labs if l.get("abnormal")]

    print("\n=== ABNORMAL LABS ===")
    for l in abnormal_labs:
        print(l)

    # ---------------------------------
    # ECG EXTRACTION (IMAGE ONLY)
    # ---------------------------------
    ecg = None
    if visit_lines and looks_like_ecg(visit_lines):
        ecg = extract_ecg_findings(visit_lines)

    print("\n=== ECG FINDINGS ===")
    print(ecg if ecg else "No ECG data detected")

    # ---------------------------------
    # CLINICAL FACTS (OCR TEXT ONLY)
    # ---------------------------------
    if visit_lines:
        full_text = "\n".join(l["text"] for l in visit_lines)
        clinical_facts = extract_clinical_facts(full_text)
    else:
        clinical_facts = {}

    print("\n=== CLINICAL FACTS ===")
    print(clinical_facts)

    # ---------------------------------
    # FINAL ENTITIES
    # ---------------------------------
    print("\n=== FINAL ENTITIES ===")
    print(entities)

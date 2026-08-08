


import uuid
from scripts.visit_grouper import group_by_date
from scripts.duplicate_detector import is_duplicate_report
from scripts.demographics_extraction import extract_demographics
from scripts.lab_extraction import (
    extract_lab_results,
    extract_date,
    normalize_date
)
from scripts.lab_normalizer import normalize_lab_results
from scripts.clinical_facts_extraction import extract_clinical_facts
from scripts.ecg_extraction import extract_ecg_findings

#from user_review import review_prescriptions
# from clinical_summary import generate_summary

from scripts.uploader import upload_file

from scripts.record_saver import (
    verify_patient,
    save_patient,
    save_lab_results,
    save_medical_record
)

from scripts.timeline_saver import add_timeline_event

from scripts.dicom_viewer import (
    load_dicom,
    show_dicom_image,
    extract_dicom_metadata
)

# NEW: DOCLING PDF PARSER
from scripts.docling_pipeline import parse_pdf_with_docling

# RAG
from scripts.chunking.chunk_router import build_chunks
from scripts.embedding import embed_chunks
from scripts.vector_store import insert_chunks



def looks_like_ecg(lines):
    text = " ".join(l["text"].lower() for l in lines)

    keywords = [
        "ecg", "hr", "bpm", "qrs", "qt",
        "tachycardia", "bundle branch",
        "axis deviation", "st", "t wave"
    ]

    return sum(k in text for k in keywords) >= 3


def process_document(file_path: str, patient_id: str):

    patient_id = str(uuid.UUID(patient_id))

    is_pdf = file_path.lower().endswith(".pdf")
    is_dicom = file_path.lower().endswith(".dcm")

    


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

        
        return {
            "lab_values": [],
            "clinical_notes": [],
            "is_duplicate": False,
        }

# ============================================================
# STEP 2: OCR / DOCLING
# ============================================================

    pages = []
    pdf_data = None

    if not is_pdf:

        print("🔍 Running OCR...")
        from ocr_pipeline import ocr_process
        pages = ocr_process(file_path)
        visits = group_by_date(pages)

    else:

        print("📄 Running Docling PDF parser...")
        pdf_data = parse_pdf_with_docling(file_path)

        # Make PDF look like a single "visit" so downstream code stays similar
        visits = {
            "PDF_VISIT": [
                {
                    "lines": pdf_data.get("lines", []),
                    "doc_type": pdf_data.get("doc_type", "UNKNOWN"),
                    "tables": pdf_data.get("tables", []),
                    "full_text": pdf_data.get("full_text", "")
                }
            ]
        }

    print(f"\nINPUT TYPE: {'PDF' if is_pdf else 'IMAGE'}")
    print(f"TOTAL VISITS: {len(visits)}")

    # ============================================================
    # STEP 3: VISIT-WISE PROCESSING
    # ============================================================

    all_extracted_data = {
        "LAB_REPORT": [],
        "PRESCRIPTION": [],
        "CLINICAL_NOTE": [],
        "RADIOLOGY": []
    }
    last_visit_date = None

    for visit_date, visit_pages in visits.items():

        last_visit_date = visit_date

        print("\n" + "=" * 60)
        print("VISIT DATE:", visit_date)
        print("=" * 60)

        visit_lines = []
        doc_types = set()

        pdf_tables = []
        pdf_full_text = ""

    #save_patient(
    #    patient_id,
    #    entities.get("dob"),
     #   entities.get("gender")
    #)
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

        # ----------------------------------------
        # PDF FLOW (DOCLING)
        # ----------------------------------------
        else:
            pdf_page = visit_pages[0] if visit_pages else {}

            visit_lines = pdf_page.get("lines", [])
            pdf_tables = pdf_page.get("tables", [])
            # print(pdf_tables)
            pdf_full_text = pdf_page.get("full_text", "")
            primary_doc_type = pdf_page.get("doc_type", "UNKNOWN")

            entities = extract_demographics(visit_lines, primary_doc_type)

        print("\n👤 DEMOGRAPHICS")
        print(entities)

        verify_patient(patient_id)

        
        # ----------------------------------------
        # LAB RESULTS
        # ----------------------------------------
        normalized_labs = []

        if is_pdf and primary_doc_type == "LAB_REPORT":

            print("📄 Extracting labs from Docling PDF output...")
            print("\n========== PDF FULL TEXT ==========")
            print(pdf_full_text[:1500])      # print first 1500 characters
            print("==================================")

            print("Extracted report date:",
                normalize_date(extract_date(pdf_full_text)))
            raw_labs = extract_lab_results(
                {
                    "lines": visit_lines,
                    "tables": pdf_tables,
                    "full_text": pdf_full_text
                },
                source="docling"
            )

        elif "LAB_REPORT" in doc_types:

            raw_labs = extract_lab_results(visit_lines)

        else:
            raw_labs = []

    #save_lab_results(
    #    patient_id,
    #    document_id,
    #    normalized_labs
    #)
        normalized_labs = normalize_lab_results(raw_labs)

        print("\n🧪 LAB RESULTS")
        print(normalized_labs)
        if is_duplicate_report(patient_id, normalized_labs):

            return {
            "lab_values": [],
            "clinical_notes": [],
            "is_duplicate": True,
        }
        if normalized_labs:
            print("\n=== FINAL LABS ===")
            for lab in normalized_labs:
                print(lab)

            all_extracted_data["LAB_REPORT"].extend(
                normalized_labs
            )

        

        
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
        ## uncomment when u want to clinical notes
        
        # ----------------------------------------
# CLINICAL FACTS
# ----------------------------------------

        clinical_facts = {}

        if primary_doc_type != "LAB_REPORT":

            if is_pdf:
                full_text = pdf_full_text.strip()
            else:
                full_text = (
            "\n".join(l["text"] for l in visit_lines)
            if visit_lines else ""
        )

            if full_text:
                clinical_facts = extract_clinical_facts(full_text)

        print("\n🧠 CLINICAL FACTS")
        print(clinical_facts)

        if clinical_facts:
            all_extracted_data["CLINICAL_NOTE"].append(
         {
            "report_date": visit_date,
            "facts": clinical_facts,
        })


    return {
    "lab_values": all_extracted_data["LAB_REPORT"],
    "clinical_notes": all_extracted_data["CLINICAL_NOTE"],
    "is_duplicate": False,
}
def save_confirmed_report(
    patient_id: str,
    file_path: str,
    confirmed_lab_values: list,
):

    patient_id = str(uuid.UUID(patient_id))

    verify_patient(patient_id)

    print("\n======================================")
    print("💾 SAVING CONFIRMED REPORT")
    print("======================================")

    document_id, _ = upload_file(
        file_path,
        patient_id
    )

    print("✅ Document stored:", document_id)

    if confirmed_lab_values:
        save_lab_results(
            patient_id,
            document_id,
            confirmed_lab_values
        )

        print("✅ Lab results saved")

        chunks = build_chunks(
            doc_type="LAB_REPORT",
            extracted_data=confirmed_lab_values,
            patient_id=patient_id,
            document_id=document_id,
        )

        if chunks:

            print(f"🧩 Total chunks created: {len(chunks)}")

            embeddings = embed_chunks(chunks)

            insert_chunks(
                chunks,
                embeddings
            )

            print("✅ RAG ingestion completed")

        else:
            print("⚠ No chunks created")
    else:
        print("⚠ No lab values to save")

    

    print("\n======================================")
    print("🎉 REPORT SAVED SUCCESSFULLY")
    print("======================================")

    return {
        "document_id": document_id,
        "is_duplicate": False,
    }
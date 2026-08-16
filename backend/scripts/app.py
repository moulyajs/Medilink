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

from scripts.uploader import upload_file

from scripts.record_saver import (
    verify_patient,
    save_patient,
    save_medical_record
)

from scripts.timeline_saver import add_timeline_event

from scripts.dicom_viewer import (
    load_dicom,
    show_dicom_image,
    extract_dicom_metadata
)

# ============================================================
# DOCLING PDF PARSER
# ============================================================

from scripts.docling_pipeline import parse_pdf_with_docling

# ============================================================
# RAG
# ============================================================

from scripts.chunking.chunk_router import build_chunks
from scripts.embedding import embed_chunks
from scripts.vector_store import insert_chunks


# ============================================================
# ECG DETECTION
# ============================================================

def looks_like_ecg(lines):

    if not lines:
        return False

    text = " ".join(
        l.get("text", "").lower()
        for l in lines
        if isinstance(l, dict)
    )

    keywords = [
        "ecg",
        "hr",
        "bpm",
        "qrs",
        "qt",
        "tachycardia",
        "bundle branch",
        "axis deviation",
        "st",
        "t wave"
    ]

    return sum(
        k in text
        for k in keywords
    ) >= 3


# ============================================================
# PROCESS DOCUMENT
# ============================================================

def process_document(
    file_path: str,
    patient_id: str
):

    # --------------------------------------------------------
    # Validate patient UUID
    # --------------------------------------------------------

    patient_id = str(
        uuid.UUID(patient_id)
    )

    is_pdf = file_path.lower().endswith(".pdf")
    is_dicom = file_path.lower().endswith(".dcm")

    # ========================================================
    # STEP 1: DICOM HANDLING
    # ========================================================

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

    # ========================================================
    # STEP 2: OCR / DOCLING
    # ========================================================

    pages = []
    pdf_data = None

    # --------------------------------------------------------
    # IMAGE / OCR
    # --------------------------------------------------------

    if not is_pdf:

        print("\n🔍 Running OCR...")

        from ocr_pipeline import ocr_process

        pages = ocr_process(
            file_path
        )

        visits = group_by_date(
            pages
        )

    # --------------------------------------------------------
    # PDF / DOCLING
    # --------------------------------------------------------

    else:

        print(
            "\n📄 Running Docling PDF parser..."
        )

        pdf_data = parse_pdf_with_docling(
            file_path
        )

        # Treat PDF as one visit
        visits = {
            "PDF_VISIT": [
                {
                    "lines": pdf_data.get(
                        "lines",
                        []
                    ),

                    "doc_type": pdf_data.get(
                        "doc_type",
                        "UNKNOWN"
                    ),

                    "tables": pdf_data.get(
                        "tables",
                        []
                    ),

                    "full_text": pdf_data.get(
                        "full_text",
                        ""
                    )
                }
            ]
        }

    print(
        f"\nINPUT TYPE: "
        f"{'PDF' if is_pdf else 'IMAGE'}"
    )

    print(
        f"TOTAL VISITS: {len(visits)}"
    )

    # ========================================================
    # STEP 3: INITIALIZE RESULT
    # ========================================================

    all_extracted_data = {

        "LAB_REPORT": [],

        "PRESCRIPTION": [],

        "CLINICAL_NOTE": [],

        "RADIOLOGY": []
    }

    last_visit_date = None

    # ========================================================
    # STEP 4: VISIT-WISE PROCESSING
    # ========================================================

    for visit_date, visit_pages in visits.items():

        last_visit_date = visit_date

        print(
            "\n" + "=" * 60
        )

        print(
            "VISIT DATE:",
            visit_date
        )

        print(
            "=" * 60
        )

        # ----------------------------------------------------
        # Initialize
        # ----------------------------------------------------

        visit_lines = []

        doc_types = set()

        pdf_tables = []

        pdf_full_text = ""

        primary_doc_type = "UNKNOWN"

        # For PDF this will contain the actual report date.
        report_date = None

        # ====================================================
        # IMAGE FLOW
        # ====================================================

        if not is_pdf:

            for p in visit_pages:

                if not isinstance(p, dict):
                    continue

                visit_lines.extend(
                    p.get("lines", [])
                )

                if p.get("doc_type"):
                    doc_types.add(
                        p.get("doc_type")
                    )

            # -----------------------------------------------
            # Determine document type
            # -----------------------------------------------

            if not doc_types:

                print(
                    "⚠️ No document types detected."
                )

                continue

            if "LAB_REPORT" in doc_types:

                primary_doc_type = "LAB_REPORT"

            elif "PRESCRIPTION" in doc_types:

                primary_doc_type = "PRESCRIPTION"

            else:

                primary_doc_type = list(
                    doc_types
                )[0]

            # -----------------------------------------------
            # Demographics
            # -----------------------------------------------

            entities = extract_demographics(
                visit_lines,
                primary_doc_type
            )

        # ====================================================
        # PDF FLOW
        # ====================================================

        else:

            pdf_page = (
                visit_pages[0]
                if visit_pages
                else {}
            )

            visit_lines = pdf_page.get(
                "lines",
                []
            )

            pdf_tables = pdf_page.get(
                "tables",
                []
            )

            pdf_full_text = pdf_page.get(
                "full_text",
                ""
            )

            primary_doc_type = pdf_page.get(
                "doc_type",
                "UNKNOWN"
            )

            # -----------------------------------------------
            # PDF may be UNKNOWN.
            # Still extract labs.
            # -----------------------------------------------

            print(
                "PDF PRIMARY DOC TYPE:",
                primary_doc_type
            )

            print(
                "PDF TABLE COUNT:",
                len(pdf_tables)
            )

            print(
                "PDF LINE COUNT:",
                len(visit_lines)
            )

            print(
                "PDF TEXT LENGTH:",
                len(pdf_full_text)
            )

            # -----------------------------------------------
            # Demographics
            # -----------------------------------------------

            entities = extract_demographics(
                visit_lines,
                primary_doc_type
            )

        # ====================================================
        # DEMOGRAPHICS
        # ====================================================

        print(
            "\n👤 DEMOGRAPHICS"
        )

        print(
            entities
        )

        # ====================================================
        # VERIFY PATIENT
        # ====================================================

        verify_patient(
            patient_id
        )

        # ====================================================
        # LAB RESULTS
        # ====================================================

        print(
            "\n" + "=" * 60
        )

        print(
            "🧪 STARTING LAB EXTRACTION"
        )

        print(
            "=" * 60
        )

        raw_labs = []

        normalized_labs = []

        # ====================================================
        # PDF LAB EXTRACTION
        # ====================================================

        if is_pdf:

            print(
                "\n📄 Extracting labs from "
                "Docling PDF output..."
            )

            # -----------------------------------------------
            # Print PDF text
            # -----------------------------------------------

            print(
                "\n========== PDF FULL TEXT =========="
            )

            print(
                pdf_full_text[:3000]
            )

            print(
                "==================================="
            )

            # -----------------------------------------------
            # Extract report date
            # -----------------------------------------------

            report_date = normalize_date(
                extract_date(
                    pdf_full_text
                )
            )

            print(
                "\nExtracted report date:",
                report_date
            )

            # -----------------------------------------------
            # Extract labs from Docling
            # -----------------------------------------------

            raw_labs = extract_lab_results(
                {
                    "lines": visit_lines,

                    "tables": pdf_tables,

                    "full_text": pdf_full_text
                },

                source="docling"
            )

        # ====================================================
        # IMAGE / OCR LAB EXTRACTION
        # ====================================================

        elif "LAB_REPORT" in doc_types:

            print(
                "\n📄 Extracting labs "
                "from OCR output..."
            )

            raw_labs = extract_lab_results(
                visit_lines
            )

        # ====================================================
        # NON LAB IMAGE
        # ====================================================

        else:

            print(
                "\n⚠️ Document is not "
                "classified as LAB_REPORT."
            )

            raw_labs = []

        # ====================================================
        # RAW LAB DEBUG
        # ====================================================

        print(
            "\n========== RAW LAB RESULTS =========="
        )

        print(
            "RAW LAB COUNT:",
            len(raw_labs)
        )

        for lab in raw_labs:

            print(
                lab
            )

        print(
            "====================================="
        )

        # ====================================================
        # NORMALIZE LABS
        # ====================================================

        if raw_labs:

            normalized_labs = (
                normalize_lab_results(
                    raw_labs
                )
            )

        else:

            normalized_labs = []

        # ====================================================
        # IMPORTANT:
        # Make sure the report date is preserved
        # after normalization.
        # ====================================================

        if normalized_labs and report_date:

            for lab in normalized_labs:

                if isinstance(lab, dict):

                    lab["date"] = report_date

        # ====================================================
        # For IMAGE/OCR reports:
        # try to obtain date from extracted labs.
        # ====================================================

        if normalized_labs and not report_date:

            for lab in normalized_labs:

                if not isinstance(lab, dict):
                    continue

                lab_date = lab.get("date")

                if lab_date:

                    report_date = lab_date

                    break

        print(
            "\nFinal report date:",
            report_date
        )

        # ====================================================
        # FINAL LAB DEBUG
        # ====================================================

        print(
            "\n🧪 NORMALIZED LAB RESULTS"
        )

        print(
            normalized_labs
        )

        print(
            "\nFINAL LAB COUNT:",
            len(normalized_labs)
        )

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        if normalized_labs:

            print(
                "\n========== DUPLICATE CHECK =========="
            )

            duplicate = is_duplicate_report(
                patient_id,
                normalized_labs
            )

            if duplicate:

                print(
                    "⚠️ DUPLICATE REPORT DETECTED"
                )

                return {
                    "lab_values": [],

                    "clinical_notes": [],

                    "is_duplicate": True,
                }

        else:

            print(
                "\n⚠️ No lab values."
            )

            print(
                "Skipping duplicate detection."
            )

        # ====================================================
        # SAVE EXTRACTED LABS FOR RESPONSE
        # ====================================================

        if normalized_labs:

            print(
                "\n=== FINAL LABS ==="
            )

            for lab in normalized_labs:

                print(
                    lab
                )

            all_extracted_data[
                "LAB_REPORT"
            ].extend(
                normalized_labs
            )

        else:

            print(
                "\n⚠️ NO LAB VALUES EXTRACTED"
            )

        # ====================================================
        # ECG
        # ====================================================

        ecg_data = None

        if (
            not is_pdf
            and visit_lines
            and looks_like_ecg(
                visit_lines
            )
        ):

            ecg_data = (
                extract_ecg_findings(
                    visit_lines
                )
            )

        print(
            "\n🫀 ECG FINDINGS"
        )

        print(
            ecg_data
        )

        # ====================================================
        # CLINICAL FACTS
        # ====================================================

        clinical_facts = {}

        should_extract_clinical_facts = (
            primary_doc_type
            not in (
                "LAB_REPORT",
                "UNKNOWN"
            )
        )

        if should_extract_clinical_facts:

            if is_pdf:

                full_text = (
                    pdf_full_text.strip()
                )

            else:

                full_text = (
                    "\n".join(
                        l.get(
                            "text",
                            ""
                        )

                        for l in visit_lines

                        if isinstance(
                            l,
                            dict
                        )
                    )
                )

            if full_text:

                try:

                    clinical_facts = (
                        extract_clinical_facts(
                            full_text
                        )
                    )

                except Exception as e:

                    print(
                        "⚠️ Clinical facts "
                        "extraction failed:",
                        e
                    )

                    clinical_facts = {}

        else:

            print(
                "\nℹ️ Skipping clinical facts "
                "extraction for:"
            )

            print(
                primary_doc_type
            )

        print(
            "\n🧠 CLINICAL FACTS"
        )

        print(
            clinical_facts
        )

        # ====================================================
        # SAVE CLINICAL NOTES
        # ====================================================

        if clinical_facts:

            all_extracted_data[
                "CLINICAL_NOTE"
            ].append(
                {
                    "report_date":
                        report_date
                        if report_date
                        else visit_date,

                    "facts":
                        clinical_facts,
                }
            )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    print(
        "\n" + "=" * 60
    )

    print(
        "🎯 PROCESS DOCUMENT COMPLETED"
    )

    print(
        "=" * 60
    )

    print(
        "TOTAL FINAL LABS:",
        len(
            all_extracted_data[
                "LAB_REPORT"
            ]
        )
    )

    print(
        "TOTAL CLINICAL NOTES:",
        len(
            all_extracted_data[
                "CLINICAL_NOTE"
            ]
        )
    )

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "lab_values":
            all_extracted_data[
                "LAB_REPORT"
            ],

        "clinical_notes":
            all_extracted_data[
                "CLINICAL_NOTE"
            ],

        "is_duplicate":
            False,
    }


# ============================================================
# SAVE CONFIRMED REPORT
# ============================================================

def save_confirmed_report(
    patient_id: str,
    file_path: str,
    confirmed_lab_values: list,
):

    # --------------------------------------------------------
    # Validate UUID
    # --------------------------------------------------------

    patient_id = str(
        uuid.UUID(patient_id)
    )

    # --------------------------------------------------------
    # Verify patient
    # --------------------------------------------------------

    verify_patient(
        patient_id
    )

    print(
        "\n======================================"
    )

    print(
        "💾 SAVING CONFIRMED REPORT"
    )

    print(
        "======================================"
    )

    # ========================================================
    # UPLOAD FILE
    # ========================================================

    document_id, stored_name = upload_file(
        file_path,
        patient_id
    )

    print(
        "✅ Document stored:",
        document_id
    )

    print(
        "✅ Stored file:",
        stored_name
    )

    # ========================================================
    # SAVE LAB RESULTS
    # ========================================================

    if confirmed_lab_values:

        print(
            "\n💾 Saving confirmed lab values..."
        )

        save_medical_record(
            patient_id=patient_id,
            file_id=document_id,
            document_type="LAB_REPORT",
            labs=confirmed_lab_values,
            clinical_facts={}
        )

        print(
            "✅ Lab results saved"
        )

    else:

        print(
            "⚠️ No lab values to save"
        )

    # ========================================================
    # TIMELINE
    # ========================================================

    print(
        "\n📅 Updating medical timeline..."
    )

    # --------------------------------------------------------
    # Find report date from confirmed values
    # --------------------------------------------------------

    report_date = None

    if confirmed_lab_values:

        for lab in confirmed_lab_values:

            if not isinstance(lab, dict):
                continue

            lab_date = lab.get("date")

            if lab_date:

                report_date = lab_date

                break

    # --------------------------------------------------------
    # IMPORTANT:
    # Do NOT manually use date.today() here.
    #
    # timeline_saver.py will use NOW() automatically
    # when event_date is None.
    # --------------------------------------------------------

    print(
        "Timeline patient:",
        patient_id
    )

    print(
        "Timeline document:",
        document_id
    )

    print(
        "Timeline type:",
        "LAB_REPORT"
    )

    if report_date:

        print(
            "📅 Report date found:",
            report_date
        )

    else:

        print(
            "📅 No report date found."
        )

        print(
            "📅 Timeline will use upload date."
        )

    # ========================================================
    # SAVE TIMELINE EVENT
    # ========================================================

    try:

        add_timeline_event(
            patient_id=patient_id,
            document_id=document_id,
            event_type="LAB_REPORT",
            summary="Lab Report",
            event_date=report_date
        )

        print(
            "✅ Timeline updated"
        )

    except Exception as e:

        print(
            "⚠️ Timeline update failed:",
            e
        )

    # ========================================================
    # RAG CHUNKS
    # ========================================================

    if confirmed_lab_values:

        try:

            chunks = build_chunks(
                doc_type="LAB_REPORT",

                extracted_data=
                    confirmed_lab_values,

                patient_id=
                    patient_id,

                document_id=
                    document_id,
            )

            if chunks:

                print(
                    f"🧩 Total chunks created: "
                    f"{len(chunks)}"
                )

                embeddings = embed_chunks(
                    chunks
                )

                insert_chunks(
                    chunks,
                    embeddings
                )

                print(
                    "✅ RAG ingestion completed"
                )

            else:

                print(
                    "⚠️ No chunks created"
                )

        except Exception as e:

            print(
                "⚠️ RAG ingestion failed:",
                e
            )

    # ========================================================
    # FINAL
    # ========================================================

    print(
        "\n======================================"
    )

    print(
        "🎉 REPORT SAVED SUCCESSFULLY"
    )

    print(
        "======================================"
    )

    return {

        "document_id":
            document_id,

        "is_duplicate":
            False,
    }
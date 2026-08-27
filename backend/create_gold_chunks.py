import json
import csv
import glob
import os

from scripts.chunking.chunk_router import build_chunks


# ============================================================
# CONFIGURATION
# ============================================================

CORPUS_DIR = "corpus"
OUTPUT_CSV = "gold_chunks.csv"


# ============================================================
# PROCESS ONE JSON FILE
# ============================================================

def process_json(json_path):

    # --------------------------------------------------------
    # Load JSON
    # --------------------------------------------------------

    with open(
        json_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    # --------------------------------------------------------
    # Get IDs from JSON
    # --------------------------------------------------------

    patient_id = data["patient_id"]

    document_id = data["document_id"]

    doc_type = data["doc_type"]

    # --------------------------------------------------------
    # Prepare data for chunk router
    # --------------------------------------------------------

    if doc_type == "LAB_REPORT":

        extracted_data = data["labs"]

    elif doc_type == "CLINICAL_NOTE":

        extracted_data = data["clinical_notes"]

    else:

        print(
            f"⚠️ Unsupported document type: {doc_type}"
        )

        return []

    # --------------------------------------------------------
    # Run YOUR existing chunking implementation
    # --------------------------------------------------------

    chunks = build_chunks(
        doc_type=doc_type,

        extracted_data=extracted_data,

        patient_id=patient_id,

        document_id=document_id
    )

    print(
        f"{json_path} → {len(chunks)} chunks"
    )

    # --------------------------------------------------------
    # Convert chunks to CSV rows
    # --------------------------------------------------------

    rows = []

    for index, chunk in enumerate(chunks):

        rows.append({

            "patient_id":
                patient_id,

            "document_id":
                document_id,

            "source_file":
                json_path,

            "chunk_index":
                index + 1,

            "report_type":
                chunk.get("report_type"),

            "chunk_type":
                chunk.get("chunk_type"),

            "chunk_level":
                chunk.get("chunk_level"),

            "report_date":
                chunk.get("report_date"),

            "chunk_text":
                chunk.get("text")
        })

    return rows


# ============================================================
# PROCESS ENTIRE CORPUS
# ============================================================

def create_gold_chunks():

    all_rows = []

    # --------------------------------------------------------
    # Find every JSON file
    # --------------------------------------------------------

    json_files = glob.glob(
        os.path.join(
            CORPUS_DIR,
            "**",
            "*.json"
        ),
        recursive=True
    )

    print(
        f"\nFound {len(json_files)} JSON files"
    )

    # --------------------------------------------------------
    # Process every JSON
    # --------------------------------------------------------

    for json_path in sorted(json_files):

        try:

            rows = process_json(
                json_path
            )

            all_rows.extend(rows)

        except Exception as e:

            print(
                f"\n❌ Failed: {json_path}"
            )

            print(
                f"Error: {e}"
            )

    # ========================================================
    # WRITE CSV
    # ========================================================

    fieldnames = [
        "patient_id",
        "document_id",
        "source_file",
        "chunk_index",
        "report_type",
        "chunk_type",
        "chunk_level",
        "report_date",
        "chunk_text"
    ]

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(all_rows)

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 60)

    print(
        f"JSON files processed : {len(json_files)}"
    )

    print(
        f"Total chunks         : {len(all_rows)}"
    )

    print(
        f"Output               : {OUTPUT_CSV}"
    )

    print(
        "✅ Gold chunk dataset created"
    )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    create_gold_chunks()
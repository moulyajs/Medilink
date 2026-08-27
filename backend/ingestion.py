import json

from scripts.chunking.chunk_router import build_chunks
from scripts.embedding import embed_chunks
from scripts.vector_store import insert_chunks
from scripts.lab_results_saver import save_lab_results


def ingest_verified_record(json_path):

    # =====================================================
    # LOAD VERIFIED JSON
    # =====================================================

    with open(
        json_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    # =====================================================
    # READ IDENTIFIERS FROM JSON
    # =====================================================

    patient_id = data["patient_id"]
    document_id = data["document_id"]
    doc_type = data["doc_type"]

    print("\n" + "=" * 80)
    print("INGESTING VERIFIED RECORD")
    print("=" * 80)

    print("JSON file    :", json_path)
    print("Patient ID   :", patient_id)
    print("Document ID  :", document_id)
    print("Document Type:", doc_type)

    # =====================================================
    # PREPARE EXTRACTED DATA
    # =====================================================

    if doc_type == "LAB_REPORT":

        extracted_data = data["labs"]

    elif doc_type == "CLINICAL_NOTE":

        extracted_data = data["clinical_notes"]

    else:

        print(
            f"❌ Unsupported document type: {doc_type}"
        )

        return

    # =====================================================
    # SAVE LAB RESULTS TO SUPABASE
    # =====================================================

    if doc_type == "LAB_REPORT":

        print("\n" + "-" * 80)
        print("SAVING LAB RESULTS TO SUPABASE")
        print("-" * 80)

        save_lab_results(
            patient_id=patient_id,
            document_id=document_id,
            labs=extracted_data
        )

        print(
            "✅ Lab results saved to Supabase"
        )

    # =====================================================
    # BUILD CHUNKS
    # =====================================================

    print("\n" + "-" * 80)
    print("BUILDING CHUNKS")
    print("-" * 80)

    chunks = build_chunks(
        doc_type=doc_type,
        extracted_data=extracted_data,
        patient_id=patient_id,
        document_id=document_id
    )

    print(
        f"✅ Created {len(chunks)} chunks"
    )

    # =====================================================
    # SHOW CHUNKS
    # =====================================================

    for i, chunk in enumerate(
        chunks,
        start=1
    ):

        print("\n" + "=" * 60)

        print(
            f"Chunk {i}"
        )

        print(
            "Chunk ID     :",
            chunk["chunk_id"]
        )

        print(
            "Patient ID   :",
            chunk["patient_id"]
        )

        print(
            "Document ID  :",
            chunk["document_id"]
        )

        print(
            "Chunk Type   :",
            chunk["chunk_type"]
        )

        print(
            "Chunk Level  :",
            chunk["chunk_level"]
        )

        print(
            "Report Date  :",
            chunk["report_date"]
        )

        print(
            "Text         :"
        )

        print(
            chunk["text"]
        )

    # =====================================================
    # GENERATE EMBEDDINGS
    # =====================================================

    print("\n" + "-" * 80)
    print("GENERATING EMBEDDINGS")
    print("-" * 80)

    embeddings = embed_chunks(
        chunks
    )

    print(
        f"✅ Generated {len(embeddings)} embeddings"
    )

    # =====================================================
    # INSERT INTO QDRANT
    # =====================================================

    print("\n" + "-" * 80)
    print("INSERTING CHUNKS INTO QDRANT")
    print("-" * 80)

    insert_chunks(
        chunks,
        embeddings
    )

    print(
        "✅ Chunks inserted into Qdrant"
    )

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    print("\n" + "=" * 80)
    print("INGESTION COMPLETE")
    print("=" * 80)

    print(
        "Patient ID   :",
        patient_id
    )

    print(
        "Document ID  :",
        document_id
    )

    print(
        "Document Type:",
        doc_type
    )

    print(
        "Chunks       :",
        len(chunks)
    )

    print(
        "\n✅ Supabase + Qdrant ingestion completed successfully."
    )


# ============================================================
# RUN ALL R*.JSON FILES
# ============================================================

import glob


if __name__ == "__main__":

    json_files = sorted(
        glob.glob(
            "corpus/user009/r*.json"
        )
    )

    print(
        f"\nFound {len(json_files)} JSON files"
    )

    for json_path in json_files:

        print("\n" + "=" * 100)

        print(
            "PROCESSING:",
            json_path
        )

        print("=" * 100)

        try:

            ingest_verified_record(
                json_path
            )

        except Exception as e:

            print(
                f"\n❌ Failed to process {json_path}"
            )

            print(
                "Error:",
                e
            )

            continue

    print("\n" + "=" * 100)
    print("ALL JSON FILES PROCESSED")
    print("=" * 100)
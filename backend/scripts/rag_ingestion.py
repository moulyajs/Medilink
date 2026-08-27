import json

from chunking.chunk_router import build_chunks
from embedding import embed_chunks
from vector_store import insert_chunks


def ingest_rag_only(json_path):

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
    print("RAG-ONLY INGESTION")
    print("=" * 80)

    print("JSON file     :", json_path)
    print("Patient ID    :", patient_id)
    print("Document ID   :", document_id)
    print("Document Type :", doc_type)

    # =====================================================
    # ONLY CLINICAL NOTES ARE ALLOWED
    # =====================================================

    if doc_type != "CLINICAL_NOTE":

        print(
            "\n❌ This file is not a CLINICAL_NOTE."
        )

        print(
            "Expected: CLINICAL_NOTE"
        )

        print(
            "Found:",
            doc_type
        )

        return

    # =====================================================
    # GET CLINICAL NOTES
    # =====================================================

    clinical_notes = data.get(
        "clinical_notes",
        []
    )

    if not clinical_notes:

        print(
            "\n⚠️ No clinical notes found."
        )

        return

    print(
        f"\nClinical note records: "
        f"{len(clinical_notes)}"
    )

    # =====================================================
    # BUILD CHUNKS
    # =====================================================

    print("\n" + "-" * 80)
    print("BUILDING CLINICAL CHUNKS")
    print("-" * 80)

    chunks = build_chunks(
        doc_type="CLINICAL_NOTE",

        extracted_data=clinical_notes,

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

        print("\n" + "=" * 70)

        print(
            f"CHUNK {i}"
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
            "Report Type  :",
            chunk["report_type"]
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
            "\nTEXT:"
        )

        print(
            chunk["text"]
        )

        print(
            "\nMETADATA:"
        )

        print(
            chunk["metadata"]
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
    # INSERT INTO QDRANT ONLY
    # =====================================================

    print("\n" + "-" * 80)
    print("INSERTING INTO QDRANT")
    print("-" * 80)

    insert_chunks(
        chunks,
        embeddings
    )

    print(
        "✅ Clinical chunks inserted into Qdrant"
    )

    # =====================================================
    # FINAL
    # =====================================================

    print("\n" + "=" * 80)
    print("RAG-ONLY INGESTION COMPLETE")
    print("=" * 80)

    print(
        "Patient ID  :",
        patient_id
    )

    print(
        "Document ID :",
        document_id
    )

    print(
        "Chunks      :",
        len(chunks)
    )

    print(
        "\n✅ Supabase was NOT modified."
    )


# ============================================================
# RUN ALL C*.JSON FILES
# ============================================================

import glob


if __name__ == "__main__":

    json_files = sorted(
        glob.glob(
            "corpus/user007/c*.json"
        )
    )

    print(
        f"\nFound {len(json_files)} clinical note JSON files"
    )

    for json_path in json_files:

        print("\n" + "=" * 100)

        print(
            "PROCESSING:",
            json_path
        )

        print("=" * 100)

        try:

            ingest_rag_only(
                json_path
            )

        except Exception as e:

            print(
                f"\n❌ Failed to process:"
            )

            print(
                json_path
            )

            print(
                "Error:",
                e
            )

            continue

    print("\n" + "=" * 100)
    print("ALL CLINICAL NOTE FILES PROCESSED")
    print("=" * 100)
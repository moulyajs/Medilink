from .embeddings import get_embedding

from .vector_store import (
    search_qdrant,
    keyword_search_qdrant,
)

from .keyword_search import extract_keywords

from .rrf import rrf_fusion
from .hybrid_search import apply_recency


def retrieve(
    query,
    patient_id,
    task=None,
):

    # ---------------------------------------------------
    # Decide which chunk types to search
    # ---------------------------------------------------

    chunk_types = None

    if task:

        intent = task.get("intent")

        if intent in [
            "LATEST_VALUE",
            "TREND",
            "ABNORMAL_LABS",
        ]:

            chunk_types = [
                "lab_row",
                "lab_summary",
            ]

    # ---------------------------------------------------
    # Vector Search
    # ---------------------------------------------------

    query_embedding = get_embedding(query)

    vector_results = search_qdrant(
        query_embedding=query_embedding,
        patient_id=patient_id,
        chunk_types=chunk_types,
        limit=30,
    )

    vector_chunks = []

    for r in vector_results:

        vector_chunks.append(
            {
                "chunk_id": r.payload.get("chunk_id"),
                "text": r.payload.get("text"),
                "chunk_type": r.payload.get("chunk_type"),
                "chunk_level": r.payload.get("chunk_level"),
                "report_type": r.payload.get("report_type"),
                "document_id": r.payload.get("document_id"),
                "report_date": r.payload.get("report_date"),
                "metadata": r.payload.get("metadata", {}),
                "score": r.score,
            }
        )

    # ---------------------------------------------------
    # Keyword Search
    # ---------------------------------------------------

    keyword_chunks = []

    keywords = extract_keywords(query)

    print("KEYWORDS:", keywords)

    for keyword in keywords:

        matches = keyword_search_qdrant(
            patient_id,
            keyword,
            chunk_types=chunk_types,
            limit=10,
        )

        for r in matches:

            keyword_chunks.append(
                {
                    "chunk_id": r.payload.get("chunk_id"),
                    "text": r.payload.get("text"),
                    "chunk_type": r.payload.get("chunk_type"),
                    "chunk_level": r.payload.get("chunk_level"),
                    "report_type": r.payload.get("report_type"),
                    "document_id": r.payload.get("document_id"),
                    "report_date": r.payload.get("report_date"),
                    "metadata": r.payload.get("metadata", {}),
                    "score": 1.0,
                }
            )

    # ---------------------------------------------------
    # Reciprocal Rank Fusion
    # ---------------------------------------------------

    fused = rrf_fusion(
        vector_chunks,
        keyword_chunks,
    )

    # ---------------------------------------------------
    # Recency Boost
    # ---------------------------------------------------

    final_chunks = apply_recency(fused)

    return final_chunks[:20]
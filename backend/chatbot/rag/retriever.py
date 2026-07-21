from .embeddings import get_embedding

from .vector_store import (
    search_qdrant,
    keyword_search_qdrant
)

from .keyword_search import (
    extract_keywords
)

from .rrf import rrf_fusion

from .hybrid_search import (
    apply_recency
)


def retrieve(
    query,
    patient_id,
    analysis=None

):

    # ---------------------
    # VECTOR SEARCH
    # ---------------------

    query_embedding = get_embedding(
        query
    )

    chunk_types = None

    if analysis:

        intent = analysis.get("intent")

        if intent in [
        "LATEST_VALUE",
        "TREND",
        "ABNORMAL_LABS"
        ]:

            chunk_types = [
            "lab_row",
            "lab_summary"
        ]

    vector_results = search_qdrant(
    query_embedding=query_embedding,
    patient_id=patient_id,
    chunk_types=chunk_types,
    limit=30
)
    """
    print("\n" + "="*80)
    print("VECTOR SEARCH RESULTS")
    print("="*80)

    for i, r in enumerate(vector_results[:10], start=1):

        print(
        f"\n[{i}] Score={round(r.score,4)}"
    )

        print(
        "Date:",
        r.payload.get("report_date")
    )

        print(
        "Type:",
        r.payload.get("chunk_type")
    )

        print(
        "Text:",
        r.payload.get("text","")[:200]
    )
    """

    vector_chunks = []

    for r in vector_results:

        vector_chunks.append({
            "chunk_id":
                r.payload.get("chunk_id"),

            "text":
                r.payload.get("text"),

            "chunk_type":
                r.payload.get("chunk_type"),

            "chunk_level":
                r.payload.get("chunk_level"),

            "report_type":
                r.payload.get("report_type"),

            "document_id":
                r.payload.get("document_id"),

            "report_date":
                r.payload.get("report_date"),

            "metadata":
                r.payload.get(
                    "metadata",
                    {}
                ),

            "score":
                r.score
        })

    # ---------------------
    # KEYWORD SEARCH
    # ---------------------

    keyword_chunks = []

    keywords = extract_keywords(
        query
    )
    print("KEYWORDS:", keywords)
    for keyword in keywords:

        matches = keyword_search_qdrant(
            patient_id,
            keyword,
            limit=10
        )
        
        for r in matches:

            keyword_chunks.append({
                "chunk_id":
                    r.payload.get("chunk_id"),

                "text":
                    r.payload.get("text"),

                "chunk_type":
                    r.payload.get("chunk_type"),

                "chunk_level":
                    r.payload.get("chunk_level"),

                "report_type":
                    r.payload.get("report_type"),

                "document_id":
                    r.payload.get("document_id"),

                "report_date":
                    r.payload.get("report_date"),

                "metadata":
                    r.payload.get(
                        "metadata",
                        {}
                    ),

                "score": 1.0
            })
    """
    print("\n" + "="*80)
    print("KEYWORD SEARCH RESULTS")
    print("="*80)

    for i, chunk in enumerate(
    keyword_chunks[:20],
    start=1
):

        print(f"\n[{i}]")

        print(
        "Date:",
        chunk["report_date"]
    )

        print(
        "Type:",
        chunk["chunk_type"]
    )

        print(
        chunk["text"][:200]
    )
    
    """
    # ---------------------
    # FUSION
    # ---------------------

    fused = rrf_fusion(
        vector_chunks,
        keyword_chunks
    )
    """
    print("\n" + "="*80)
    print("RRF FUSION RESULTS")
    print("="*80)

    for i, item in enumerate(
    fused[:20],
    start=1
):

        print(
        f"\n[{i}] RRF={item['score']:.5f}"
    )

        print(
        item["chunk"]["report_date"]
    )

        print(
        item["chunk"]["text"][:200]
    )
    """
    # ---------------------
    # RECENCY
    # ---------------------

    final_chunks = apply_recency(
        fused
    )

    return final_chunks[:20]
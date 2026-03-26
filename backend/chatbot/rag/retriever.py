from .embeddings import get_embedding
from .vector_store import search_qdrant


def retrieve(query: str, patient_id: str):
    query_embedding = get_embedding(query)

    try:
        results = search_qdrant(
            query_embedding=query_embedding,
            patient_id=patient_id,
            limit=10
        )
    except Exception as e:
        print("⚠ Qdrant error:", e)
        return []

    # ✅ Handle empty results
    if not results:
        return []

    chunks = []
    for r in results:
        chunks.append({
            "text": r.payload.get("text"),
            "document_id": r.payload.get("document_id"),
            "report_date": r.payload.get("report_date"),
            "score": r.score
        })

    return chunks
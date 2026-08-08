from .rag import handle_rag
from ..time_retriever import get_latest_lab


def handle_latest(task, patient_id, query):

    entity = task.get("entity")

    latest = get_latest_lab(
        patient_id,
        entity
    )

    # Exact match found
    if latest:
        return {
            "type": "latest",
            "content": latest.payload["text"]
        }

    # Fallback to RAG
    rag_response = handle_rag(
        task,
        patient_id,
        query
    )

    if rag_response.get("chunks"):
        return {
            "type": "latest",
            "content": rag_response["content"],
            "chunks": rag_response["chunks"]
        }

    return {
        "type": "latest",
        "content": f"I couldn't find any {entity} results in your records."
    }
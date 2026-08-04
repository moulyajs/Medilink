from ..retriever import retrieve
from ..reranker import rerank
from ..context_builder import build_context
from ..prompts import build_rag_prompt
from ..llm import generate_answer


def handle_rag(task, patient_id, query):

    chunks = retrieve(
        query,
        patient_id,
        task
    )

    if not chunks:
        return {
            "type": "rag",
            "content": "No relevant medical data found.",
            "chunks": []
        }

    reranked_chunks = rerank(
        query,
        chunks,
        top_k=5
    )

    context = build_context(
        reranked_chunks
    )

    prompt = build_rag_prompt(
        context,
        query
    )

    answer = generate_answer(prompt)

    return {
        "type": "rag",
        "content": answer,
        "chunks": reranked_chunks
    }
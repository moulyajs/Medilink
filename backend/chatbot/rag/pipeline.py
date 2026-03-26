from .retriever import retrieve
from .reranker import rerank
from .context_builder import build_context
from .prompts import build_rag_prompt
from .llm import generate_answer


def rewrite_query(query, chat_history):
    if not chat_history:
        return query

    history_text = " ".join([m["content"] for m in chat_history[-4:]])
    return f"{history_text} {query}"


def rag_pipeline(query: str, patient_id: str, chat_history: list):

    # 🔥 Step 0: Rewrite query using history
    rewritten_query = rewrite_query(query, chat_history)

    # Step 1: Retrieve
    chunks = retrieve(rewritten_query, patient_id)

    if not chunks:
        return {
            "answer": "No relevant medical data found.",
            "chunks": []
        }

    # Step 2: Rerank
    reranked_chunks = rerank(query, chunks, top_k=5)

    # Step 3: Build context
    context = build_context(reranked_chunks)

    # Step 4: Prompt
    prompt = build_rag_prompt(context, query, chat_history)

    # Step 5: Generate answer
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "chunks": reranked_chunks
    }
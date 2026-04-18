from .retriever import retrieve
from .reranker import rerank
from .context_builder import build_context
from .prompts import build_rag_prompt
from .llm import generate_answer

# ✅ ONLY this agent
from chatbot.agents.prompt_guard_agent import PromptGuardAgent


# 🔐 Initialize once
guard = PromptGuardAgent()


def is_sensitive_output(answer: str) -> bool:
    sensitive_patterns = [
        "system rules",
        "you are a medical assistant",
        "hidden instructions",
        "internal policy",
        "prompt"
    ]

    answer = answer.lower()
    return any(p in answer for p in sensitive_patterns)


def rewrite_query(query, chat_history):
    if not chat_history:
        return query

    history_text = " ".join([m["content"] for m in chat_history[-4:]])
    return f"{history_text} {query}"


def rag_pipeline(query: str, patient_id: str, chat_history: list):

    # 🚧 ONLY Agent: Prompt Guard
    if guard.detect(query):
        return {
            "answer": "⚠️ Security Alert: Query blocked due to potential prompt injection.",
            "chunks": []
        }

    # 🔥 Step 0: Rewrite query
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

    # 🚨 Output Guard (KEEP THIS — important even with one agent)
    if is_sensitive_output(answer):
        return {
            "answer": "⚠️ Security Alert: Response blocked due to sensitive information leakage.",
            "chunks": []
        }

    return {
        "answer": answer,
        "chunks": reranked_chunks
    }
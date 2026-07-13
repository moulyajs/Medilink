from .retriever import retrieve
from .reranker import rerank
from .context_builder import build_context
from .prompts import build_rag_prompt
from .llm import generate_answer

# ✅ ONLY this agent
# from chatbot.agents.prompt_guard_agent import PromptGuardAgent

from .query_analyzer import analyze_query

from .time_retriever import (
    get_latest_lab,
    get_lab_history,
    get_abnormal_labs
)

# 🔐 Initialize once
# guard = PromptGuardAgent()

"""
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
"""


def rewrite_query(query, chat_history):

    if not chat_history:
        return query

    history_text = " ".join(
        [m["content"] for m in chat_history[-4:]]
    )

    return f"{history_text} {query}"


def rag_pipeline(
    query: str,
    patient_id: str,
    chat_history: list
):

    # 🚧 ONLY Agent: Prompt Guard
    # if guard.detect(query):
    #     return {
    #         "answer": "⚠️ Security Alert: Query blocked due to potential prompt injection.",
    #         "chunks": []
    #     }

    # ----------------------------------
    # STEP 0 : QUERY REWRITE
    # ----------------------------------

    rewritten_query = rewrite_query(
        query,
        chat_history
    )

    # ----------------------------------
    # STEP 1 : QUERY ANALYSIS
    # ----------------------------------

    analysis = analyze_query(query)
    """
    print("\n" + "=" * 80)
    print("QUERY ANALYSIS")
    print("=" * 80)
    print(analysis)
    """
    intent = analysis.get(
        "intent",
        "GENERAL_RAG"
    )

    entity = analysis.get(
        "entity"
    )

    # ----------------------------------
    # LATEST VALUE
    # ----------------------------------

    if intent == "LATEST_VALUE" and entity:

        latest = get_latest_lab(
            patient_id,
            entity
        )

        if latest:

            return {
                "answer":
                    latest.payload["text"],
                "chunks": []
            }

    # ----------------------------------
    # TREND / HISTORY
    # ----------------------------------

    if intent == "TREND" and entity:

        history = get_lab_history(
            patient_id,
            entity
        )

        if history:

            return {
                "answer": str(history),
                "chunks": []
            }

    # ----------------------------------
    # ABNORMAL LABS
    # ----------------------------------

    if intent == "ABNORMAL_LABS":

        abnormal = get_abnormal_labs(
            patient_id
        )

        chunks = []

        for c in abnormal:

            chunks.append(
                {
                    "text":
                        c.payload.get(
                            "text"
                        ),

                    "report_date":
                        c.payload.get(
                            "report_date"
                        ),

                    "chunk_type":
                        c.payload.get(
                            "chunk_type"
                        ),

                    "report_type":
                        c.payload.get(
                            "report_type"
                        )
                }
            )

        context = build_context(
            chunks
        )

        prompt = build_rag_prompt(
            context,
            query,
            chat_history
        )

        answer = generate_answer(
            prompt
        )

        return {
            "answer": answer,
            "chunks": chunks
        }

    # ----------------------------------
    # GENERAL RAG
    # ----------------------------------

    chunks = retrieve(
        rewritten_query,
        patient_id,
        analysis
    )

    if not chunks:

        return {
            "answer":
                "No relevant medical data found.",
            "chunks": []
        }
    """
    print("\n" + "=" * 80)
    print("INPUT TO RERANKER")
    print("=" * 80)

    for i, chunk in enumerate(
        chunks[:20],
        start=1
    ):

        print(
            f"\n[{i}] "
            f"{chunk.get('report_date')}"
        )

        print(
            chunk.get(
                "chunk_type"
            )
        )

        print(
            chunk.get(
                "text",
                ""
            )[:200]
        )
        """

    # ----------------------------------
    # RERANK
    # ----------------------------------

    reranked_chunks = rerank(
        query,
        chunks,
        top_k=5
    )

    # ----------------------------------
    # CONTEXT
    # ----------------------------------

    context = build_context(
        reranked_chunks
    )

    # ----------------------------------
    # PROMPT
    # ----------------------------------

    prompt = build_rag_prompt(
        context,
        query,
        chat_history
    )

    # ----------------------------------
    # GENERATE
    # ----------------------------------

    answer = generate_answer(
        prompt
    )

    # 🚨 Output Guard (KEEP THIS — important even with one agent)
    # if is_sensitive_output(answer):
    #     return {
    #         "answer": "⚠️ Security Alert: Response blocked due to sensitive information leakage.",
    #         "chunks": []
    #     }

    return {
        "answer": answer,
        "chunks": reranked_chunks
    }
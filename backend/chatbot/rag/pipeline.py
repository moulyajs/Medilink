from .retriever import retrieve
from .reranker import rerank
from .context_builder import build_context
from .prompts import build_rag_prompt
from .llm import generate_answer
from .query_rewriter import rewrite_query
# ✅ ONLY this agent
# from chatbot.agents.prompt_guard_agent import PromptGuardAgent

from .query_analyzer import analyze_query

from .time_retriever import (
    get_latest_lab,
    get_lab_history,
    get_abnormal_labs,
    get_lab_trend,
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
    GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
}

    THANKS = {
    "thanks",
    "thank you",
    "thx"
}

    BYE = {
    "bye",
    "goodbye",
    "see you"
}
    query_lower = query.strip().lower()

    if query_lower in GREETINGS:
        return {
            "answer": (
                "Hello! 👋 I'm Medilink AI. "
                "How can I help you with your medical records today?"
            ),
            "chunks": []
        }

    if query_lower in THANKS:
        return {
            "answer": "You're welcome! Feel free to ask about your reports, lab results, or medical history.",
            "chunks": []
        }

    if query_lower in BYE:
        return {
            "answer": "Take care! I'm here whenever you need help with your health records.",
            "chunks": []
        }

    # Only now invoke the LLM
    
    rewritten_query = rewrite_query(
        query,
        chat_history
    )
    print("\n" + "=" * 80)
    print("QUERY REWRITER")
    print("=" * 80)
    print("Original Query:")
    print(query)

    print("\nRewritten Query:")
    print(rewritten_query)


    # ----------------------------------
    # STEP 1 : QUERY ANALYSIS
    # ----------------------------------

    analysis = analyze_query(rewritten_query)
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
    # TREND 
    # ----------------------------------

    if intent == "TREND" and entity:
        print("\n" + "=" * 60)
        print("TREND INTENT DETECTED")
        print("Entity:", entity)
        print("=" * 60)
        trend = get_lab_trend(
        patient_id,
        entity
    )

        history = get_lab_history(
        patient_id,
        entity
    )

        if trend:

            context = f"""
Lab Test: {entity}

Trend: {trend['trend']}
Latest Value: {trend['latest_value']}
Status: {trend['status']}
Delta: {trend['delta']}
Slope: {trend['slope']}
Data Points: {trend['data_points']}

History:
{history}
"""

            prompt = f"""
You are Medilink AI.

Explain the patient's lab trend in simple language.

Rules:
- Do NOT diagnose diseases.
- Do NOT prescribe treatment.
- Mention whether the trend is increasing, decreasing, or stable.
- Mention whether the latest value is normal or abnormal.
- Do NOT advise consulting a doctor unless the latest value is abnormal or the trend is clinically concerning.
- Use the history only to support your explanation.
- Keep the answer concise.

Trend Information:

{context}

Answer:
"""

        answer = generate_answer(prompt)

        return {
            "answer": answer,
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
            rewritten_query
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
    print("\nUsing Retrieval Query:")
    print(rewritten_query)
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
    print("\nCrossEncoder Query:")
    print(rewritten_query)
    reranked_chunks = rerank(
        rewritten_query,
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
    rewritten_query
)

    # ----------------------------------
    # GENERATE
    # ----------------------------------
    print("\n" + "=" * 80)
    print("FINAL PROMPT")
    print("=" * 80)
    print(prompt)
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
from .rag import handle_rag
from ..time_retriever import (
    get_lab_trend,
    get_lab_history,
)
from ..llm import generate_answer


def handle_trend(task, patient_id, query):

    entity = task.get("entity")

    trend = get_lab_trend(
        patient_id,
        entity,
    )

    # If exact lookup fails, use RAG
    if not trend:

        rag_response = handle_rag(
            task,
            patient_id,
            query,
        )

        if rag_response.get("chunks"):
            return {
                "type": "trend",
                "content": rag_response["content"],
                "chunks": rag_response["chunks"],
            }

        return {
            "type": "trend",
            "content": f"I couldn't find any {entity} results in your records."
        }

    history = get_lab_history(
        patient_id,
        entity,
    )

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
        "type": "trend",
        "content": answer,
    }
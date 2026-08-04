from ..time_retriever import get_abnormal_labs
from ..context_builder import build_context
from ..prompts import build_rag_prompt
from ..llm import generate_answer


def handle_abnormal(task, patient_id, query):
    

    abnormal = get_abnormal_labs(patient_id)
    if not abnormal:
        return {
        "type": "abnormal",
        "content": "I couldn't find any abnormal lab results.",
        "chunks": []
    }
    chunks = []

    for c in abnormal:
        chunks.append({
            "text": c.payload.get("text"),
            "report_date": c.payload.get("report_date"),
            "chunk_type": c.payload.get("chunk_type"),
            "report_type": c.payload.get("report_type"),
        })

    context = build_context(chunks)

    prompt = build_rag_prompt(
        context,
        query,
    )

    answer = generate_answer(prompt)

    return {
        "type": "abnormal",
        "content": answer,
        "chunks": chunks,
    }
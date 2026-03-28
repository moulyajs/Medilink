def build_rag_prompt(context: str, query: str, chat_history: list):

    history_text = "\n".join([
        f"{m['role'].upper()}: {m['content']}"
        for m in chat_history
    ])

    return f"""
You are a medical assistant.

RULES:
- Use ONLY the provided context
- Do NOT diagnose
- Highlight abnormal values if present
- If unsure, say you don't have enough information
- Keep answers clear and concise
- Do not prescribe medicines

Conversation History:
{history_text}

Context:
{context}

User Question:
{query}

Answer:
"""
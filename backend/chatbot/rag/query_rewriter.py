import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"


def rewrite_query(query: str, chat_history: list):

    if not chat_history:
        return query

    history = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in chat_history[-6:]
    )

    prompt = f"""
You are a query rewriting assistant.

Your ONLY job is to rewrite the user's latest message into a standalone question.

Rules:

- Do NOT answer the question.
- Do NOT explain anything.
- Preserve the user's intent.
- Resolve references like:
  - it
  - this
  - that
  - previous
  - latest
  - those
-Do NOT include laboratory values.
- Do NOT include dates.
- Do NOT copy previous assistant responses.
- If the query is already complete, return it unchanged.
- Return ONLY the rewritten question.

Conversation:

{history}

Latest User Question:
{query}

Standalone Question:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    rewritten = response.json()["response"].strip()

    print("\nStandalone Query:")
    print(rewritten)

    return rewritten
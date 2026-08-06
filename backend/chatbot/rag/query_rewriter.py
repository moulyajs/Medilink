import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

# -----------------------------------------
# Messages that never need rewriting
# -----------------------------------------

SIMPLE_MESSAGES = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
    "bye",
    "goodbye",
    "see you",
}

# -----------------------------------------
# Words indicating a follow-up question
# -----------------------------------------

FOLLOW_UP_WORDS = {
    # Pronouns
    "it",
    "this",
    "that",
    "these",
    "those",
    "its",
    "their",
    "them",
    "they",

    # References
    "mine",
    "one",
    "ones",

    # Time references
    "previous",
    "earlier",
    "former",
    "latter",
    "last",
    "before",

    # Comparison
    "same",
    "another",
    "other",
    "else",
}

# -----------------------------------------
# Common follow-up phrases
# -----------------------------------------

FOLLOW_UP_PREFIXES = (
    "what about",
    "how about",
    "is it",
    "is that",
    "why is",
    "why was",
    "why does",
    "does it",
    "does that",
    "should i",
    "should that",
    "can you explain",
    "what does that",
    "what do you mean",
)


def rewrite_query(query: str, chat_history: list):

    query = query.strip()

    if not chat_history:
        return query

    query_lower = query.lower()

    # Greetings / thanks / bye
    if query_lower in SIMPLE_MESSAGES:
        return query

    words = set(
        query_lower.replace("?", "").split()
    )

    needs_rewrite = (
        any(word in FOLLOW_UP_WORDS for word in words)
        or any(
            query_lower.startswith(prefix)
            for prefix in FOLLOW_UP_PREFIXES
        )
    )

    # Already a complete question
    if not needs_rewrite:
        return query

    history = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in chat_history[-6:]
    )

    prompt = f"""
You are a query rewriting assistant.

Rewrite ONLY follow-up questions into standalone questions.

Rules:

- Never answer the question.
- Never change the user's intent.
- Never add medical knowledge.
- Never expand abbreviations.
- Never invent new information.
- Preserve the user's wording whenever possible.
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
            "stream": False,
        },
    )

    rewritten = response.json()["response"].strip()

    print("\nStandalone Query:")
    print(rewritten)

    return rewritten
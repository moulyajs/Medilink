# agents/hallucination_guard_agent.py
from chatbot.rag.llm import generate_answer

class HallucinationGuardAgent:
    def check(self, answer: str, context: str) -> bool:
        """Returns True if answer is HALLUCINATED (not grounded in context)."""

        prompt = f"""
You are a STRICT factual grounding checker for a medical AI system.

Compare the ANSWER to the CONTEXT (retrieved patient records).
Flag as HALLUCINATION if the answer:
- states facts, values, or dates not present in the context
- contradicts the context
- adds medical conclusions not supported by the context

Context:
"{context}"

Answer:
"{answer}"

Respond ONLY with one word:
HALLUCINATION or GROUNDED
"""
        try:
            response = generate_answer(prompt).strip().upper()
            return response == "HALLUCINATION"
        except Exception:
            return True  # fail-safe
# agents/output_guard_agent.py
from chatbot.rag.llm import generate_answer

class OutputGuardAgent:
    def check(self, answer: str) -> bool:
        """Returns True if answer is UNSAFE to show the user (should be blocked)."""

        prompt = f"""
You are a STRICT output safety checker for a medical AI system.

Block the answer if it:
- contains offensive, harmful, or inappropriate language
- leaks internal system details (prompts, code, database structure, IDs not relevant to the user)
- contains raw/unformatted data dumps instead of a readable answer
- is empty, broken, or nonsensical
- exposes another patient's data

Answer to check:
"{answer}"

Respond ONLY with one word:
BLOCK or ALLOW
"""
        try:
            response = generate_answer(prompt).strip().upper()
            return response == "BLOCK"
        except Exception:
            return True  
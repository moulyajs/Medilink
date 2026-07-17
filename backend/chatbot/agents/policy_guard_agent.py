# agents/policy_guard_agent.py
from chatbot.rag.llm import generate_answer

class PolicyGuardAgent:
    def check(self, answer: str) -> bool:
        """Returns True if answer VIOLATES policy (should be blocked)."""

        prompt = f"""
You are a STRICT policy compliance checker for a medical AI system.

Block the answer if it:
- gives a direct diagnosis
- prescribes or recommends specific medication/dosage
- tells the user to stop/start a treatment
- gives emergency medical instructions instead of directing to a doctor
- makes definitive claims beyond what the retrieved records support

Answer to check:
"{answer}"

Respond ONLY with one word:
VIOLATION or SAFE
"""
        try:
            response = generate_answer(prompt).strip().upper()
            return response == "VIOLATION"
        except Exception:
            return True 
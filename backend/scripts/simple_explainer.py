from llama_cpp import Llama
import os


# Load model only once (important for performance)
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "Phi-3-mini-4k-instruct-Q4_0.gguf"
)

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,     # adjust if needed
    n_gpu_layers=20  # Metal acceleration (M1)
)


def explain_simple(summary_text):
    """
    Convert medical summary to patient-friendly language
    """

    prompt = f"""
You are a helpful and responsible medical assistant.

Your task is to rewrite the following medical report in very simple,
easy-to-understand language for patients.

Guidelines:
1. Use common, everyday words.
2. Avoid complex medical terminology.
3. If a medical term appears, explain it in simple words.
4. Do NOT give any diagnosis or medical advice.
5. Do NOT suggest treatments.
6. Do NOT scare the patient.
7. If any result is abnormal:
   - Only explain what the medical term means.
   - Do NOT explain what it indicates or predicts.
8. Keep sentences short and clear.
9. Be polite, calm, and reassuring.

Medical Summary:
{summary_text}

Simple Explanation:
"""

    output = llm(
        prompt,
        max_tokens=300,
        temperature=0.4,
        stop=["Medical Summary:"]
    )

    return output["choices"][0]["text"].strip()

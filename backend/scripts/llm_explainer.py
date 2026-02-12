import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"

print("Loading Phi-3 model...")

# Detect best device
if torch.backends.mps.is_available():
    DEVICE = "mps"
    DTYPE = torch.float16   # Important for memory
    print("Using Apple GPU (MPS)")
else:
    DEVICE = "cpu"
    DTYPE = torch.float32
    print("Using CPU")


# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
)


# Load model (memory optimized)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=DTYPE,
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    use_cache=False
)

model.to(DEVICE)
model.eval()

print("Phi-3 loaded.")


# -----------------------------
# Generator
# -----------------------------

def generate_plain_explanation(summary_text: str) -> str:

    prompt = f"""
You are a medical assistant.

Explain this health report in simple language.

Rules:
- Use easy words
- No diagnosis
- No treatment advice
- Only use given info

Report:
{summary_text}

Simple explanation:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    # Move inputs to device
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}


    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            num_beams=2,
            use_cache=False,
            pad_token_id=tokenizer.eos_token_id
        )


    result = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return result.strip()

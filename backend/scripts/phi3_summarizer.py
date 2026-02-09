from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.float32,   # CPU safe
    device_map="cpu"             # FORCE CPU
)

def generate_phi3_summary(prompt, max_tokens=80):
    # 🔥 VERY IMPORTANT: limit input size
    prompt = prompt[:1500]

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)

import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"



def generate_answer(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()
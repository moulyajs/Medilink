import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

def generate_answer(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    print(response.status_code)
    print(response.text)

    return response.json()["response"].strip()
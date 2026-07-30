import json
import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"


def analyze_query(query):

    prompt = f"""
You are a medical query classifier.

Return ONLY JSON.

Possible intents:

LATEST_VALUE
TREND
ABNORMAL_LABS
MEDICAL_DEFINITION
GENERAL_RAG

Examples:

User: what is my latest haemoglobin
{{"intent":"LATEST_VALUE","entity":"HAEMOGLOBIN"}}

User: show haemoglobin trend
{{"intent":"TREND","entity":"HAEMOGLOBIN"}}

User: which labs are abnormal
{{"intent":"ABNORMAL_LABS"}}

User: what is HbA1c
{{"intent":"MEDICAL_DEFINITION","entity":"HBA1C"}}

User: why is creatinine test done
{{"intent":"MEDICAL_DEFINITION","entity":"CREATININE"}}

User: what does LDL measure
{{"intent":"MEDICAL_DEFINITION","entity":"LDL"}}

User: what medicines am i taking
{{"intent":"GENERAL_RAG"}}

User Query:
{query}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    text = response.json()["response"]

    try:
        return json.loads(text)
    except:
        return {
            "intent": "GENERAL_RAG"
        }
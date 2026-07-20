import json
import requests


OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

def extract_clinical_facts(text):

    prompt = f"""
You are a medical information extraction system.

Extract ONLY explicitly mentioned medical information.

Rules:

- Symptoms = patient complaints only.
- Diagnoses = diseases or conditions diagnosed by physician.
- Medications = prescribed drugs.
- Procedures = surgeries, scans, interventions.
- Findings = clinical findings, examination findings, imaging findings.

DO NOT extract:
- doctor names
- addresses
- appointment dates
- next visit instructions
- advice
- contact information

Return ONLY JSON.

Schema:

{{
  "symptoms": [],
  "diagnoses": [],
  "medications": [],
  "procedures": [],
  "findings": []
}}

Document:

{text[:6000]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    result = response.json()["response"]

    try:
        return json.loads(result)

    except Exception:

        return {
            "symptoms": [],
            "diagnoses": [],
            "medications": [],
            "procedures": [],
            "findings": []
        }
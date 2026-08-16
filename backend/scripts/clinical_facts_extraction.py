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

Return ONLY valid JSON.

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

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=120
        )

        print("OLLAMA STATUS:", response.status_code)
        print("OLLAMA RESPONSE:", response.text[:2000])

        response.raise_for_status()

        data = response.json()

        if "response" not in data:
            print("⚠️ Ollama response does not contain 'response'")

            return {
                "symptoms": [],
                "diagnoses": [],
                "medications": [],
                "procedures": [],
                "findings": []
            }

        result = data["response"]

        try:
            parsed = json.loads(result)

            return {
                "symptoms": parsed.get("symptoms", []),
                "diagnoses": parsed.get("diagnoses", []),
                "medications": parsed.get("medications", []),
                "procedures": parsed.get("procedures", []),
                "findings": parsed.get("findings", [])
            }

        except json.JSONDecodeError:
            print("⚠️ Ollama returned invalid JSON:")
            print(result)

            return {
                "symptoms": [],
                "diagnoses": [],
                "medications": [],
                "procedures": [],
                "findings": []
            }

    except requests.exceptions.RequestException as e:
        print("⚠️ Ollama connection error:", e)

        return {
            "symptoms": [],
            "diagnoses": [],
            "medications": [],
            "procedures": [],
            "findings": []
        }

    except Exception as e:
        print("⚠️ Clinical facts extraction error:", e)

        return {
            "symptoms": [],
            "diagnoses": [],
            "medications": [],
            "procedures": [],
            "findings": []
        }
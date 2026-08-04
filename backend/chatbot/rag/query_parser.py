import json
import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"


def parse_query(query: str):

    prompt = f"""
You are a medical query parser.

Your task is to identify ALL user requests.

Return ONLY valid JSON.

Output format:

{{
    "greeting": true,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "LATEST_VALUE",
            "entity": "..."
        }}
    ]
}}

Possible intents:

LATEST_VALUE
TREND
ABNORMAL_LABS
MEDICAL_DEFINITION
GENERAL_RAG

Rules:

- A user can ask multiple things.
- Extract every task.
- Greeting is NOT a task.
- Thanks is NOT a task.
- Bye is NOT a task.
- If no entity exists, omit it.
- If no medical task exists, return an empty task list.
- Return ONLY JSON.

Very Important:

If the user asks:

"What is haemoglobin?"
"What is creatinine?"
"What does platelet count mean?"
"What is meant by HbA1c?"

→ intent = MEDICAL_DEFINITION

Do NOT classify these as LATEST_VALUE.

-----------------------------------------

If the user asks:

"What is my haemoglobin?"
"What is my haemoglobin value?"
"What is my latest creatinine?"
"What is my platelet count?"

→ intent = LATEST_VALUE

LATEST_VALUE refers to retrieving the patient's own lab value.

Examples:

"What is my haemoglobin?"
"My haemoglobin level"
"What is my current haemoglobin?"
"What was my latest creatinine?"
"Show my platelet count."

These should NEVER be classified as MEDICAL_DEFINITION.

-----------------------------------------

When unsure between MEDICAL_DEFINITION and LATEST_VALUE:

Choose MEDICAL_DEFINITION unless the query clearly refers to the user's own medical records.

-----------------------------------------

The following phrases usually indicate MEDICAL_DEFINITION:

- what is
- what is meant by
- what does ... mean
- define
- explain
- tell me about

unless they clearly refer to the user's own medical records using words like:

my
latest
current
value
result
level

-----------------------------------------

Return the entity exactly as it appears in the user's query.

Do not convert British spelling to American spelling or vice versa.

Example:

User:
What is haemoglobin?

Entity:
HAEMOGLOBIN

User:
What is hemoglobin?

Entity:
HEMOGLOBIN

-----------------------------------------

Examples:

User:
Hi

Output:
{{
    "greeting": true,
    "thanks": false,
    "bye": false,
    "tasks": []
}}

User:
Hi, show my haemoglobin trend.

Output:
{{
    "greeting": true,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "TREND",
            "entity": "HAEMOGLOBIN"
        }}
    ]
}}

User:
What is HbA1c and show my HbA1c trend.

Output:
{{
    "greeting": false,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "MEDICAL_DEFINITION",
            "entity": "HBA1C"
        }},
        {{
            "intent": "TREND",
            "entity": "HBA1C"
        }}
    ]
}}

User:
What is haemoglobin?

Output:
{{
    "greeting": false,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "MEDICAL_DEFINITION",
            "entity": "HAEMOGLOBIN"
        }}
    ]
}}

User:
What is my haemoglobin?

Output:
{{
    "greeting": false,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "LATEST_VALUE",
            "entity": "HAEMOGLOBIN"
        }}
    ]
}}

User:
Hi, what is haemoglobin and what is my haemoglobin value?

Output:
{{
    "greeting": true,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "MEDICAL_DEFINITION",
            "entity": "HAEMOGLOBIN"
        }},
        {{
            "intent": "LATEST_VALUE",
            "entity": "HAEMOGLOBIN"
        }}
    ]
}}

User:
Which medicines am I taking?

Output:
{{
    "greeting": false,
    "thanks": false,
    "bye": false,
    "tasks": [
        {{
            "intent": "GENERAL_RAG"
        }}
    ]
}}

User Query:
{query}

JSON:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
        },
    )

    text = response.json()["response"]

    try:
        return json.loads(text)

    except Exception:
        return {
            "greeting": False,
            "thanks": False,
            "bye": False,
            "tasks": [
                {
                    "intent": "GENERAL_RAG"
                }
            ]
        }
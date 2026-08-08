from ..definition_prompt import build_definition_prompt
from ..llm import generate_answer


def handle_definition(task, patient_id, query):

    prompt = build_definition_prompt(query)

    answer = generate_answer(prompt)

    return {
        "type": "definition",
        "content": answer,
    }
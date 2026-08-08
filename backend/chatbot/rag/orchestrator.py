from .handlers.greeting import (
    handle_greeting,
    handle_thanks,
    handle_bye,
)

from .handlers.definition import handle_definition
from .handlers.latest import handle_latest
from .handlers.trend import handle_trend
from .handlers.abnormal import handle_abnormal
from .handlers.rag import handle_rag

from .response_builder import build_response


# ---------------------------------------------------
# Registry of all task handlers
# ---------------------------------------------------

TASK_HANDLERS = {
    "LATEST_VALUE": handle_latest,
    "TREND": handle_trend,
    "MEDICAL_DEFINITION": handle_definition,
    "ABNORMAL_LABS": handle_abnormal,
    "GENERAL_RAG": handle_rag,
}


def orchestrate(parsed, patient_id, query):

    responses = []

    # ---------------------------------------------------
    # Conversation
    # ---------------------------------------------------

    if parsed.get("greeting"):
        responses.append(handle_greeting())

    if parsed.get("thanks"):
        responses.append(handle_thanks())

    if parsed.get("bye"):
        responses.append(handle_bye())

    # ---------------------------------------------------
    # Medical Tasks
    # ---------------------------------------------------

    for task in parsed.get("tasks", []):

        intent = task.get("intent")

        handler = TASK_HANDLERS.get(intent)

        if handler:

            response = handler(
                task=task,
                patient_id=patient_id,
                query=query,
            )

            if response:
                responses.append(response)

    return build_response(responses)
# chatbot/chat_api.py

from fastapi import FastAPI
from pydantic import BaseModel

from chatbot.rag.pipeline import rag_pipeline
from chatbot.chat_service import get_session, update_session

app = FastAPI()


class ChatRequest(BaseModel):
    query: str
    patient_id: str
    session_id: str


@app.post("/chat")
def chat(req: ChatRequest):

    chat_history = get_session(req.session_id)

    response = rag_pipeline(
        query=req.query,
        patient_id=req.patient_id,
        chat_history=chat_history
    )

    update_session(
        req.session_id,
        req.query,
        response["answer"]
    )

    return response
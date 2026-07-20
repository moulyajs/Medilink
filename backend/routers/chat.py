from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db

from models.patient import Patient

from utils.dependencies import get_current_patient

from chatbot.rag.pipeline import rag_pipeline

from schemas.chat import (
    CreateSessionResponse,
    SendMessageRequest,
    SendMessageResponse,
    SessionSummary,
    SessionMessagesResponse,
    ChatMessageResponse,
)

from services.chat_service import (
    create_session,
    get_sessions,
    get_session,
    get_messages,
    save_message,
    update_title,
    touch_session,
    delete_session,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"],
)

@router.post(
    "/session",
    response_model=CreateSessionResponse,
)
def create_chat_session(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    session = create_session(
        current_patient.patient_id,
        db,
    )

    return CreateSessionResponse(
        session_id=session.session_id
    )
@router.get(
    "/sessions",
    response_model=list[SessionSummary],
)
def list_sessions(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return get_sessions(
        current_patient.patient_id,
        db,
    )

@router.get(
    "/session/{session_id}",
    response_model=SessionMessagesResponse,
)
def load_session(
    session_id: UUID,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    session = get_session(
        session_id,
        current_patient.patient_id,
        db,
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = get_messages(
        session.session_id,
        db,
    )

    return SessionMessagesResponse(
        session_id=session.session_id,
        title=session.title,
        messages=[
            ChatMessageResponse(
                role=m.role,
                content=m.content,
            )
            for m in messages
        ],
    )
@router.post(
    "/session/{session_id}/message",
    response_model=SendMessageResponse,
)

def send_message(
    session_id: UUID,
    request: SendMessageRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    session = get_session(
        session_id,
        current_patient.patient_id,
        db,
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    previous_messages = get_messages(
        session_id,
        db,
    )

    history = [
        {
            "role": m.role,
            "content": m.content,
        }
        for m in previous_messages
    ]

    save_message(
        session_id,
        "user",
        request.query,
        db,
    )

    result = rag_pipeline(
        query=request.query,
        patient_id=str(current_patient.patient_id),
        chat_history=history,
    )

    save_message(
        session_id,
        "assistant",
        result["answer"],
        db,
    )

    update_title(
        session,
        request.query,
        db,
    )

    touch_session(
        session,
        db,
    )

    return SendMessageResponse(
        answer=result["answer"]
    )
@router.delete("/session/{session_id}")
def remove_session(
    session_id: UUID,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    session = get_session(
        session_id,
        current_patient.patient_id,
        db,
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    delete_session(session, db)

    return {
        "message": "Conversation deleted successfully"
    }
from datetime import datetime

from sqlalchemy.orm import Session

from models.chat_session import ChatSession
from models.chat_message import ChatMessage

def create_session(
    patient_id,
    db: Session
):
    session = ChatSession(
        patient_id=patient_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session

def get_sessions(
    patient_id,
    db: Session
):
    return (
        db.query(ChatSession)
        .filter(
            ChatSession.patient_id == patient_id,
            ChatSession.is_deleted == False
        )
        .order_by(ChatSession.updated_at.desc())
        .all()
    )

def get_session(
    session_id,
    patient_id,
    db: Session
):
    return (
        db.query(ChatSession)
        .filter(
            ChatSession.session_id == session_id,
            ChatSession.patient_id == patient_id,
            ChatSession.is_deleted == False
        )
        .first()
    )
def get_messages(
    session_id,
    db: Session
):
    return (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

def save_message(
    session_id,
    role,
    content,
    db: Session
):
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message
MAX_TITLE_LENGTH = 40

def generate_title(query: str) -> str:
    query = " ".join(query.split())

    if len(query) <= MAX_TITLE_LENGTH:
        return query

    return query[:MAX_TITLE_LENGTH].rstrip() + "..."
def update_title(
    session,
    first_query,
    db: Session
):
    if session.title:
        return

    session.title = generate_title(first_query)

    db.commit()
def touch_session(
    session,
    db: Session
):
    session.updated_at = datetime.utcnow()

    db.commit()

def delete_session(
    session,
    db: Session
):
    db.delete(session)
    db.commit()
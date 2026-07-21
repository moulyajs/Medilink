from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


# ---------- Existing ----------

class ChatResponse(BaseModel):
    answer: str


# ---------- Create Session ----------

class CreateSessionResponse(BaseModel):
    session_id: UUID


# ---------- Send Message ----------

class SendMessageRequest(BaseModel):
    query: str


class SendMessageResponse(BaseModel):
    answer: str


# ---------- Conversation List ----------

class SessionSummary(BaseModel):
    session_id: UUID
    title: str | None
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------- Chat Messages ----------

class ChatMessageResponse(BaseModel):
    role: str
    content: str

    class Config:
        from_attributes = True


class SessionMessagesResponse(BaseModel):
    session_id: UUID
    title: str | None
    messages: List[ChatMessageResponse]
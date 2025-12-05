from typing import List
from uuid import UUID
from pydantic import BaseModel

from app.schemas.message_schemas import MessageOut

class ContextChunk(BaseModel):
    id: str
    source: str | None = None
    page: int | None = None
    score: float
    content: str

class ChatRequest(BaseModel):
    session_id: UUID
    question: str

class ChatResponse(BaseModel):
    answer: str
    contexts: List[ContextChunk]
    messages: List[MessageOut]

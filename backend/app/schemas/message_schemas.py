# backend/app/schemas/message_schemas.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageBase(BaseModel):
    session_id: UUID
    role: str
    content: str
    mode: str = "chat"


class MessageCreate(MessageBase):
    pass


class MessageOut(MessageBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

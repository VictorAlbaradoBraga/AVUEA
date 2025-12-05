# backend/app/schemas/session_schemas.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionBase(BaseModel):
    title: str | None = None


class SessionCreate(SessionBase):
    pass


class SessionOut(SessionBase):
    id: UUID
    created_at: datetime

    class Config:
        # Pydantic v2: usar from_attributes em vez de orm_mode
        from_attributes = True

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)

    role = Column(String, nullable=False)      # "user" ou "assistant"
    content = Column(String, nullable=False)
    mode = Column(String, nullable=False, default="chat")

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", backref="messages")

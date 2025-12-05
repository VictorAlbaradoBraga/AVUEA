from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services import message_service

router = APIRouter(prefix="/chat", tags=["chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
):
    return message_service.handle_chat(db, body)

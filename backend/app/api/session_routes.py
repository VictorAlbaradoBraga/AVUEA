from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.session_schemas import SessionCreate, SessionOut
from app.services import session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SessionOut)
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db),
):
    return session_service.create_session(db, data)

@router.get("/", response_model=list[SessionOut])
def list_sessions(
    db: Session = Depends(get_db),
):
    return session_service.list_sessions(db)

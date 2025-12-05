from sqlalchemy.orm import Session

from app.models.session import Session as SessionModel
from app.schemas.session_schemas import SessionCreate, SessionOut

def create_session(db: Session, data: SessionCreate) -> SessionOut:
    db_session = SessionModel(title=data.title)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return SessionOut.from_orm(db_session)

def list_sessions(db: Session) -> list[SessionOut]:
    sessions = db.query(SessionModel).order_by(SessionModel.created_at.desc()).all()
    return [SessionOut.from_orm(s) for s in sessions]

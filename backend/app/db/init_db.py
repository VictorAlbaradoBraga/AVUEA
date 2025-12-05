# backend/app/db/init_db.py
from app.db.base import Base
from app.db.session import engine

# importe os models aqui, pra que o Base conheça todas as tabelas
from app.models import session as session_model  # noqa
from app.models import message as message_model  # noqa


def init_db():
    Base.metadata.create_all(bind=engine)

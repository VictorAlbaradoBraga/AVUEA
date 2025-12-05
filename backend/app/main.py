from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.init_db import init_db
from app.api import session_routes, chat_routes

app = FastAPI(title="RAG Chat API")

# CORS basico para o front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cria tabelas no banco
init_db()

# inclui rotas
app.include_router(session_routes.router)
app.include_router(chat_routes.router)

@app.get("/health")
def health():
    return {"status": "ok"}

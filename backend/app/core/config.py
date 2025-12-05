import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "RAG Chat"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/rag_chat",
    )

    # diretorios de dados
    PDF_DIR: str = os.getenv("PDF_DIR", "data/pdfs")
    VECTORSTORE_DIR: str = os.getenv("VECTORSTORE_DIR", "data/vectorstore")

settings = Settings()

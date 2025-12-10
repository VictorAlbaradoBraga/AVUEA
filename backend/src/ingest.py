# src/ingest.py
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

PDF_DIR = Path("data/pdfs")
VECTOR_DIR = Path("data/vectorstore")

# modelo de embedding local (leve, ótimo para CPU)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# depois, se quiser testar Qwen3-Embedding-0.6B:
# EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

def run_ingest():
    if VECTOR_DIR.exists() and any(VECTOR_DIR.iterdir()):
        print(f"Vectorstore já existe em {VECTOR_DIR}, pulando ingestão.")
        return
    docs = []
    for pdf_path in PDF_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()
        for d in pdf_docs:
            d.metadata["source"] = pdf_path.name
        docs.extend(pdf_docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DIR),
    )

    print(f"Ingestao concluida. {len(chunks)} chunks armazenados.")

if __name__ == "__main__":
    run_ingest()

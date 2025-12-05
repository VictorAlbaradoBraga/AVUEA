# src/rag.py
from pathlib import Path
from typing import List, Optional

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

VECTOR_DIR = Path("data/vectorstore")

# -----------------------------
# Embeddings (transformers via sentence-transformers)
# -----------------------------
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# Se quiser testar depois (mais pesado):
# EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

_embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME
)

_vectorstore = Chroma(
    embedding_function=_embeddings,
    persist_directory=str(VECTOR_DIR),
)

# -----------------------------
# LLM LOCAL com transformers
# -----------------------------
# Modelo leve para CPU:
GEN_MODEL_NAME = "google/flan-t5-small"
# Depois você pode testar:
#  - "google/flan-t5-base" (mais pesado, melhor qualidade)
#  - ou algum modelo instruído em ptBR (ex: ptt5) se quiser foco em português.

_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_NAME)
_model = AutoModelForSeq2SeqLM.from_pretrained(
    GEN_MODEL_NAME,
    # Aqui daria para brincar com dtype (meia precisão) para economizar memória:
    # torch_dtype=torch.float16,  # se sua CPU/GPU suportar
)

_generation_pipeline = pipeline(
    "text2text-generation",
    model=_model,
    tokenizer=_tokenizer,
    device=-1,  # -1 = CPU
)


def answer_question(question: str, history: Optional[list[str]] = None):
    """
    Faz RAG:
    - Recupera documentos relevantes no Chroma
    - Monta um prompt com o contexto
    - Gera resposta com modelo local via transformers
    - Retorna resposta + chunks para o front
    """
    retriever = _vectorstore.as_retriever(search_kwargs={"k": 4})
    # LangChain 0.2+: retriever é um Runnable, usa .invoke()
    docs: List[Document] = retriever.invoke(question)

    # monta contexto
    context_text = "\n\n".join([d.page_content for d in docs])

    history_text = ""
    if history:
        history_text = "\n\nHistorico:\n" + "\n".join(history)

    prompt = f"""
Você é um assistente que responde com base EXCLUSIVAMENTE no contexto abaixo.

Contexto:
{context_text}

{history_text}

Pergunta:
{question}

Responda de forma objetiva, mas completa.
"""

    result = _generation_pipeline(
        prompt,
        max_new_tokens=256,
        do_sample=False,
    )

    answer = result[0]["generated_text"]

    # monta lista de chunks para o front
    contexts = []
    for i, d in enumerate(docs):
        # Chroma nem sempre traz "score" no metadata; deixamos 0.0 por padrão
        raw_score = d.metadata.get("score", 0.0)
        score = float(raw_score) if isinstance(raw_score, (int, float)) else 0.0

        contexts.append(
            {
                "id": f"chunk-{i}",
                "source": d.metadata.get("source"),
                "page": d.metadata.get("page"),
                "score": score,
                "content": d.page_content,
            }
        )

    return {
        "answer": answer,
        "contexts": contexts,
    }

from pathlib import Path
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import re

# Configurações
VECTOR_DIR = Path("data/vectorstore")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL_NAME = "google/flan-t5-large"  # FLAN-T5-large

# Inicializa os componentes do Chroma (embeddings e vectorstore)
_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
_vectorstore = Chroma(
    embedding_function=_embeddings,
    persist_directory=str(VECTOR_DIR),
)

# Inicializa o modelo de geração de texto (FLAN-T5)
print(f"Carregando modelo {GEN_MODEL_NAME}...")
_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_NAME)
_model = AutoModelForSeq2SeqLM.from_pretrained(
    GEN_MODEL_NAME, 
    torch_dtype=torch.float32,
)

_generation_pipeline = pipeline(
    "text2text-generation",
    model=_model,
    tokenizer=_tokenizer,
    device=-1,  # CPU
)

# Função de sumarização do contexto
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_chunks(docs: List[Document], max_summary_length: int = 150) -> str:
    """
    Resume os chunks para criar um contexto mais conciso e objetivo.
    """
    summarized_chunks = []
    
    for doc in docs:
        # Gerar um resumo para o conteúdo de cada chunk
        summary = summarizer(doc.page_content, max_length=max_summary_length, min_length=50, do_sample=False)
        summarized_chunks.append(summary[0]['summary_text'])
    
    return "\n\n".join(summarized_chunks)

# Função para limpar a resposta final
def clean_answer(text: str) -> str:
    """Limpa a resposta final"""
    text = re.sub(r'\s+', ' ', text)  # Remove múltiplos espaços
    return text.strip()

# Função principal do RAG para gerar a resposta
def answer_question(question: str):
    """
    Pipeline de RAG otimizado:
    1. Recupera chunks relevantes
    2. Resume e constrói contexto com as informações relevantes
    3. Gera uma resposta coesa com base no contexto otimizado
    """
    
    # 1. RECUPERAÇÃO: Obtém chunks relevantes
    retriever = _vectorstore.as_retriever(search_kwargs={"k": 4})
    try:
        docs = retriever.invoke(question)
    except Exception as e:
        print(f"Erro na recuperação: {e}")
        return {
            "answer": "Erro ao recuperar documentos.",
            "contexts": []
        }
    
    if not docs:
        return {
            "answer": "Não encontrei documentos relevantes.",
            "contexts": []
        }
    
    # 2. Sumarização dos chunks recuperados
    summarized_context = summarize_chunks(docs)
    
    # 3. Criar prompt otimizado com contexto resumido
    prompt = f"""
Responda à pergunta abaixo utilizando as informações fornecidas, de forma clara e objetiva, sem repetir o texto do contexto.

Contexto:
{summarized_context}

Pergunta:
{question}

Resposta (em tópicos se aplicável):
"""
    
    # 4. Geração da resposta
    try:
        result = _generation_pipeline(
            prompt,
            max_length=350,
            min_length=100,
            num_beams=4,
            repetition_penalty=1.2,
            length_penalty=1.0,
            early_stopping=True,
            no_repeat_ngram_size=3,
            do_sample=False,
        )
        
        raw_answer = result[0]["generated_text"]
        answer = clean_answer(raw_answer)
        
    except Exception as e:
        print(f"Erro na geração: {e}")
        answer = "Erro ao gerar resposta."

    # Prepara os chunks para retorno
    contexts = []
    for i, doc in enumerate(docs):
        contexts.append({
            "id": f"chunk-{i}",
            "source": doc.metadata.get("source", "Desconhecido"),
            "page": doc.metadata.get("page", 0),
            "score": float(doc.metadata.get("score", 0.0)) if isinstance(doc.metadata.get("score", 0.0), (int, float)) else 0.0,
            "content": doc.page_content,
        })
    
    return {
        "answer": answer,
        "contexts": contexts,
    }

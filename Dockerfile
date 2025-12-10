FROM python:3.11-slim

# 1. Diretório de trabalho
WORKDIR /app

# 2. Dependências de sistema (psycopg2 etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 3. Copiar requirements do backend
COPY backend/requirements.txt ./requirements.txt

# 4. Instalar dependências a partir do PyPI
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar código da aplicação
COPY backend/app /app/app
COPY backend/src /app/src
COPY backend/data /app/data

# 6. Variáveis de ambiente
ENV PYTHONPATH=/app

# 7. Expor porta
EXPOSE 8000

# 8. Comando:
#    - roda a ingestão (cria/atualiza o Chroma em /app/data/vectorstore)
#    - depois sobe a API FastAPI com Uvicorn
CMD ["bash", "-c", "python src/ingest.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

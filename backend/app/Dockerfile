FROM python:3.11-slim

# 1. Criar diretório de trabalho
WORKDIR /app

# 2. Copiar requirements e instalar dependências
COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar código da API e do RAG
COPY . /app/app
COPY ../src /app/src
COPY ../data /app/data

# 4. Variáveis de ambiente
ENV PYTHONPATH=/app

# 5. Expor porta
EXPOSE 8000

# 6. Comando para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

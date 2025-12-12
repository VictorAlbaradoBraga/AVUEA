# AVUEA - Sistema de Perguntas e Respostas com Backend em FastAPI e LLM

Este é um sistema de perguntas e respostas baseado em um modelo de linguagem (LLM) para consultar regras, artigos e informações extraídas de documentos, como PDFs. O backend foi desenvolvido com **FastAPI** e utiliza modelos de linguagem da **Hugging Face** para gerar as respostas. O foco principal deste repositório é avaliar o desempenho do backend com o modelo de LLM.

## Como Rodar o Backend

### Requisitos
- **Docker** e **Docker Compose** instalados.

### Rodando o Backend

1. **Na raiz do projeto, execute o comando abaixo para iniciar o backend via Docker**:

    ```bash
    docker compose up --build
    ```

    Esse comando irá:
    - Construir o ambiente Docker.
    - Instalar todas as dependências necessárias.
    - Baixar o modelo de linguagem.
    - Configurar o banco de dados PostgreSQL.
    
    **Observação**: Esse processo pode demorar, pois o modelo de linguagem e o banco de dados precisam ser configurados pela primeira vez.

2. **Após a instalação, o backend estará acessível na porta `8000`** (FastAPI) e pronto para receber requisições.

### Testar a API

Após rodar o backend, você pode acessar as rotas via **FastAPI**:
- **GET `/sessions/`**: Lista as sessões existentes.
- **POST `/sessions/`**: Cria uma nova sessão.
- **POST `/chat/`**: Envia uma pergunta e recebe a resposta gerada pelo modelo de LLM, junto com o contexto relevante (chunks de texto recuperados de documentos).

## Como Rodar o Frontend

### Requisitos
- **Python 3.11** (ou superior) instalado.

### Rodando o Frontend

1. **Acesse a pasta do frontend**:

    ```bash
    cd frontend
    ```

2. **Instale as dependências do frontend**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Execute o frontend com Streamlit**:

    ```bash
    streamlit run app.py
    ```

4. **Após isso, o frontend estará acessível no endereço**:

    ```
    http://192.168.1.8:8501
    ```

### Funcionalidades Implementadas

1. **Criação e Listagem de Sessões**:
   O backend permite a criação de sessões e a listagem de sessões previamente criadas. Cada sessão mantém um histórico de perguntas e respostas.

2. **Envio de Perguntas**:
   O sistema permite ao usuário enviar perguntas, e o backend gera uma resposta utilizando o modelo de linguagem `google/flan-t5-large`. A resposta é baseada em documentos previamente carregados no sistema.

3. **Consulta aos Chunks**:
   Cada resposta gerada pode ser acompanhada dos chunks de onde as informações foram extraídas. Esses chunks são partes do documento processado, que podem ser visualizados via frontend.

4. **Modelo Utilizado**:
   - **Modelo de Linguagem**: `google/flan-t5-large` (Hugging Face).
   - **Banco de Dados**: PostgreSQL para armazenar sessões e mensagens.
   - **Contêiner Docker**: Para facilitar a configuração e o uso do projeto.

## Limitações

- **Modelo em CPU**: O modelo de linguagem `google/flan-t5-large` está sendo executado em **CPU**, o que pode impactar na velocidade de resposta e na precisão das respostas. Para um desempenho ideal, seria necessário rodar o modelo em **GPU**.
  
- **Erros Gramaticais e Limitações do Modelo**: Devido ao modelo ser executado em CPU e à natureza do próprio modelo de linguagem, pode haver erros gramaticais ou imprecisões nas respostas geradas.

## O que Gostaríamos que Fosse Avaliado

- **Desempenho do Modelo**: O foco principal deste projeto é avaliar o desempenho do backend utilizando o modelo `google/flan-t5-large`. Gostaríamos de saber se o modelo é capaz de gerar respostas coerentes e úteis a partir do conteúdo extraído de documentos.
- **Arquitetura do Sistema**: Gostaríamos que analisassem a estrutura do backend, com seus módulos organizados e funcionais, garantindo uma comunicação eficiente entre as partes. A arquitetura foi pensada para suportar grandes volumes de documentos e permitir a recuperação e processamento de informações de forma escalável.
- **Criatividade e Contornar os Problemas no Backend**: Gostaríamos que avaliassem a criatividade em contornar o problema de rodar o modelo de linguagem em **CPU** e como o sistema lida com a recuperação de contexto relevante. 

## Tecnologias Utilizadas

- **Backend**: FastAPI, Docker, PostgreSQL.
- **Modelo de Linguagem**: `google/flan-t5-large` da Hugging Face.
- **API**: FastAPI para a comunicação entre o frontend e o backend.
  
## Como Contribuir

1. Faça um fork deste repositório.
2. Crie uma nova branch para suas alterações.
3. Submeta um Pull Request com uma descrição clara das suas mudanças.

Agradecemos seu feedback e contribuições!

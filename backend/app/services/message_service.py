from sqlalchemy.orm import Session
from app.models.message import Message as MessageModel
from app.schemas.message_schemas import MessageOut
from app.schemas.chat_schemas import ChatRequest, ChatResponse, ContextChunk
from src.rag import answer_question  # Função que agora cuida de tudo internamente

def get_messages_by_session(db: Session, session_id) -> list[MessageOut]:
    msgs = (
        db.query(MessageModel)
        .filter(MessageModel.session_id == session_id)
        .order_by(MessageModel.created_at.asc())
        .all()
    )
    return [MessageOut.from_orm(m) for m in msgs]

def handle_chat(db: Session, chat_request: ChatRequest) -> ChatResponse:
    # 1) Salvar mensagem do usuário
    user_msg = MessageModel(
        session_id=chat_request.session_id,
        role="user",
        content=chat_request.question,
        mode="chat",
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 2) Chamar RAG com a pergunta, sem a necessidade de buscar os chunks manualmente
    rag_result = answer_question(chat_request.question)  # O RAG agora cuida de tudo internamente
    answer_text = rag_result["answer"]
    contexts_dicts = rag_result["contexts"]

    # 3) Converte dicionários para ContextChunk (schema Pydantic)
    contexts = [ContextChunk(**c) for c in contexts_dicts]

    # 4) Salvar mensagem da assistente no banco de dados
    assistant_msg = MessageModel(
        session_id=chat_request.session_id,
        role="assistant",
        content=answer_text,
        mode="chat",
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    # 5) Recarregar o histórico completo atualizado
    messages = get_messages_by_session(db, chat_request.session_id)

    return ChatResponse(
        answer=answer_text,
        contexts=contexts,  # Contextos agora incluem os chunks utilizados
        messages=messages,
    )

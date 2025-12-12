import streamlit as st
import requests

# URL da API FastAPI
API_URL = "http://127.0.0.1:8000"  # Ajuste conforme necessário

# Função para listar as sessões
def list_sessions():
    response = requests.get(f"{API_URL}/sessions/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao listar sessões!")
        return []

# Função para criar uma nova sessão
def create_session(title: str):
    response = requests.post(f"{API_URL}/sessions/", json={"title": title})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao criar sessão!")
        return None

# Função para enviar uma pergunta e receber uma resposta
def send_question(session_id: str, question: str):
    payload = {
        "session_id": session_id,
        "question": question
    }
    response = requests.post(f"{API_URL}/chat/", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao enviar pergunta!")
        return None

# Função principal para a interface do Streamlit
def main():
    st.set_page_config(page_title="Sistema de Perguntas e Respostas", page_icon=":robot_face:")

    # Session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Carregar sessões e interações
    st.title("Sistema de Perguntas e Respostas sobre as Regras da UEA")
    
    # Menu de navegação
    menu = ["Home", "Criar Sessão", "Chat"]
    choice = st.sidebar.selectbox("Escolha uma opção", menu)

    # Criar Sessão
    if choice == "Criar Sessão":
        st.subheader("Criar uma nova sessão")
        session_title = st.text_input("Título da sessão")
        if st.button("Criar Sessão"):
            if session_title:
                session = create_session(session_title)
                if session:
                    st.success(f"Sessão criada com sucesso: {session['title']}")
            else:
                st.warning("Por favor, insira um título para a sessão.")

    # Chat (Perguntar e Obter Resposta)
    elif choice == "Chat":
        st.subheader("Enviar Pergunta")
        
        # Escolher uma sessão
        sessions = list_sessions()
        session_titles = [session['title'] for session in sessions]
        selected_session_title = st.selectbox("Escolha a sessão", session_titles)
        
        if selected_session_title:
            selected_session_id = next(session['id'] for session in sessions if session['title'] == selected_session_title)
            question = st.text_input("Digite sua pergunta")
            if st.button("Enviar Pergunta"):
                if question:
                    response = send_question(selected_session_id, question)
                    if response:
                        # Adicionar a pergunta do usuário e resposta do assistente ao histórico
                        st.session_state.chat_history.append({"role": "user", "content": question})
                        st.session_state.chat_history.append({"role": "assistant", "content": response['answer']})
                        
                        # Exibe as mensagens do chat
                        for message in st.session_state.chat_history:
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])
                        
                        # Mostrar os contextos (chunks) com a opção de expandir
                        if response.get("contexts"):
                            with st.expander("Mostrar Contextos"):
                                for context in response["contexts"]:
                                    st.markdown(f"**ID:** {context['id']}")
                                    st.markdown(f"**Fonte:** {context['source']}")
                                    st.markdown(f"**Página:** {context['page']}")
                                    st.markdown(f"**Conteúdo:** {context['content']}")
                                    st.markdown("---")
                else:
                    st.warning("Por favor, insira uma pergunta.")
                
if __name__ == "__main__":
    main()

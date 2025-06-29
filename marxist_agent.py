import streamlit as st
import os
import google.generativeai as genai
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory

# --- CONFIGURAÇÃO DA PÁGINA E TÍTULO ---
st.set_page_config(page_title="Agente de IA Marxista", page_icon="☭", layout="wide")
st.title("☭ Agente de IA Marxista")
st.caption("Um agente para analisar o mundo sob a ótica do materialismo histórico-dialético.")

# --- CONFIGURAÇÃO DA API KEY ---
with st.sidebar:
    st.header("Configuração")
    st.markdown("Para o agente funcionar, insira sua chave da API do [Google AI Studio](https://aistudio.google.com/app/apikey).")
    google_api_key = st.text_input("Google API Key", key="google_api_key", type="password")

    if google_api_key:
        os.environ['GOOGLE_API_KEY'] = google_api_key
        try:
            genai.configure(api_key=google_api_key)
            st.success("API Key configurada!")
        except Exception as e:
            st.error(f"Erro na API Key: {e}")
            google_api_key = None
    else:
        st.warning("Por favor, insira sua Google API Key.")

# --- FUNÇÕES COM CACHE PARA OTIMIZAÇÃO ---
@st.cache_resource
def carregar_retriever():
    """Cria e retorna o retriever da base de conhecimento marxista."""
    with st.spinner("Carregando base de conhecimento (textos de Marx e Engels)..."):
        docs = [
            """Do Manifesto Comunista (Marx e Engels, 1848): A história de todas as sociedades até hoje existentes é a história das lutas de classes. Homem livre e escravo, patrício e plebeu, barão e servo, mestre de corporação e companheiro, numa palavra, opressores e oprimidos, em constante oposição, têm vivido numa guerra ininterrupta, ora franca, ora disfarçada; uma guerra que terminou sempre, ou por uma transformação revolucionária da sociedade inteira, ou pela destruição das duas classes em luta.""",
            """Sobre o Materialismo Histórico (Prefácio de 'Para a Crítica da Economia Política', Marx, 1859): Na produção social da sua vida, os homens entram em determinadas relações, necessárias, independentes da sua vontade, relações de produção que correspondem a uma determinada fase de desenvolvimento das suas forças produtivas materiais. O conjunto destas relações de produção forma a estrutura económica da sociedade, a base real sobre a qual se ergue uma superestrutura jurídica e política e à qual correspondem determinadas formas de consciência social.""",
            """Sobre a Mais-Valia (O Capital, Volume I, Marx, 1867): O capitalista compra a força de trabalho por seu valor, determinado pelo tempo de trabalho necessário para sua produção. A diferença, esse trabalho não pago, é a mais-valia. Essa mais-valia é a fonte do lucro e da acumulação de capital.""",
            """Sobre a Alienação (Manuscritos Econômico-Filosóficos, Marx, 1844): A alienação do trabalhador em seu produto significa não apenas que seu trabalho se torna um objeto, uma existência externa, mas que ele existe fora dele, independente, como algo estranho a ele, e que se torna um poder próprio, confrontando-o."""
        ]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        textos_divididos = text_splitter.create_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(textos_divididos, embeddings)
        st.success("Base de conhecimento carregada!")
        return vectorstore.as_retriever(search_kwargs={"k": 3})

def inicializar_agente():
    """
    Inicializa e retorna o Agente Executor com sua própria memória.
    """
    retriever = carregar_retriever()
    tools = [create_retriever_tool(retriever, "busca_textos_marxistas", "Busca e retorna trechos das obras de Marx e Engels para embasar a análise.")]
    
    prompt = hub.pull("hwchase17/react-chat")
    
    prompt.template = """Você é um Agente de IA Marxista, um intelectual dedicado. Sua missão é analisar o mundo através das lentes do materialismo histórico e dialético. Baseie suas análises em conceitos como luta de classes, mais-valia e alienação. Rebuta argumentos contrários (liberais, etc.) com a lógica marxista. Use a ferramenta `busca_textos_marxistas` para embasar suas respostas. Responda sempre em português do Brasil.""" + prompt.template
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.6)
    
    # A memória é criada aqui e viverá junto com o agente executor
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=5,
        return_messages=True
    )
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    return agent_executor

# --- INTERFACE DE CHAT DO STREAMLIT ---
if google_api_key:
    # Inicializa o agente e o armazena no estado da sessão para que persista
    if "agent_executor" not in st.session_state:
        st.session_state.agent_executor = inicializar_agente()
    
    # Inicializa o histórico de mensagens para a UI
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Olá, camarada! Apresente um tema para nossa análise dialética."}]
    
    # Exibe as mensagens do histórico da UI
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Captura a nova entrada do usuário
    if prompt_usuario := st.chat_input("Faça sua pergunta..."):
        # Adiciona a mensagem do usuário à UI
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.markdown(prompt_usuario)

        # Gera e exibe a resposta do agente
        with st.chat_message("assistant"):
            with st.spinner("Analisando as contradições..."):
                # Invoca o agente. Ele usará sua memória interna, que foi criada uma vez por sessão.
                # A chave "chat_history" é passada implicitamente pela memória do agente.
                response = st.session_state.agent_executor.invoke({
                    "input": prompt_usuario
                })
                
                resposta_agente = response['output']
                st.markdown(resposta_agente)
                # Adiciona a resposta do agente à UI
                st.session_state.messages.append({"role": "assistant", "content": resposta_agente})
else:
    st.info("Aguardando configuração da chave de API na barra lateral.")

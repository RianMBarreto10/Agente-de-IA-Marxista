# ☭ Agente de IA Marxista ☭

Um agente de IA treinado nos textos clássicos para analisar o mundo, os memes e as contradições do capital com um rigoroso materialismo histórico-dialético.

---

### 🤔 O que é isso?

Você já se perguntou como Karl Marx analisaria a "uberização" do trabalho, a cultura dos influenciadores digitais ou o último meme que viralizou? Eu também.

Este projeto é um experimento divertido que busca criar um "personagem" de IA com uma persona específica e bem fundamentada. Usando o poder dos Modelos de Linguagem (LLMs) e algumas técnicas de engenharia, construí um agente que não apenas *fala* como um marxista, mas que *pensa* com base nos textos clássicos, consultando-os em tempo real para formular suas análises.

A ideia não é ser um manifesto político, mas sim um estudo fascinante sobre como podemos dar "personalidade" e "conhecimento especializado" para uma IA, de uma forma que seja ao mesmo tempo engraçada e tecnicamente interessante.

---

### 🧠 A Engenharia por Trás do Agente

Este projeto não é apenas um `if/else` glorificado. Ele combina alguns dos conceitos mais modernos em aplicações de IA generativa:

* **LangChain**: O esqueleto da operação. Usei o LangChain para orquestrar todas as peças, criando um **agente** que tem acesso a ferramentas e a uma memória para manter conversas coerentes. É o que permite que a IA raciocine sobre quando e como usar seu conhecimento.

* **RAG (Retrieval-Augmented Generation)**: Esta é a alma do projeto. Em vez de depender apenas do conhecimento genérico do LLM, eu criei uma base de conhecimento vetorial com trechos do "Manifesto Comunista", "O Capital", etc.
    * Quando você faz uma pergunta, o sistema primeiro busca os trechos mais relevantes desses textos clássicos.
    * Esses trechos são então enviados para o LLM junto com a sua pergunta, dando a ele o contexto necessário para formular uma resposta precisa e fundamentada. É como fazer uma prova com consulta, mas a consulta é a obra completa de Marx!
    * Para isso, utilizei `sentence-transformers` para criar os embeddings (vetores numéricos) e `FAISS` para construir um banco de dados vetorial super eficiente.

* **Google Gemini (LLM)**: O cérebro que gera o texto. Usei o modelo `gemini-1.5-flash-latest` do Google, que é rápido, inteligente e acessível via API. Ele atua como o processador final, recebendo as instruções, os textos recuperados pelo RAG e a sua pergunta para gerar a análise final.

* **Prompt Engineering**: A "personalidade" do agente não surge do nada. Ela foi cuidadosamente moldada através de um *prompt de sistema* detalhado, que instrui o LLM a atuar consistentemente como um intelectual marxista, a usar uma terminologia específica e a rebater argumentos contrários.

* **Streamlit**: A interface web amigável que você vê foi construída com Streamlit. Ele transforma um script Python em uma aplicação web interativa, tornando o projeto acessível para qualquer pessoa usar sem precisar tocar em uma linha de código.

---

### 🚀 Como Rodar Localmente

Quer ver o agente em ação na sua máquina? É fácil!

1.  **Clone o repositório:**

2.  **Crie um ambiente virtual (altamente recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    Temos um arquivo `requirements.txt` com tudo que você precisa.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run marxist_agent.py
    ```

5.  **Configure sua API Key:**
    Abra a aplicação no navegador, vá na barra lateral e insira sua chave da API do Google AI Studio.

---

### 💡 Próximos Passos e Contribuições

Este projeto é só o começo! Algumas ideias para o futuro:
* Expandir a base de conhecimento com mais textos (Lênin, Gramsci, etc.).
* Dar ao agente acesso a novas ferramentas, como uma busca na web para analisar notícias em tempo real.
* Criar outras "personalidades" de IA (um agente anarcocapitalista? um filósofo estoico?).

Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*!

---
*Disclaimer: Este é um projeto de estudo e entretenimento. As análises são geradas por uma IA e não devem ser consideradas como aconselhamento político ou acadêmico. Divirta-se!*

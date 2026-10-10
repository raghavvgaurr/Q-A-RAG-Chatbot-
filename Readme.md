# 💬 Universal QA Assistant

### One assistant. Two ways to get answers.

A conversational AI application that combines **Groq-powered general chat** with **Retrieval-Augmented Generation (RAG)** to answer questions from uploaded PDF documents.

Ask general questions, explore your documents, view retrieved source passages, and ask follow-up questions — all through a single Streamlit interface.

\<p align="center">
&#x20; \<img src="[https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)" alt="Python">
&#x20; \<img src="[https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)" alt="Streamlit">
&#x20; \<img src="[https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge)" alt="LangChain">
&#x20; \<img src="[https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)" alt="Groq">
\</p>

---

## ✨ Overview

Universal QA Assistant brings two capabilities together in one application:

- **General Chat:** Ask questions and receive AI-generated answers without uploading a document.
- **Document RAG:** Upload PDF files and ask questions using information retrieved from their contents.

The application retrieves relevant text passages, generates answers using a Groq-hosted language model, and displays source excerpts with page references.

The goal is to make document-based question answering more interactive, transparent, and useful.

## 📸 Application Preview

### 1. Document Question Answering

Upload a PDF, create embeddings, and explore the document through natural-language questions.

### 2. Context-Aware Responses

View the retrieved document passages used to generate an answer, including their filenames and page numbers.

### 3. General AI Chat

Ask questions outside your documents using the same conversational interface.

> Add screenshots of your application here to showcase the interface, PDF retrieval, and generated answers.

---

## 🚀 Features

| Feature                 | Description                                                                      |
| ----------------------- | -------------------------------------------------------------------------------- |
| 💬 General Chat         | Ask questions without uploading documents.                                       |
| 📄 PDF Upload           | Upload one or more PDF files through the interface.                              |
| 🧠 Semantic Search      | Retrieve relevant passages using Hugging Face embeddings.                        |
| ⚡ FAISS Vector Search   | Search document chunks efficiently using vector similarity.                      |
| 🔗 RAG Pipeline         | Generate answers grounded in retrieved document context.                         |
| 💭 Conversation Memory  | Use recent chat history to understand follow-up questions.                       |
| 📚 Source References    | Inspect retrieved passages, filenames, and page numbers.                         |
| 🎛️ Model Configuration | Configure the Groq model, temperature, and response length.                      |
| 🧩 Modular Architecture | Separate document loading, splitting, retrieval, prompts, and application logic. |

---

## 🏗️ Architecture

```text
                    USER
                      |
                      v
              STREAMLIT INTERFACE
                      |
             +--------+--------+
             |                 |
             v                 v
        GENERAL CHAT       DOCUMENT RAG
             |                 |
             |           PDF DOCUMENTS
             |                 |
             |                 v
             |           TEXT EXTRACTION
             |                 |
             |                 v
             |           TEXT CHUNKING
             |                 |
             |                 v
             |          HUGGING FACE
             |            EMBEDDINGS
             |                 |
             |                 v
             |            FAISS INDEX
             |                 |
             |                 v
             |         RELEVANT CONTEXT
             |                 |
             +--------+--------+
                      |
                      v
               GROQ LANGUAGE MODEL
                      |
                      v
               GENERATED ANSWER
                      |
                      v
            CHAT HISTORY + SOURCES
```

The general chat path answers questions directly. The RAG path retrieves relevant document passages before generating an answer.

Conversation history helps interpret follow-up questions in both modes.

---

## 🛠️ Tech Stack

**Language and interface**

- Python
- Streamlit

**LLM and orchestration**

- Groq API
- LangChain
- LangChain Core

**Document processing and retrieval**

- PyPDF
- Recursive Character Text Splitter
- Hugging Face Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2`
- FAISS

**Configuration**

- Python dotenv
- Environment variables

---

## 📂 Project Structure

```text
ChatBot/
│
├── app.py                 # Streamlit interface
├── utils.py               # LLM and QA/RAG logic
├── loader.py              # PDF loading and metadata
├── text_splitter.py       # Document chunking
├── vector_store.py        # Embeddings and FAISS
├── memory.py              # Conversation history
├── prompts.py             # LLM prompt templates
│
├── requirements.txt       # Python dependencies
├── .env                   # Local API key (not committed)
├── .env.example           # Environment template
├── .gitignore             # Excluded files
│
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

---

## ⚙️ Getting Started

### Prerequisites

Before running the application, make sure you have:

- Python 3.10 or later
- A Groq API key
- Git
- Internet access for API requests and the initial embedding-model download

### 1. Clone the repository

```bash
git clone https://github.com/raghavvgaurr/Q-A-Chatbot.git
cd Q-A-Chatbot
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Obtain your API key from the [Groq Console](https://console.groq.com/).

Never commit your real API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to start using the assistant.

---

## 📖 How to Use

### General Chat

1. Launch the application.
2. Enter your Groq API key if it is not configured in `.env`.
3. Select a language model.
4. Choose **General Chat**.
5. Enter your question and review the response.

### Document-Based Question Answering

1. Upload one or more PDF files from the sidebar.
2. Click **Create Embeddings**.
3. Wait for document processing and indexing to finish.
4. Select **Document RAG** or use **Auto** mode.
5. Ask a question about the uploaded documents.
6. Expand the source section to inspect the retrieved passages and page references.
7. Ask follow-up questions to explore the same subject in more detail.

### Answering Modes

- **Auto:** Uses document retrieval whenever a document index is available; otherwise, uses general chat.
- **General Chat:** Answers without retrieving PDF content.
- **Document RAG:** Requires an indexed document collection.

---

## 🧠 How RAG Works

Retrieval-Augmented Generation combines information retrieval with language generation.

**Step 1 — Document loading**

PDF pages are extracted into text documents while retaining page metadata.

**Step 2 — Text splitting**

Long documents are split into smaller, overlapping chunks.

**Step 3 — Embedding generation**

Each chunk is converted into a numerical vector using a Sentence Transformers embedding model.

**Step 4 — Vector indexing**

FAISS stores the vectors and supports similarity-based retrieval.

**Step 5 — Context retrieval**

The system retrieves the most relevant chunks for the user's question.

**Step 6 — Answer generation**

The retrieved passages, question, and recent conversation history are passed to the Groq language model.

**Step 7 — Source display**

The interface displays the answer and the passages retrieved from the documents.

This approach helps ground answers in document content, although retrieval and generated answers can still be incorrect.

---

## 🔐 Security and Limitations

- Store API keys in `.env` locally or in your hosting platform's secret manager.
- Keep `.env`, virtual environments, and other sensitive files out of Git.
- Uploaded PDFs are processed in the active application session.
- The current FAISS index is held in memory and is not permanently stored.
- Conversation history is session-based and is not a persistent user database.
- Auto mode currently selects RAG whenever a document index exists, even for unrelated questions.
- Scanned PDFs may require OCR before their contents can be searched.
- Large PDFs and embedding-model downloads may increase processing time and memory usage.

---

## 🛣️ Roadmap

- [ ] General-purpose AI chat
- [ ] PDF document ingestion
- [ ] Embeddings and FAISS retrieval
- [ ] Document-grounded answers
- [ ] Session-based conversation history
- [ ] Retrieved source passages and page references
- [ ] Smarter routing between general chat and RAG
- [ ] Persistent conversation memory
- [ ] Persistent vector storage
- [ ] Support for DOCX, TXT, CSV, and web sources
- [ ] Hybrid search and reranking
- [ ] External tools and agent-based workflows
- [ ] Automated testing and CI/CD deployment

---

## ☁️ Deployment

The application can be deployed using:

- [Streamlit Community Cloud](https://share.streamlit.io/) — quick portfolio deployment.
- [Render](https://render.com/) — hosted web application.
- [Hugging Face Spaces](https://huggingface.co/spaces) — AI application demos, subject to supported runtime configuration.
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) — managed application deployment.
- Docker with a container-hosting platform — reproducible deployments.

For a first public demo, Streamlit Community Cloud is a practical starting point. For a more advanced portfolio project, add automated testing and CI/CD after the application is working reliably.

---

## 👨‍💻 Author

**Raghav Gaur**

B.Tech — Robotics and Artificial Intelligence

Interested in AI Engineering, Machine Learning, Generative AI, RAG systems, and Robotics.

- GitHub: [@raghavvgaurr](https://github.com/raghavvgaurr)

---

\<p align="center">
&#x20; \<b>Built with Python, Streamlit, LangChain, FAISS, Hugging Face, and Groq.\</b>
&#x20; \<br>
&#x20; Exploring the intersection of conversational AI and knowledge retrieval.
\</p>

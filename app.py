

import os
import sys

import streamlit as st
from dotenv import load_dotenv

# Add the project folder to Python's import path
project_folder = os.path.dirname(os.path.abspath(__file__))

if project_folder not in sys.path:
    sys.path.insert(0, project_folder)

from loader import load_pdf
from text_splitter import split_documents
from vector_store import create_embeddings, create_vector_store
from memory import (
    initialize_memory,
    get_history,
    add_message,
    clear_memory,
)
from utils import (
    create_llm,
    answer_general,
    answer_with_rag,
)


load_dotenv()

st.set_page_config(
    page_title="Universal QA Assistant",
    page_icon="💬",
    layout="wide",
)

st.title("Universal QA Assistant")
st.caption("Chat with AI or ask questions about your PDF documents.")

# Start a new conversation if this is the first run
initialize_memory()

if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar settings
with st.sidebar:
    st.header("Model Settings")

    api_key = st.text_input(
        "Groq API key",
        type="password",
        help="You can also set GROQ_API_KEY in your .env file.",
    )

    model_name = st.selectbox(
        "Choose a model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ],
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
    )

    max_tokens = st.slider(
        "Maximum response length",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
    )

    st.divider()
    st.header("Your Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Create Embeddings", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            try:
                with st.spinner("Reading and processing PDFs..."):
                    documents = []

                    for uploaded_file in uploaded_files:
                        documents.extend(load_pdf(uploaded_file))

                    chunks = split_documents(documents)
                    embedding_model = create_embeddings()

                    st.session_state.vector_store = create_vector_store(
                        chunks,
                        embedding_model,
                    )

                    st.session_state.indexed_files = [
                        file.name for file in uploaded_files
                    ]

                st.success(
                    f"Processed {len(uploaded_files)} PDF(s) "
                    f"into {len(chunks)} text chunks."
                )

            except Exception as error:
                st.error(f"Could not process the documents: {error}")

    if "vector_store" in st.session_state:
        st.success("Your documents are ready.")

        if st.button("Remove Documents", use_container_width=True):
            st.session_state.pop("vector_store", None)
            st.session_state.pop("indexed_files", None)
            st.rerun()

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        clear_memory()
        st.rerun()


# Choose how questions should be answered
answer_mode = st.radio(
    "Chat Mode",
    ["Auto", "General Chat", "Document RAG"],
    horizontal=True,
    help=(
        "Auto uses document retrieval when an index is available. "
        "General Chat answers without document retrieval."
    ),
)

if "vector_store" in st.session_state:
    file_names = st.session_state.get("indexed_files", [])
    st.caption("Indexed documents: " + ", ".join(file_names))


# Show the previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        sources = message.get("sources", [])

        if sources:
            with st.expander("View document sources"):
                for source in sources:
                    st.markdown(
                        f"**{source['source']} — Page {source['page']}**"
                    )
                    st.write(source["content"])
                    st.divider()


# Accept the next question
question = st.chat_input("Ask a question...")

if question:
    try:
        # Keep the conversation history for follow-up questions
        history = get_history()

        add_message("user", question)

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = create_llm(
                    api_key=api_key or None,
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # Decide whether to use the document retriever
                use_rag = (
                    answer_mode == "Document RAG"
                    or (
                        answer_mode == "Auto"
                        and "vector_store" in st.session_state
                    )
                )

                if use_rag:
                    if "vector_store" not in st.session_state:
                        raise ValueError(
                            "Please upload and index your PDFs first."
                        )

                    result = answer_with_rag(
                        llm=llm,
                        vector_store=st.session_state.vector_store,
                        question=question,
                        history=history,
                        k=4,
                    )

                    answer = result["answer"]
                    sources = result["sources"]

                else:
                    answer = answer_general(
                        llm=llm,
                        question=question,
                        history=history,
                    )
                    sources = []

                st.markdown(answer)

                # Show the passages used to answer the question
                if sources:
                    with st.expander("View document sources"):
                        for source in sources:
                            st.markdown(
                                f"**{source['source']} — "
                                f"Page {source['page']}**"
                            )
                            st.write(source["content"])
                            st.divider()

        add_message(
            "assistant",
            answer,
            sources=sources,
        )

    except Exception as error:
        st.error(f"Something went wrong: {error}")


import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from prompts import (
    GENERAL_PROMPT,
    QUERY_REWRITE_PROMPT,
    RAG_PROMPT,
)
from vector_store import get_retriever


load_dotenv()


DEFAULT_MODEL = "openai/gpt-oss-120b"


def create_llm(api_key=None, model_name=DEFAULT_MODEL,
               temperature=0.2, max_tokens=1000):
    """Create the Groq chat model."""

    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Please provide a Groq API key.")

    return ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def answer_general(llm, question, history=""):
    """Answer a general question using conversation history."""

    chain = GENERAL_PROMPT | llm | StrOutputParser()

    return chain.invoke({
        "question": question,
        "history": history or "No previous conversation.",
    })


def rewrite_query(llm, question, history=""):
    """Convert a follow-up question into a retrieval query."""

    if not history:
        return question

    chain = QUERY_REWRITE_PROMPT | llm | StrOutputParser()

    return chain.invoke({
        "question": question,
        "history": history,
    }).strip()


def answer_with_rag(llm, vector_store, question, history="",
                    k=4):
    """Retrieve document passages and answer from their context."""

    standalone_query = rewrite_query(
        llm, question, history
    )

    retriever = get_retriever(vector_store, k=k)
    documents = retriever.invoke(standalone_query)

    if not documents:
        return {
            "answer": (
                "I couldn't find relevant information in "
                "the uploaded documents."
            ),
            "sources": [],
            "documents": [],
        }

    context = "\n\n".join(
        (
            f"Source: {doc.metadata.get('source', 'Uploaded PDF')}\n"
            f"Page: {int(doc.metadata.get('page', 0)) + 1}\n"
            f"Content:\n{doc.page_content}"
        )
        for doc in documents
    )

    chain = RAG_PROMPT | llm | StrOutputParser()

    answer = chain.invoke({
        "question": question,
        "history": history or "No previous conversation.",
        "context": context,
    })

    sources = []
    for doc in documents:
        sources.append({
            "source": doc.metadata.get(
                "source", "Uploaded PDF"
            ),
            "page": int(doc.metadata.get("page", 0)) + 1,
            "content": doc.page_content,
        })

    return {
        "answer": answer,
        "sources": sources,
        "documents": documents,
    }

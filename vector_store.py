
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def create_vector_store(chunks, embedding_model):
    if not chunks:
        raise ValueError("No chunks available for indexing.")

    return FAISS.from_documents(
        chunks,
        embedding_model
    )


def get_retriever(vector_store, k=4):
    return vector_store.as_retriever(
        search_kwargs={"k": k}
    )

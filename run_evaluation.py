
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langsmith import Client, evaluate

from text_splitter import split_documents
from utils import answer_with_rag, create_llm
from vector_store import create_embeddings, create_vector_store

load_dotenv()

DATASET_NAME = "wttc_rag_test_set"
DEFAULT_DOCS_DIR = Path(__file__).parent / "docs"

client = Client()


def _evaluation_pdf_paths():
    pdf_path = os.getenv("EVALUATION_PDF_PATH")
    if pdf_path:
        path = Path(pdf_path)
        if not path.is_file():
            raise FileNotFoundError(f"Evaluation PDF not found: {path}")
        return [path]

    docs_dir = Path(os.getenv("EVALUATION_DOCS_DIR", DEFAULT_DOCS_DIR))
    paths = sorted(docs_dir.glob("*.pdf"))

    if (
        not os.getenv("EVALUATION_DOCS_DIR")
        and len(paths) == 1
        and paths[0].name == "Stock_Prediction_Project_Report.pdf"
    ):
        raise ValueError(
            "The default docs folder only contains the stock prediction "
            "project report, but this evaluation dataset expects the WTTC "
            "source PDF. Set EVALUATION_PDF_PATH or EVALUATION_DOCS_DIR "
            "to the correct evaluation document."
        )

    return paths


@lru_cache(maxsize=1)
def _evaluation_rag():
    documents = []

    for pdf_path in _evaluation_pdf_paths():
        loader = PyPDFLoader(str(pdf_path))
        loaded_documents = loader.load()

        for document in loaded_documents:
            document.metadata["source"] = pdf_path.name

        documents.extend(loaded_documents)

    if not documents:
        raise ValueError(
            "No evaluation PDFs found. Set EVALUATION_PDF_PATH or "
            "EVALUATION_DOCS_DIR."
        )

    chunks = split_documents(documents)
    embeddings = create_embeddings()
    vector_store = create_vector_store(chunks, embeddings)
    llm = create_llm(
        model_name=os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b"),
        temperature=float(os.getenv("GROQ_TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "1000")),
    )

    return llm, vector_store


def target(inputs: dict) -> dict:
    question = inputs["question"]

    llm, vector_store = _evaluation_rag()
    result = answer_with_rag(
        llm=llm,
        vector_store=vector_store,
        question=question,
        history="",
        k=int(os.getenv("RAG_TOP_K", "4")),
    )

    # Keep the output schema consistent with the dataset.
    if isinstance(result, dict):
        answer = result.get("answer", "")
    else:
        answer = str(result)

    return {"answer": answer}


def answer_check(inputs: dict, outputs: dict, reference_outputs: dict):
    prediction = outputs.get("answer", "").strip().lower()
    expected = reference_outputs.get("answer", "").strip()

    if not prediction:
        return {"key": "answer_present", "score": 0}

    # Special handling for questions whose answer is absent from the PDF.
    if expected.upper().startswith("NOT_IN_DOCUMENT"):
        abstention_phrases = [
            "not in the document",
            "not contain",
            "does not mention",
            "do not contain",
            "cannot find",
            "not provided",
            "insufficient information",
            "doesn't specify",
            "not specified",
        ]

        abstained = any(phrase in prediction for phrase in abstention_phrases)
        return {"key": "correct_abstention", "score": int(abstained)}

    # Initial lexical check only; not a full semantic accuracy metric.
    normalized_expected = expected.lower().strip(" .,!?:;")
    matched = normalized_expected in prediction

    return {"key": "reference_match", "score": int(matched)}


if __name__ == "__main__":
    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[answer_check],
        experiment_prefix="wttc-rag-baseline-v1",
        description="Baseline evaluation of the WTTC PDF RAG assistant",
    )

    print("Evaluation complete.")
    print(results)

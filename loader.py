
from tempfile import NamedTemporaryFile

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(uploaded_file):
    """Load pages from a Streamlit-uploaded PDF."""

    if uploaded_file is None:
        raise ValueError("Please upload a PDF file.")

    if not uploaded_file.name.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    temp_path = None

    try:
        with NamedTemporaryFile(
            suffix=".pdf", delete=False
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        loader = PyPDFLoader(temp_path)
        documents = loader.load()

        for document in documents:
            document.metadata["source"] = uploaded_file.name

        if not documents:
            raise ValueError("No readable pages found in the PDF.")

        return documents

    finally:
        if temp_path:
            import os
            if os.path.exists(temp_path):
                os.remove(temp_path)

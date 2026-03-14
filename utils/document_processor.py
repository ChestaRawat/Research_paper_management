import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(uploaded_file, url_input):

    documents = []

    if uploaded_file is not None:

        file_extension = uploaded_file.name.split(".")[-1].lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{file_extension}"
        ) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        try:
            if file_extension == "pdf":
                loader = PyPDFLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path, encoding="utf-8")

            documents = loader.load()

        finally:
            os.unlink(tmp_path)

    elif url_input and url_input.strip():

        try:
            loader = WebBaseLoader(url_input.strip())
            documents = loader.load()
        except Exception as e:
            print(f"Error loading URL: {e}")
            documents = []

    return documents


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Document split into {len(chunks)} chunks.")
    return chunks


def extract_text(documents):

    full_text = ""
    for doc in documents:
        full_text += doc.page_content + "\n\n"

    return full_text
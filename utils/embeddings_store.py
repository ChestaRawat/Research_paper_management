# Mistral doesn't have its own embedding model in langchain yet
# so we use sentence-transformers which is FREE and runs locally
# No API key needed for embeddings!

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_vector_store(chunks, api_key: str = None):

    if not chunks:
        print("No chunks to embed.")
        return None

    print(f"Total chunks to embed: {len(chunks)}")

    try:
        # FREE local embeddings — no API key needed
        # Downloads once (~90MB), then runs offline
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        print("Building FAISS vector store...")
        vector_store = FAISS.from_documents(chunks, embeddings)

        print("Vector store built successfully!")
        return vector_store

    except Exception as e:
        print(f"Error building vector store: {e}")
        return None


def semantic_search(query: str, vector_store, top_k: int = 4):

    if not vector_store:
        return []

    docs = vector_store.similarity_search(query, k=top_k)
    return docs
# src/rag/vectorstore.py
"""Vector store wrapper for SocrAItes.

Uses ChromaDB (local) to store document chunks and perform similarity
retrieval. This is a minimal implementation suitable for the MVP. In a
production setting you would configure persistence directory, embedding
model, and optionally a reranker.
"""

from __future__ import annotations

import os
from typing import List, Tuple

from chromadb import PersistentClient
from chromadb.utils import embedding_functions

# Environment variable name for the persistence folder (can be overridden)
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

if os.getenv("OPENAI_API_KEY"):
    embeddings = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small",
    )
else:
    # Use default embedding function if API key is missing
    embeddings = embedding_functions.DefaultEmbeddingFunction()


def get_client() -> PersistentClient:
    """Return a Chroma PersistentClient, creating the directory if needed."""
    os.makedirs(PERSIST_DIR, exist_ok=True)
    return PersistentClient(path=PERSIST_DIR)


def get_collection(name: str = "socratic_docs"):
    """Retrieve (or create) a collection for storing document chunks.

    The collection uses the ``embeddings`` function defined above.
    """
    client = get_client()
    if name in client.list_collections():
        return client.get_collection(name)
    else:
        return client.create_collection(name=name, embedding_function=embeddings)


def add_documents(docs: List[str], metadatas: List[dict] | None = None) -> None:
    """Add a list of document *chunks* to the vector store.

    Each chunk becomes a separate record. ``metadatas`` can contain source
    information like ``{"source": "Week5.pdf", "page": 12}``.
    """
    collection = get_collection()
    ids = [f"doc_{i}" for i in range(len(docs))]
    collection.add(ids=ids, documents=docs, metadatas=metadatas or [{}] * len(docs))


def query(query_text: str, k: int = 5) -> List[Tuple[str, float]]:
    """Return the top‑k most similar document chunks for *query_text*.

    Returns a list of ``(document, distance)`` tuples.
    """
    collection = get_collection()
    results = collection.query(query_texts=[query_text], n_results=k)
    docs = results.get("documents", [[]])[0]
    dists = results.get("distances", [[]])[0]
    return list(zip(docs, dists))

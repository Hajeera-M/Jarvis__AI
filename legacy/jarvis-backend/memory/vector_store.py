"""
JARVIS — Vector Store (Memory)
ChromaDB-based memory for storing and retrieving conversation history.
"""

import chromadb
from chromadb.config import Settings
from config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
import uuid
from datetime import datetime

_client = None
_collection = None


def _get_collection():
    """Lazy-initialize ChromaDB client and collection."""
    global _client, _collection
    if _collection is None:
        _client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=CHROMA_PERSIST_DIR,
            anonymized_telemetry=False,
        ))
        _collection = _client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"description": "JARVIS conversation memory"},
        )
    return _collection


def store_interaction(user_message: str, ai_response: str) -> None:
    """
    Store a conversation turn in memory.
    
    Args:
        user_message: What the user said
        ai_response: What JARVIS responded
    """
    collection = _get_collection()
    
    doc_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Store as a combined document for better retrieval
    document = f"User: {user_message}\nJARVIS: {ai_response}"
    
    collection.add(
        ids=[doc_id],
        documents=[document],
        metadatas=[{
            "timestamp": timestamp,
            "user_message": user_message[:500],  # Truncate for metadata
            "type": "conversation",
        }],
    )


def search_memory(query: str, k: int = 3) -> list[str]:
    """
    Search memory for relevant past interactions.
    
    Args:
        query: Search query (usually the current user message)
        k: Number of results to return
    
    Returns:
        List of relevant past conversation strings
    """
    collection = _get_collection()
    
    # Don't search if collection is empty
    if collection.count() == 0:
        return []
    
    results = collection.query(
        query_texts=[query],
        n_results=min(k, collection.count()),
    )
    
    documents = results.get("documents", [[]])[0]
    return documents


def clear_memory() -> None:
    """Clear all stored memories."""
    global _collection
    if _collection is not None:
        _client.delete_collection(CHROMA_COLLECTION_NAME)
        _collection = None


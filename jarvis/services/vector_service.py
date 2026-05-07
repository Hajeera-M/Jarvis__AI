"""
JARVIS — Vector Service
Provides semantic memory and document search via ChromaDB.
"""

import os
import logging
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger("JARVIS")

# Configuration
DATA_DIR = os.path.join(os.getcwd(), "data")
CHROMA_PATH = os.path.join(DATA_DIR, "chroma_db")

class VectorService:
    _client = None
    _collection = None

    @staticmethod
    def _get_client():
        if VectorService._client is None:
            if not os.path.exists(CHROMA_PATH):
                os.makedirs(CHROMA_PATH, exist_ok=True)
            VectorService._client = chromadb.PersistentClient(path=CHROMA_PATH)
        return VectorService._client

    @staticmethod
    def _get_collection():
        if VectorService._collection is None:
            client = VectorService._get_client()
            # Default embedding function (sentence-transformers)
            # This might trigger a download on first use
            emb_fn = embedding_functions.DefaultEmbeddingFunction()
            VectorService._collection = client.get_or_create_collection(
                name="jarvis_memory",
                embedding_function=emb_fn
            )
        return VectorService._collection

    @staticmethod
    def add_memory(text: str, metadata: Dict[str, Any] = None):
        """Adds a piece of text to the semantic memory."""
        try:
            collection = VectorService._get_collection()
            # Generate a unique ID based on timestamp
            import time
            doc_id = f"mem_{int(time.time() * 1000)}"
            collection.add(
                documents=[text],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
            logger.info(f"Added to semantic memory: {text[:50]}...")
        except Exception as e:
            logger.error(f"Vector Add Failed: {e}")

    @staticmethod
    def query_memory(query_text: str, n_results: int = 3, threshold: float = 1.5) -> List[str]:
        """
        Queries the semantic memory for similar past interactions.
        Threshold: 0.0 is exact match, higher is less similar. 
        1.5 is a balanced threshold for conversational context.
        """
        try:
            collection = VectorService._get_collection()
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            if not results['documents'] or not results['distances']:
                return []
                
            # Filter results by distance threshold
            filtered_docs = []
            for doc, dist in zip(results['documents'][0], results['distances'][0]):
                if dist < threshold:
                    filtered_docs.append(doc)
            
            return filtered_docs
        except Exception as e:
            logger.error(f"Vector Query Failed: {e}")
            return []

    @staticmethod
    def ingest_document(file_path: str):
        """Reads a file and adds its content to the vector database."""
        try:
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Simple chunking by paragraph/lines for now
            chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 20]
            
            collection = VectorService._get_collection()
            for i, chunk in enumerate(chunks):
                doc_id = f"doc_{os.path.basename(file_path)}_{i}"
                collection.add(
                    documents=[chunk],
                    metadatas=[{"source": file_path}],
                    ids=[doc_id]
                )
            logger.info(f"Ingested document: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Document Ingestion Failed: {e}")
            return False

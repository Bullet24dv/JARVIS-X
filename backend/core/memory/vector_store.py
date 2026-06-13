import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from loguru import logger

class VectorMemory:
    def __init__(self):
        """Inicializa VectorMemory con ChromaDB en modo persistente local"""
        # Usar directorio persistente local en lugar de servidor remoto
        persist_dir = os.path.join(os.getcwd(), "chroma_data")
        os.makedirs(persist_dir, exist_ok=True)
        
        # Cliente persistente - NO necesita servidor
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Modelo de embeddings multilingüe
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Colecciones de memoria
        self.short_term = self.client.get_or_create_collection("short_term")
        self.long_term = self.client.get_or_create_collection("long_term")
        self.episodic = self.client.get_or_create_collection("episodic")
        self.semantic = self.client.get_or_create_collection("semantic")
        
        logger.info(f"VectorMemory initialized in persistent mode at {persist_dir}")
    
    def add_memory(self, text: str, memory_type: str, metadata: Dict = None):
        """Agrega un recuerdo a la memoria vectorial"""
        embedding = self.embedding_model.encode(text).tolist()
        doc_id = f"{memory_type}_{datetime.now().timestamp()}"
        
        collection = getattr(self, memory_type)
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[metadata or {"timestamp": datetime.now().isoformat(), "text": text}],
            documents=[text]
        )
        logger.debug(f"Memory added: {doc_id}")
    
    def search(self, query: str, memory_type: str, top_k: int = 5) -> List[Dict]:
        """Busca recuerdos similares a la consulta"""
        query_embedding = self.embedding_model.encode(query).tolist()
        collection = getattr(self, memory_type)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
    
    def get_all(self, memory_type: str, limit: int = 100) -> List[Dict]:
        """Obtiene todos los recuerdos de un tipo"""
        collection = getattr(self, memory_type)
        results = collection.get(limit=limit)
        return results
    
    def delete_memory(self, memory_type: str, doc_id: str):
        """Elimina un recuerdo específico"""
        collection = getattr(self, memory_type)
        collection.delete(ids=[doc_id])
        logger.debug(f"Memory deleted: {doc_id}")
    
    def clear_memory(self, memory_type: str):
        """Limpia toda la memoria de un tipo"""
        collection = getattr(self, memory_type)
        # Obtener todos los IDs
        results = collection.get()
        if results and results.get('ids'):
            collection.delete(ids=results['ids'])
        logger.info(f"Cleared memory type: {memory_type}")
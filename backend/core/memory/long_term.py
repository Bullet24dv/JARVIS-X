from backend.core.memory.vector_store import VectorMemory

class LongTermMemory:
    """Memoria de largo plazo usando ChromaDB"""
    
    def __init__(self):
        self.vector_store = VectorMemory()
        
    def store(self, text: str, metadata: dict = None):
        self.vector_store.add_memory(text, "long_term", metadata)
        
    def retrieve(self, query: str, top_k: int = 5):
        return self.vector_store.search(query, "long_term", top_k)
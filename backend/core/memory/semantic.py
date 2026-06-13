from backend.core.memory.vector_store import VectorMemory
from typing import List, Dict

class SemanticMemory:
    """Memoria de hechos y conocimiento general"""
    
    def __init__(self):
        self.vector_store = VectorMemory()
        
    def learn_fact(self, fact: str, source: str = None):
        self.vector_store.add_memory(fact, "semantic", {"source": source})
        
    def recall_facts(self, query: str, top_k: int = 5) -> List[Dict]:
        return self.vector_store.search(query, "semantic", top_k)
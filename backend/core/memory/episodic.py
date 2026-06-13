from backend.core.memory.vector_store import VectorMemory
from typing import List, Dict

class EpisodicMemory:
    """Memoria de eventos y experiencias personales"""
    
    def __init__(self):
        self.vector_store = VectorMemory()
        
    def remember_event(self, event: str, context: dict):
        self.vector_store.add_memory(event, "episodic", context)
        
    def recall_events(self, query: str, top_k: int = 5) -> List[Dict]:
        return self.vector_store.search(query, "episodic", top_k)
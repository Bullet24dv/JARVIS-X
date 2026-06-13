from backend.core.memory.vector_store import VectorMemory
from backend.models.memory import Memory
from typing import List, Dict

class MemoryService:
    def __init__(self):
        self.vector_memory = VectorMemory()
        
    async def add(self, text: str, memory_type: str, user_id: str = None, metadata: dict = None):
        await Memory.store(user_id or "default", text, memory_type, metadata)
        self.vector_memory.add_memory(text, memory_type, metadata)
        
    async def search(self, query: str, memory_type: str, top_k: int = 5) -> List[Dict]:
        return self.vector_memory.search(query, memory_type, top_k)
        
    async def recall_relevant(self, context: str, top_k: int = 10) -> List[Dict]:
        # Buscar en todos los tipos
        results = []
        for mem_type in ["short_term", "long_term", "episodic", "semantic"]:
            res = self.vector_memory.search(context, mem_type, top_k)
            results.extend(res)
        return results[:top_k]
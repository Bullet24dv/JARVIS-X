from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.memory_service import MemoryService

router = APIRouter()
memory_service = MemoryService()

class MemoryEntry(BaseModel):
    text: str
    memory_type: str  # short_term, long_term, episodic, semantic

@router.post("/add")
async def add_memory(entry: MemoryEntry):
    await memory_service.add(entry.text, entry.memory_type)
    return {"status": "added"}

@router.get("/search")
async def search_memory(query: str, memory_type: str = "long_term", top_k: int = 5):
    results = await memory_service.search(query, memory_type, top_k)
    return {"results": results}

@router.get("/recall")
async def recall_context(context: str):
    memories = await memory_service.recall_relevant(context)
    return {"memories": memories}
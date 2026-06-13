from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from backend.services.llm_service import LLMService
from backend.services.auth_service import AuthService

router = APIRouter()

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    provider: str

@router.post("/completion", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Obtiene respuesta del LLM con failover automático"""
    try:
        llm_service = LLMService()
        result = await llm_service.get_response(request.messages, request.temperature)
        return ChatResponse(response=result["content"], provider=result["provider"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
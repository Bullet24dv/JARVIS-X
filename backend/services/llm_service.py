from backend.core.llm_router import LLMRouter
from typing import List, Dict, Any
from loguru import logger

class LLMService:
    def __init__(self):
        self.router = LLMRouter()
        
    async def initialize(self):
        await self.router.initialize()
        
    async def get_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        return await self.router.chat_completion(messages, temperature)
        
    async def stream_response(self, messages: List[Dict[str, str]], temperature: float = 0.7):
        async for chunk in self.router.stream_completion(messages, temperature):
            yield chunk
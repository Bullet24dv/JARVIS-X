import os
import google.generativeai as genai
from typing import List, Dict, Any, AsyncGenerator
from loguru import logger
from .base import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    name = "gemini"
    
    def __init__(self):
        self.model = None
        
    @classmethod
    def is_available(cls) -> bool:
        return bool(os.getenv("GEMINI_API_KEY"))
        
    async def initialize(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Gemini provider initialized")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        # Convertir formato de mensajes
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"Instrucciones: {msg['content']}\n"
            else:
                prompt += f"{msg['role']}: {msg['content']}\n"
        response = await self.model.generate_content_async(prompt, generation_config=genai.types.GenerationConfig(temperature=temperature))
        return {"content": response.text, "provider": self.name}
        
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"Instrucciones: {msg['content']}\n"
            else:
                prompt += f"{msg['role']}: {msg['content']}\n"
        response = await self.model.generate_content_async(prompt, stream=True, generation_config=genai.types.GenerationConfig(temperature=temperature))
        async for chunk in response:
            if chunk.text:
                yield chunk.text
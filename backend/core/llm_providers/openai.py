import os
from openai import AsyncOpenAI
from typing import List, Dict, Any, AsyncGenerator
from loguru import logger
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    name = "openai"
    
    def __init__(self):
        self.client = None
        self.model = "gpt-4o-mini"
        
    @classmethod
    def is_available(cls) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))
        
    async def initialize(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logger.info("OpenAI provider initialized")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return {"content": response.choices[0].message.content, "provider": self.name}
        
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
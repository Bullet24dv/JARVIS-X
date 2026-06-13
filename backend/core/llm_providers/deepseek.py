import os
from openai import AsyncOpenAI
from typing import List, Dict, Any, AsyncGenerator
from loguru import logger
from .base import BaseLLMProvider

class DeepSeekProvider(BaseLLMProvider):
    name = "deepseek"
    
    def __init__(self):
        self.client = None
        self.model = "deepseek-chat"
        
    @classmethod
    def is_available(cls) -> bool:
        return bool(os.getenv("DEEPSEEK_API_KEY"))
        
    async def initialize(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        )
        logger.info("DeepSeek provider initialized")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=False
        )
        return {
            "content": response.choices[0].message.content,
            "provider": self.name,
            "model": self.model
        }
        
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
import os
import aiohttp
import json
from typing import List, Dict, Any, AsyncGenerator
from loguru import logger
from .base import BaseLLMProvider

class OpenRouterProvider(BaseLLMProvider):
    name = "openrouter"
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "openrouter/auto"
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("OPENROUTER_API_KEY"))
        
    async def initialize(self):
        logger.info("OpenRouter provider initialized")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature
            }
            async with session.post(f"{self.base_url}/chat/completions", json=payload, headers=headers) as resp:
                result = await resp.json()
                return {"content": result["choices"][0]["message"]["content"], "provider": self.name}
                
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": True
            }
            async with session.post(f"{self.base_url}/chat/completions", json=payload, headers=headers) as resp:
                async for line in resp.content:
                    if line:
                        line = line.decode().strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            if data != "[DONE]":
                                try:
                                    chunk = json.loads(data)
                                    if "choices" in chunk and chunk["choices"][0].get("delta", {}).get("content"):
                                        yield chunk["choices"][0]["delta"]["content"]
                                except:
                                    pass
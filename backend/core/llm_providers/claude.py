import os
from anthropic import AsyncAnthropic
from typing import List, Dict, Any, AsyncGenerator
from loguru import logger
from .base import BaseLLMProvider

class ClaudeProvider(BaseLLMProvider):
    name = "claude"
    
    def __init__(self):
        self.client = None
        self.model = "claude-3-haiku-20240307"
        
    @classmethod
    def is_available(cls) -> bool:
        return bool(os.getenv("CLAUDE_API_KEY"))
        
    async def initialize(self):
        self.client = AsyncAnthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        logger.info("Claude provider initialized")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        # Convertir formato (Claude usa system message separado)
        system = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                user_messages.append({"role": msg["role"], "content": msg["content"]})
        response = await self.client.messages.create(
            model=self.model,
            system=system,
            messages=user_messages,
            temperature=temperature,
            max_tokens=1024
        )
        return {"content": response.content[0].text, "provider": self.name}
        
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        system = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                user_messages.append({"role": msg["role"], "content": msg["content"]})
        async with self.client.messages.stream(
            model=self.model,
            system=system,
            messages=user_messages,
            temperature=temperature,
            max_tokens=1024
        ) as stream:
            async for text in stream.text_stream:
                yield text
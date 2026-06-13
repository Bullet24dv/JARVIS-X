import asyncio
import random
from typing import AsyncGenerator, Dict, Any, Optional, List
from datetime import datetime
from loguru import logger

from backend.core.llm_providers.base import BaseLLMProvider
from backend.core.llm_providers.deepseek import DeepSeekProvider
from backend.core.llm_providers.openai import OpenAIProvider
from backend.core.llm_providers.gemini import GeminiProvider
from backend.core.llm_providers.claude import ClaudeProvider
from backend.core.llm_providers.ollama import OllamaProvider

class LLMRouter:
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.primary_provider = "deepseek"
        self.fallback_chain = ["deepseek", "openai", "gemini", "claude", "ollama"]
        self.current_provider: Optional[BaseLLMProvider] = None
        self.failure_counts = {}
        self.last_failures = {}
        
    async def initialize(self):
        # DeepSeek
        if DeepSeekProvider.is_available():
            self.providers["deepseek"] = DeepSeekProvider()
            await self.providers["deepseek"].initialize()
        # OpenAI
        if OpenAIProvider.is_available():
            self.providers["openai"] = OpenAIProvider()
            await self.providers["openai"].initialize()
        # Gemini
        if GeminiProvider.is_available():
            self.providers["gemini"] = GeminiProvider()
            await self.providers["gemini"].initialize()
        # Claude
        if ClaudeProvider.is_available():
            self.providers["claude"] = ClaudeProvider()
            await self.providers["claude"].initialize()
        # Ollama
        if OllamaProvider.is_available():
            self.providers["ollama"] = OllamaProvider()
            await self.providers["ollama"].initialize()
            
        # Establecer el primer proveedor disponible
        for name in self.fallback_chain:
            if name in self.providers:
                self.current_provider = self.providers[name]
                break
                
        logger.info(f"LLM Router initialized. Primary: {self.current_provider.name if self.current_provider else 'none'}")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_retries: int = 3) -> Dict[str, Any]:
        errors = []
        for attempt in range(max_retries):
            if not self.current_provider:
                raise Exception("No LLM providers available")
            provider_name = self.current_provider.name
            try:
                response = await self.current_provider.chat_completion(messages, temperature)
                return response
            except Exception as e:
                logger.error(f"Provider {provider_name} failed: {e}")
                errors.append(f"{provider_name}: {e}")
                await self._mark_failure(provider_name)
                # Switch to next provider
                self.current_provider = await self._get_next_provider()
                if not self.current_provider:
                    break
        raise Exception(f"All LLM providers failed: {errors}")
        
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        if not self.current_provider:
            raise Exception("No LLM providers available")
        async for chunk in self.current_provider.stream_completion(messages, temperature):
            yield chunk
            
    async def _get_next_provider(self) -> Optional[BaseLLMProvider]:
        for name in self.fallback_chain:
            if name in self.providers and name != (self.current_provider.name if self.current_provider else ""):
                if self.failure_counts.get(name, 0) < 3:
                    logger.info(f"Failing over to {name}")
                    return self.providers[name]
        return None
        
    async def _mark_failure(self, provider_name: str):
        self.failure_counts[provider_name] = self.failure_counts.get(provider_name, 0) + 1
        self.last_failures[provider_name] = datetime.now()
        asyncio.create_task(self._reset_failure_count(provider_name, 300))
        
    async def _reset_failure_count(self, provider_name: str, delay: int):
        await asyncio.sleep(delay)
        self.failure_counts[provider_name] = 0
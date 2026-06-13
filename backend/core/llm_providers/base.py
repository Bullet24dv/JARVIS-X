from abc import ABC, abstractmethod
from typing import Dict, List, Any, AsyncGenerator, Optional
from loguru import logger

class BaseLLMProvider(ABC):
    name: str = "base"
    
    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        pass
    
    @abstractmethod
    async def initialize(self):
        pass
    
    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        pass
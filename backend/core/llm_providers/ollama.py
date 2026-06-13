import aiohttp
import json
from typing import List, Dict, Any, AsyncGenerator
from loguru import logger
from .base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    name = "ollama"
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "llama3.2:latest"
        
    @classmethod
    def is_available(cls) -> bool:
        # Verificar si Ollama está corriendo
        import requests
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            return r.status_code == 200
        except:
            return False
            
    async def initialize(self):
        # Verificar que el modelo existe, si no, descargar
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/api/tags") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = [m["name"] for m in data.get("models", [])]
                    if self.model not in models:
                        logger.warning(f"Model {self.model} not found in Ollama. Pulling...")
                        async with session.post(f"{self.base_url}/api/pull", json={"name": self.model}) as pull:
                            pass  # esperar
        logger.info("Ollama provider initialized")
        
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": False
            }
            async with session.post(f"{self.base_url}/api/chat", json=payload) as resp:
                result = await resp.json()
                return {"content": result["message"]["content"], "provider": self.name}
                
    async def stream_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": True
            }
            async with session.post(f"{self.base_url}/api/chat", json=payload) as resp:
                async for line in resp.content:
                    if line:
                        data = json.loads(line.decode())
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
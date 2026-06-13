from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from loguru import logger
from backend.core.llm_router import LLMRouter
from backend.core.memory.vector_store import VectorMemory

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, llm_router: LLMRouter, memory: VectorMemory):
        self.name = name
        self.role = role
        self.llm = llm_router
        self.memory = memory
        self.state = "idle"
        self.tasks = []
        self.messages = []
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
        
    async def think(self, prompt: str) -> str:
        """Usa LLM para razonar."""
        messages = [
            {"role": "system", "content": f"Eres {self.name}, un agente especializado en {self.role}. Responde en español latino."},
            {"role": "user", "content": prompt}
        ]
        response = await self.llm.chat_completion(messages)
        return response["content"]
        
    def remember(self, text: str):
        self.memory.add_memory(text, "episodic", {"agent": self.name})
        
    async def delegate(self, agent_name: str, task: Dict) -> Any:
        """Delega tarea a otro agente."""
        from backend.core.agents.orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator.get_instance()
        return await orchestrator.delegate(agent_name, task)
from backend.core.agents.orchestrator import AgentOrchestrator
from backend.core.llm_router import LLMRouter
from backend.core.memory.vector_store import VectorMemory
from typing import Dict, Any
from loguru import logger

class AgentService:
    def __init__(self):
        self.orchestrator = None
        
    async def initialize(self):
        llm_router = LLMRouter()
        await llm_router.initialize()
        memory = VectorMemory()
        self.orchestrator = AgentOrchestrator()
        await self.orchestrator.initialize(llm_router, memory)
        
    async def run_agent(self, agent_name: str, action: str, params: Dict) -> Dict:
        return await self.orchestrator.delegate(agent_name, {"action": action, **params})
        
    async def list_agents(self) -> list:
        return list(self.orchestrator.agents.keys())
        
    async def orchestrate(self, task_description: str) -> Dict:
        routing = await self.orchestrator.route_task(task_description)
        return await self.orchestrator.delegate(routing["agent"], {"action": "process", "task": task_description})
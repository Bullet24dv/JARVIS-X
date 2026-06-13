import asyncio
from loguru import logger
from backend.core.agents.orchestrator import AgentOrchestrator
from backend.core.llm_router import LLMRouter
from backend.core.memory.vector_store import VectorMemory

class AgentManager:
    def __init__(self):
        self.orchestrator = None
        
    async def start(self):
        llm = LLMRouter()
        await llm.initialize()
        memory = VectorMemory()
        self.orchestrator = AgentOrchestrator()
        await self.orchestrator.initialize(llm, memory)
        logger.info("Agent Manager started")
        
    async def run_task(self, agent_name: str, task: dict):
        return await self.orchestrator.delegate(agent_name, task)
        
if __name__ == "__main__":
    manager = AgentManager()
    asyncio.run(manager.start())
    asyncio.get_event_loop().run_forever()
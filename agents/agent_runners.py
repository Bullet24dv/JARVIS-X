import asyncio
from backend.core.agents.programmer import ProgrammerAgent
from backend.core.agents.researcher import ResearcherAgent
from backend.core.llm_router import LLMRouter
from backend.core.memory.vector_store import VectorMemory

async def run_programmer_agent(task: dict):
    llm = LLMRouter()
    await llm.initialize()
    memory = VectorMemory()
    agent = ProgrammerAgent("Programmer", "Developer", llm, memory)
    return await agent.process(task)

async def run_researcher_agent(task: dict):
    llm = LLMRouter()
    await llm.initialize()
    memory = VectorMemory()
    agent = ResearcherAgent("Researcher", "Investigator", llm, memory)
    return await agent.process(task)
import asyncio
from aio_pika import connect_robust, IncomingMessage
from loguru import logger
from backend.core.agents.orchestrator import AgentOrchestrator
from backend.core.llm_router import LLMRouter
from backend.core.memory.vector_store import VectorMemory

class AgentWorker:
    def __init__(self):
        self.orchestrator = None
        
    async def start(self):
        llm = LLMRouter()
        await llm.initialize()
        memory = VectorMemory()
        self.orchestrator = AgentOrchestrator()
        await self.orchestrator.initialize(llm, memory)
        
        connection = await connect_robust("amqp://guest:guest@rabbitmq:5672/")
        channel = await connection.channel()
        queue = await channel.declare_queue("agent_queue", durable=True)
        await queue.consume(self.process_agent_task)
        logger.info("Agent worker started")
        await asyncio.Future()
        
    async def process_agent_task(self, message: IncomingMessage):
        async with message.process():
            import json
            data = json.loads(message.body.decode())
            agent_name = data.get("agent")
            task = data.get("task")
            result = await self.orchestrator.delegate(agent_name, task)
            logger.info(f"Agent {agent_name} result: {result}")
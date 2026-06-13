import asyncio
from aio_pika import connect_robust, IncomingMessage
from loguru import logger
from backend.core.task_queue import task_queue
from backend.services.llm_service import LLMService
from backend.services.computer_service import ComputerService

class TaskWorker:
    def __init__(self):
        self.llm_service = LLMService()
        self.computer_service = ComputerService()
        
    async def start(self):
        connection = await connect_robust("amqp://guest:guest@rabbitmq:5672/")
        channel = await connection.channel()
        queue = await channel.declare_queue("task_queue", durable=True)
        await queue.consume(self.process_task)
        logger.info("Task worker started")
        await asyncio.Future()
        
    async def process_task(self, message: IncomingMessage):
        async with message.process():
            try:
                data = message.body.decode()
                logger.info(f"Processing task: {data}")
                # Lógica de procesamiento
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Task failed: {e}")
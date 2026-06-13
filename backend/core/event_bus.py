import asyncio
from typing import Dict, List, Callable, Any
from loguru import logger

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.queue = asyncio.Queue()
        self.running = False
        
    async def start(self):
        self.running = True
        asyncio.create_task(self._process_events())
        logger.info("Event bus started")
        
    async def stop(self):
        self.running = False
        logger.info("Event bus stopped")
        
    def on(self, event: str, callback: Callable):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
        
    async def emit(self, event: str, data: Any):
        await self.queue.put((event, data))
        
    async def _process_events(self):
        while self.running:
            try:
                event, data = await self.queue.get()
                if event in self.listeners:
                    for callback in self.listeners[event]:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(data)
                            else:
                                callback(data)
                        except Exception as e:
                            logger.error(f"Event callback error: {e}")
            except Exception as e:
                logger.error(f"Event bus error: {e}")

event_bus = EventBus()
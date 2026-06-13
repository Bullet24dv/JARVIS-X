import asyncio
from typing import Any, Callable, Dict
from collections import deque
from loguru import logger

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.workers = []
        self.running = False
        
    async def start(self, num_workers: int = 4):
        self.running = True
        for i in range(num_workers):
            worker = asyncio.create_task(self._worker(i))
            self.workers.append(worker)
        logger.info(f"Task queue started with {num_workers} workers")
        
    async def stop(self):
        self.running = False
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        
    async def add_task(self, task: Callable, *args, **kwargs):
        future = asyncio.Future()
        self.queue.append((task, args, kwargs, future))
        return future
        
    async def _worker(self, worker_id: int):
        while self.running:
            if self.queue:
                task, args, kwargs, future = self.queue.popleft()
                try:
                    if asyncio.iscoroutinefunction(task):
                        result = await task(*args, **kwargs)
                    else:
                        result = task(*args, **kwargs)
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(e)
                    logger.error(f"Worker {worker_id} error: {e}")
            else:
                await asyncio.sleep(0.01)

task_queue = TaskQueue()
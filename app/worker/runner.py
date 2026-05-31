import asyncio
from dataclasses import dataclass
from typing import Protocol

from app.services.batch_processor import BatchExecutionEngine

@dataclass(slots=True)
class WorkerJob:
    job_id: str
    prompt: str
    
class WorkerQueue(Protocol):
    async def pop(self) -> WorkerJob | None: 
        ...
    async def ack(self, job_id: str) -> None:
        ...
    async def fail(self, job_id: str, reason: str | None = None) -> None:
        ...
        
        
class BatchWorker:
    def __init__(
        self, 
        queue: WorkerQueue, 
        engine: BatchExecutionEngine, 
        poll_interval: float = 0.2,
    ) -> None:
        self._queue = queue
        self._engine = engine
        self._poll_interval = poll_interval

    async def run(self) -> None:
        while True:
            job = await self._queue.pop()
            if job is None:
                await asyncio.sleep(self._poll_interval)
                continue
            
            try:
                await self._engine.batch_execute(job.prompt)
                await self._queue.ack(job.job_id)
            except Exception as e:
                print(f"Error processing job {job.job_id}: {e}")
                await self._queue.fail(job.job_id, str(e))
import json

from redis.asyncio import Redis

from app.worker.runner import WorkerJob, WorkerQueue

class RedisWorkerQueue(WorkerQueue):
    def __init__(
        self, redis_url: str, 
        pending_key: str = "llm:jobs:pending", 
        failed_key: str = "llm:jobs:failed"
    ) -> None:
        self._redis = Redis.from_url(redis_url)
        self._pending_key = pending_key
        self._failed_key = failed_key

    async def pop(self) -> WorkerJob | None:
        result = await self._redis.blpop(self._pending_key, timeout=1)
        if result is None:
            return None
        payload = result[1]
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        data = json.loads(payload)
        return WorkerJob(job_id=data["job_id"], prompt=data["prompt"])

    async def ack(self, job_id: str) -> None:
        _ = job_id

    async def fail(self, job_id: str, reason: str | None = None) -> None:
        await self._redis.rpush(
            self._failed_key, 
            json.dumps({"job_id": job_id, "reason": reason or "Unknown error"}),
        )
        
    async def push(self, job: WorkerJob) -> None:
        await self._redis.rpush(
            self._pending_key, 
            json.dumps({"job_id": job.job_id, "prompt": job.prompt}),
        )
        
    async def close(self) -> None:
        await self._redis.aclose()
        
        
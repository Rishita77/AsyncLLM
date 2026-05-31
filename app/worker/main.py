import asyncio

from app.core.settings import get_settings
from app.infra.redis_queue import RedisWorkerQueue
from app.providers.openai_provider import OpenAIProvider
from app.services.batch_processor import BatchExecutionEngine
from app.worker.runner import BatchWorker


async def run_worker() -> None:
    settings = get_settings()
    provider = OpenAIProvider(
        api_key=settings.openai_api_key, 
        model=settings.openai_model, 
        timeout_seconds=settings.request_timeout_seconds
)
    engine = BatchExecutionEngine(provider=provider, settings=settings)
    queue = RedisWorkerQueue(redis_url=settings.redis_url)
    worker = BatchWorker(queue=queue, engine=engine)
    
    try:
        await worker.run()
    finally:
        await provider.aclose()
        await queue.close()
        
        
def main() -> None:
    asyncio.run(run_worker())
    
if __name__ == "__main__":
    main()
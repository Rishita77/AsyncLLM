import asyncio

from app.core.settings import get_settings
from app.infra.redis_queue import RedisWorkerQueue
from app.services.batch_processor import BatchExecutionEngine
from app.worker.runner import BatchWorker
from app.providers.openai_provider import OpenAIProvider

async def run_worker():
    settings = get_settings()
    provider = OpenAIProvider(api_key=settings.openai_api_key, model=settings.openai_model, timeout_seconds=settings.openai_timeout_seconds)
    engine = BatchExecutionEngine(provider=provider)
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
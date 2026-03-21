import asyncio
from models import LLMResponse
from worker import worker
from core.rate_limiter import TokenBucket
from typing import AsyncIterator
from caller import call_llm

async def run_batch(prompts: list, num_workers: int=5) -> AsyncIterator[LLMResponse]:
    queue = asyncio.Queue()
    result_queue = asyncio.Queue()
    
    request_bucket = TokenBucket(rate=120/60, capacity=60)
    token_bucket = TokenBucket(rate=10000/60, capacity=10000)
    
    for i, p in enumerate(prompts):
        await queue.put((str(i),p))
        
    workers =  [
        asyncio.create_task(worker(f"W{i}", queue, result_queue, request_bucket, token_bucket, call_llm))
        for i in range(num_workers)
    ]
    
    async def result_stream():
        finished_workers = 0
        
        while finished_workers < num_workers:
            result = await result_queue.get()
            
            if result is None:
                finished_workers += 1
                continue
            
            yield result
        
    async def shutdown():
        await queue.join()
        
        for _ in workers:
            await queue.put(None)
            
        await asyncio.gather(*workers)
        
        for _ in workers:
            await result_queue.put(None)
            
    asyncio.create_task(shutdown())
    
    return result_stream()
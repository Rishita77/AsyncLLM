import asyncio
from models import LLMResponse
from typing import List
from worker import worker

async def run_batch(prompts: list, num_workers: int=5) -> List[LLMResponse]:
    queue = asyncio.Queue()
    results: List[LLMResponse] = []
    
    for i, p in enumerate(prompts):
        await queue.put((str(i),p))
        
    workers =  [
        asyncio.create_task(worker(f"W{i}", queue, results))
        for i in range(num_workers)
    ]
    
    await queue.join()
    
    for _ in workers:
        await queue.put(None)
        
    await asyncio.gather(*workers)
    
    return results
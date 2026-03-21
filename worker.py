import asyncio
from models import LLMResponse
from typing import List
import time
from caller import call_llm
from core.rate_limiter import TokenBucket
from core.retry import retry_with_backoff

async def worker(worker_id: str, queue: asyncio.Queue, result_queue: asyncio.Queue, request_bucket: TokenBucket, token_bucket: TokenBucket):
    while True:
        
        item = await queue.get()
        
        if item is None:
            queue.task_done()
            break
        
        prompt_id, prompt = item
        
        start = time.perf_counter()
        
        try:
            output = await retry_with_backoff(
                lambda: call_llm(prompt, request_bucket, token_bucket)
            )
            
            result = LLMResponse(
                request_id=prompt_id,
                output_text=output,
                start_time=start,
                end_time = time.perf_counter(),
            )
            
        except Exception as e:
            result = LLMResponse(
                request_id=prompt_id,
                error=str(e),
                start_time=start,
                end_time=time.perf_counter(),
            )
            
        await result_queue.put(result)
        
        queue.task_done()
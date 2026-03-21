import asyncio
from models import LLMResponse
from typing import List
import time
from caller import call_llm

async def worker(worker_id: str, queue: asyncio.Queue, results: List[LLMResponse]):
    while True:
        
        item = await queue.get()
        
        if item is None:
            queue.task_done()
            break
        
        prompt_id, prompt = item
        
        start = time.time()
        
        try:
            output = await call_llm(prompt)
            
            result = LLMResponse(
                request_id=prompt_id,
                output_text=output,
                start_time=start,
                end_time = time.time(),
            )
            
        except Exception as e:
            result = LLMResponse(
                request_id=prompt_id,
                error=str(e),
                start_time=start,
                end_time=time.time(),
            )
            
        results.append(result)
        
        queue.task_done()
import asyncio
import random

async def retry_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            wait = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(wait)
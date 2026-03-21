import asyncio
import time

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.perf_counter()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1):
        async with self.lock:
            while True:
                now = time.perf_counter()
                elapsed = now - self.last_refill

                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate
                )
                self.last_refill = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return

                wait_time = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
import asyncio
import random
from collections.abc import Callable, Awaitable
from typing import TypeVar

from app.core.errors import ProviderError

T = TypeVar("T")

def is_retyable(exc: Exception) -> bool:
    return isinstance(exc, (ProviderError, TimeoutError, asyncio.TimeoutError))

async def retry_with_backoff(func: Callable[[], Awaitable[T]], max_retries: int, 
                             base_delay_seconds: float) -> tuple[T, int]:
    """Retry an async function with exponential backoff."""
    attempt = 0
    
    while True:
        try:
            return await func(), attempt + 1
        except Exception as exc:
            if not is_retyable(exc) or attempt >= max_retries:
                raise
            delay = (2 ** attempt) * base_delay_seconds
            jitter = delay + random.uniform(0, delay/4)
            await asyncio.sleep(jitter)
            attempt += 1
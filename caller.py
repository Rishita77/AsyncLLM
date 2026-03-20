import asyncio
import logging
import time
from typing import Callable, Optional, AsyncIterator

from openai import AsyncOpenAI, APIStatusError, APIConnectionError, RateLimitError

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[LLMResult], None]

class AsyncLLMBatchCaller:
    """Sends a list of LLM requests to OpenAI concurrently with rate limiting, retries and progress reporting
    """
    
    def __init__(
        self,
        api_key: str | None = None,
        max_concurrent: int = 10,
        rpm: int = 60,
        tpm: int = 90_000,
        max_retries: int = 0,
    ):
        self.client = AsyncOpenAI(api_key=api_key, max_retries=max_retries)
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._rate_limiter = TokenBucketRateLimiter(rpm=rpm, tpm=tpm)
        self._retry_config = RetryConfig() or retry_config
        
    async def close(self) -> None:
        await self.client.close()
        
    async def __aenter__(self) -> "AsyncLLMBatchCaller":
        return self
    
    async def __aexit__(self, *_) -> None:
        await self.close()
        
    async def run_batch(
        self,
        requests: list[LLMRequest],
        progress_callback: Optional[ProgressCallback] = None,
    ) -> tuple[list[LLMResult], BatchSummary]:
        """Run a batch of LLM requests concurrently with rate limiting and retries.
        
        Args:
            requests: A list of LLMRequest objects to send to OpenAI.
            progress_callback: An optional callback function that will be called with each LLMResult as it is received.
            
        Returns:
            A list of LLMResult objects corresponding to the input requests, in the same order.
        """
        tasks = [self._run_single_request(request, progress_callback) for request in requests]
        return await asyncio.gather(*tasks
    )
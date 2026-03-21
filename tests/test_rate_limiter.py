import pytest
import asyncio
from core.rate_limiter import TokenBucket

@pytest.mark.asyncio
async def test_token_bucket_enforces_rate():
    bucket = TokenBucket(rate=1, capacity=1)

    start = asyncio.get_event_loop().time()

    await bucket.acquire()
    await bucket.acquire()

    end = asyncio.get_event_loop().time()

    assert end - start >= 1
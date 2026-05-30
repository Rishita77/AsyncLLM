import asyncio
from collections.abc import Awaitable
from typing import TypeVar

from app.core.errors import ProviderTimeoutError

T = TypeVar("T")


async def with_timeout(task: Awaitable[T], timeout_seconds: float) -> T:
    """Run an async function with a timeout."""
    try:
        async with asyncio.timeout(timeout_seconds):
            return await task
    except TimeoutError as exc:
        raise ProviderTimeoutError(f"Operation timed out after {timeout_seconds:.2f} seconds") from exc
import pytest
import asyncio
import time
from batch_processor import run_batch

@pytest.mark.asyncio
async def test_streaming_results_arrive_incrementally():

    prompts = ["a", "b", "c"]

    async def slow_call(prompt, *_):
        await asyncio.sleep(0.5)
        return prompt

    stream = await run_batch(prompts)

    times = []

    async for result in stream:
        times.append(time.perf_counter())

    intervals = [
        t2 - t1 for t1, t2 in zip(times, times[1:])
    ]

    assert any(interval > 0.1 for interval in intervals)
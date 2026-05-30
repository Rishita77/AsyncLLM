import argparse
import asyncio
import time
import tracemalloc
from time import perf_counter

from app.core.settings import Settings
from app.providers.base import ProviderResult, ProviderUsage
from app.services.batch_processor import BatchExecutionEngine


class FakeProvider:
    def __init__(self, response_time: float) -> None:
        self._response_time = response_time

    async def batch_execute(self, prompt: str) -> ProviderResult:
        await asyncio.sleep(self._response_time)
        return ProviderResult(response=f"Echo: {prompt}", usage=ProviderUsage(tokens=10, latency=self._response_time))
    
    async def aclose(self) -> None:
        return None
    
async def run_benchmark(batch_size: int, latency: float):
    prompts = [f"Prompt {i} for batch size {batch_size}" for i in range(batch_size)]
    settings = Settings(
        OPENAI_API_KEY="fake-api-key",
        request_timeout_seconds=30,
        max_retries=0,
    )
    provider = FakeProvider(response_time=latency)
    engine = BatchExecutionEngine(provider=provider)
    tracemalloc.start()
    start = perf_counter()
    await engine.batch_execute(prompts, concurrency=1)
    elapsed = perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    current_mb = current / (1024 * 1024)
    peak_mb = peak / (1024 * 1024)
    print(f"Batch size: {batch_size}, Latency: {latency:.2f}s, Total time: {elapsed:.2f}s, Current memory usage: {current_mb:.2f} MB, Peak memory usage: {peak_mb:.2f} MB")
    
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark the batch processing engine with a fake provider.")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of prompts to include in each batch.")
    parser.add_argument("--latency", type=float, default=1.0, help="Simulated response time of the fake provider in seconds.")
    return parser.parse_args()
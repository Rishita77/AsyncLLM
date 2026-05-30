import argparse
import asyncio
from asyncio import tasks
from time import perf_counter
import math

from app.core.settings import Settings
from app.providers.base import ProviderResult, ProviderUsage
from app.services.batch_processor import BatchExecutionEngine


class FakeProvider:
    def __init__(self, response_time: float) -> None:
        self._response_time = response_time

    async def batch_execute(self, prompt: str) -> ProviderResult:
        await asyncio.sleep(self._response_time)
        return ProviderResult(response=f"Echo: {prompt}", usage=ProviderUsage(prompt_tokens=10, completion_tokens=25))
    
    async def aclose(self) -> None:
        return None
    
def percentile(data: list[float], p: float) -> float:
    if not data:
        return 0.0
    ordered = sorted(data)
    index = min(max(0, math.ceil(p / 100 * len(ordered)) - 1), len(ordered) - 1)
    return ordered[index]

async def run_benchmark(batch_size: int, concurrency: int, latency: float):
    prompts = [f"Prompt {i} for batch size {batch_size}" for i in range(batch_size)]
    settings = Settings(
        OPENAI_API_KEY="fake-api-key",
        max_concurrency=concurrency,
        request_timeout_seconds=30,
        max_retries=0,
    )
    provider = FakeProvider(response_time=latency)
    engine = BatchExecutionEngine(provider=provider)

    start_time = perf_counter()
    results = await engine.batch_execute(prompts, concurrency=concurrency)
    elapsed_time = perf_counter() - start_time
    
    latencies = [result.usage.latency for result in results]
    print(f"Batch size: {batch_size}, Concurrency: {concurrency}, Latency: {latency:.2f}s, Total time: {elapsed_time:.2f}s, 50th percentile latency: {percentile(latencies, 50):.2f}s, 95th percentile latency: {percentile(latencies, 95):.2f}s")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark the batch processing engine with a fake provider.")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of prompts to include in each batch.")
    parser.add_argument("--concurrency", type=int, default=5, help="Number of concurrent requests to make to the provider.")
    parser.add_argument("--latency", type=float, default=1.0, help="Simulated response time of the fake provider in seconds.")
    return parser.parse_args()


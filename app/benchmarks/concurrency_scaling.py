import argparse
import asyncio
import time
from dataclasses import dataclass
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
    
@dataclass(slots=True)
class ScalingResult:
    concurrency: int
    latency: float
    total_time: float
    average_latency: float
    

async def run_benchmark(batch_size: int, concurrency: int, latency: float) -> ScalingResult:
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
    average_latency = sum(latencies) / len(latencies) if latencies else 0.0
    return ScalingResult(concurrency=concurrency, latency=latency, total_time=elapsed_time, average_latency=average_latency)

async def run_scaling_benchmarks(batch_size: int, latencies: list[float], concurrencies: list[int]):
    for latency in latencies:
        for concurrency in concurrencies:
            result = await run_benchmark(batch_size=batch_size, concurrency=concurrency, latency=latency)
            print(f"Concurrency: {result.concurrency}, Simulated Latency: {result.latency:.2f}s, Total Time: {result.total_time:.2f}s, Average Latency: {result.average_latency:.2f}s")
            
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark the batch processing engine with a fake provider across different concurrency levels and latencies.")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of prompts to include in each batch.")
    parser.add_argument("--latencies", type=float, nargs="+", default=[0.5, 1.0, 2.0], help="List of simulated response times for the fake provider in seconds.")
    parser.add_argument("--concurrencies", type=int, nargs="+", default=[1, 5, 10], help="List of concurrency levels to test.")
    return parser.parse_args()
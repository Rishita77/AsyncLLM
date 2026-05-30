import argparse
import asyncio
import time

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
    
async def run_benchmark(settings: Settings):
    provider = FakeProvider(response_time=settings.fake_provider_response_time)
    engine = BatchExecutionEngine(provider=provider)

    start_time = time.perf_counter()
    await engine.batch_execute("Hello, world!")
    end_time = time.perf_counter()

    print(f"Total latency: {end_time - start_time:.2f} seconds")
    
def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark the batch processing engine with a fake provider.")
    parser.add_argument("--response-time", type=float, default=1.0, help="Simulated response time of the fake provider in seconds.")
    return parser.parse_args()

def main():
    args = parse_args()
    settings = Settings(fake_provider_response_time=args.response_time)
    asyncio.run(run_benchmark(settings))
    
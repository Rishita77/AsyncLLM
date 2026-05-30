import asyncio
import pytest

from app.core.settings import Settings
from app.services.batch_processor import BatchExecutionEngine, compute_batch_metrics
from app.models.domain import BatchItemStatus
from app.providers.base import ProviderResult, ProviderUsage

class FakeProvider:
    async def execute(self, prompt: str) -> ProviderResult:
        await asyncio.sleep(0.01)  # Simulate some processing time
        return ProviderResult(
            output=f"Processed: {prompt}", 
            usage=ProviderUsage(prompt_tokens=5, completion_tokens=5),
        )
        
    async def aclose(self) -> None:
        return None
    
@pytest.mark.asyncio
async def test_batch_processor_returns_successful_results() -> None:
    settings = Settings(
        OPENAI_API_KEY="test_key",
        max_concurrency=2,
        max_retries=1,
        request_timeout_seconds=1.0,
    )
    engine = BatchExecutionEngine(provider=FakeProvider(), settings=settings)
    prompts = ["a", "b"]
    results = await engine.batch_execute(prompts, concurrency=2)
    
    assert len(results) == len(prompts)
    for i, result in enumerate(results):
        assert result.status == BatchItemStatus.SUCCESS
        assert result.output_text == f"Processed: {prompts[i]}"
        assert result.total_tokens == 12
        
        
@pytest.mark.asyncio
async def test_compute_batch_metrics_summarizes_results() -> None:
    Settings = Settings(
        OPENAI_API_KEY="test_key"
    )
    engine = BatchExecutionEngine(provider=FakeProvider(), settings=Settings)
    results = await engine.batch_execute(["only prompt"], concurrency=1)
    metrics = compute_batch_metrics(results)
    
    assert metrics.total_requests == 1
    assert metrics.successful_items == 1
    assert metrics.failed_items == 0
    assert metrics.cancelled_requests == 0
    assert metrics.average_latency_ms >=  0
    assert metrics.p95_latency_ms >= 0
    
    
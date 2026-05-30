import asyncio
import statistics
import time
import uuid
from collections.abc import Sequence

from app.core.errors import ProviderTimeoutError
from app.core.retry import retry_with_exponential_backoff
from app.core.settings import Settings
from app.providers.base import LLMProvider, ProviderResult, ProviderUsage
from app.core.timeout import with_timeout
from app.models.domain import BatchItemStatus, BatchMetrics, BatchResult

class BatchExecutionEngine:
    def __init__(self, provider: LLMProvider, settings: Settings) -> None:
        self._provider = provider
        self._settings = settings
        
    @property
    def provider(self) -> LLMProvider:
        return self._provider
    
    def _estimate_prompt_tokens(self, prompt: str) -> int:
        return max(1, int(len(prompt.split()) * self.settings.estimated_input_token_multiplier))
    
    def _estimate_cost_usd(self, usage: ProviderUsage) -> float:
        input_cost = (usage.input_tokens / 1_000_000) * self.settings.input_token_usd_per_1m
        output_cost = (usage.output_tokens / 1_000_000) * self.settings.output_token_usd_per_1m
        return round(input_cost + output_cost, 8)
    
    async def _run_single(self, request_id: str, prompt: str, semaphore: asyncio.Semaphore) -> BatchResult:
        start = time.perf_counter()
        
        async def execute_once() -> None:
            async with semaphore:
                return await with_timeout(
                    self.provider.generate(prompt),
                    timeout=self.settings.provider_timeout_seconds,
                    timeout_seconds = self._settings.retry_backoff_seconds
                )
            
        try:
            provider_result, attempts = await retry_with_exponential_backoff(
                operation=execute_once,
                max_attempts=self._settings.max_retries,
                base_delay_seconds = self._settings.retry_backoff_seconds,
            )
            
            usage = provider_result.usage
            status = BatchItemStatus.SUCCESS
            error = None
            output_text = provider_result.output_text
        except ProviderTimeoutError as e:
            attempts = self._settings.max_retries+1
            usage = ProviderUsage(input_tokens=self._estimate_prompt_tokens(prompt), completion_tokens=0)
            status = BatchItemStatus.TIMEOUT
            error = "Request timed out"
            output_text = None
        except asyncio.CancelledError:
            attempts = 1
            usage = ProviderUsage(prompt_tokens=0, completion_tokens=0)
            status = BatchItemStatus.CANCELLED
            error = "Request was cancelled"
            output_text = None
            raise
        except Exception as e:
            attempts = self._settings.max_retries+1
            usage = ProviderUsage(prompt_tokens=self._estimate_prompt_tokens(prompt), completion_tokens=0)
            status = BatchItemStatus.FAILED
            error = str(e)
            output_text = None
        
        latency = (time.perf_counter() - start) * 1000
        
        return BatchResult(
            request_id=request_id,
            prompt=prompt,
            status=status,
            output_text=output_text,
            prompt_tokens=usage.input_tokens,
            completion_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            estimated_cost_usd=self._estimate_cost_usd(usage),
            latency_ms=latency,
            attempts=attempts,
            error=error
        )
        
    async def batch_execute(self, prompts: list[str], concurrency: int | None = None) -> list[BatchResult]:
        
        semaphore = asyncio.Semaphore(concurrency or self._settings.max_concurrency)
        
        results: list[BatchResult] = []
        
        async def wrapped(prompt: str) -> None:
            request_id = str(uuid.uuid4())
            result = await self._run_single(request_id=request_id, prompt=prompt, semaphore=semaphore)
            results.append(result)
        
        try:
            async with asyncio.TaskGroup() as tg:
                for prompt in prompts:
                    tg.create_task(wrapped(prompt))
        except* asyncio.CancelledError:
            raise
        
        results.sort(key=lambda r: r.request_id)
        return results
    
def compute_batch_metrics(results: Sequence[BatchResult]) -> BatchMetrics:
        if not results:
            return BatchMetrics(
                total_items=0,
                successful_items=0,
                failed_items=0,
                timed_out_items=0,
                cancelled_items=0,
                average_latency_ms=0.0,
                median_latency_ms=0.0,
                total_cost_usd=0.0
            )
        
        latencies = [r.latency_ms for r in results]
        # p95 latency is the latency value below which 95% of the latencies fall. We calculate the index for the 95th percentile and get the corresponding latency value.
        p95_latency = max(0, min(len(latencies)-1, int(round((len(latencies) - 1)*0.95))))
        ordered_latencies = sorted(latencies)
        
        return BatchMetrics(
            total_items=len(results),
            successful_items=sum(1 for r in results if r.status == BatchItemStatus.SUCCESS),
            failed_items=sum(1 for r in results if r.status == BatchItemStatus.FAILED),
            timed_out_items=sum(1 for r in results if r.status == BatchItemStatus.TIMEOUT),
            cancelled_items=sum(1 for r in results if r.status == BatchItemStatus.CANCELLED),
            average_latency_ms=statistics.mean(latencies),
            p95_latency_ms=ordered_latencies[p95_latency],
        )
        
        
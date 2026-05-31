from prometheus_client import Counter, Histogram

REQUESTS_TOTAL = Counter(
    "async_llm_requests_total",
    "Total number of requests made to the LLM provider",
    labelnames=("status",),
)

LATENCY_MS = Histogram(
    "async_llm_request_latency_ms",
    "Per-prompt latency in milliseconds",
    buckets=(50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000),
)

TOKENS_TOTAL = Counter(
    "async_llm_tokens_total",
    "Total number of tokens processed by the LLM provider",
    labelnames=("type",), 
)

def record_prompt(status: str, latency_ms: float, prompt_tokens: int, completion_tokens: int):
    REQUESTS_TOTAL.labels(status=status).inc()
    LATENCY_MS.observe(latency_ms)
    TOKENS_TOTAL.labels(type="prompt").inc(prompt_tokens)
    TOKENS_TOTAL.labels(type="completion").inc(completion_tokens)

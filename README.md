# AsyncLLM

An async LLM batch processing client for the OpenAI API, built to be production-grade

## Features

- **Async concurrency** — run N requests in parallel via `asyncio`
- **Token bucket rate limiting** — respect OpenAI's RPM and TPM limits automatically
- **Exponential backoff with jitter** — retry transient failures without thundering herd
- **Streaming results** — get results as they arrive, not all-at-once at the end
- **Structured outputs** — typed results with latency, token usage, and error details
- **Full test suite** — covers rate limiter, retry logic, and error handling


## Architecture

        Input Prompts
            ↓
        Async Queue
            ↓
    Worker Pool (N workers)
            ↓
    Rate Limiter (Token Buckets)
            ↓
        OpenAI API
            ↓
    Retry Layer (Backoff + Jitter)
            ↓
        Result Queue
            ↓
        Streaming Consumer

### Key Components

| Module | Responsibility |
|------|----------------|
| `batch_processor.py` | Orchestrates pipeline + streaming |
| `worker.py` | Executes tasks, handles retries |
| `caller.py` | OpenAI API interaction |
| `core/rate_limiter.py` | Token bucket implementation |
| `core/retry.py` | Retry with exponential backoff |
| `models.py` | Structured response objects |

## Running Tests

```bash
python -m pytest
```
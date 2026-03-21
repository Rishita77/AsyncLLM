# llm-batch-caller

An async LLM batch processing client for the OpenAI API, built to be production-grade

## Features

- **Async concurrency** — run N requests in parallel via `asyncio`
- **Token bucket rate limiting** — respect OpenAI's RPM and TPM limits automatically
- **Exponential backoff with jitter** — retry transient failures without thundering herd
- **Streaming results** — get results as they arrive, not all-at-once at the end
- **Structured outputs** — typed results with latency, token usage, and error details
- **Full test suite** — covers rate limiter, retry logic, and error handling


## Architecture

            ┌──────────────┐
            │ Input Prompts│
            └──────┬───────┘
                   ↓
            ┌──────────────┐
            │ Task Queue   │
            └──────┬───────┘
                   ↓
        ┌──────────────────────┐
        │ Workers (async pool) │
        └──────┬───────────────┘
               ↓
   ┌─────────────────────────────┐
   │ Rate Limiter (token bucket) │
   └────────────┬────────────────┘
                ↓
        ┌──────────────┐
        │ OpenAI API   │
        └──────────────┘
                ↓
   ┌─────────────────────────────┐
   │ Retry + Backoff + Jitter    │
   └────────────┬────────────────┘
                ↓
        ┌──────────────┐
        │ Result Queue │
        └──────┬───────┘
               ↓
        Streaming Output

## Quick Start

python -m main.py

## Running Tests

```bash
python -m pytest
```
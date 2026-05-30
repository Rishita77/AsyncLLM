# AsyncLLM Platform

Production-style async LLM batch processing and evaluation platform built with Python, FastAPI, asyncio, Redis, and Docker.

This project is designed as a learning-to-production bridge: simple enough to understand end-to-end, but structured like an internal AI platform service.

## What This Project Demonstrates

- Advanced async Python with `asyncio.TaskGroup` and `asyncio.Semaphore`
- Resilience patterns: timeout handling + exponential retry with jitter
- Provider abstraction for clean separation of API integration logic
- Queue-driven worker architecture (Redis-backed)
- API-first design with typed request/response models (Pydantic v2)
- Throughput/latency/memory/concurrency benchmark scripts
- Dockerized local stack and CI pipeline foundations

## Tech Stack

- Python 3.12+
- FastAPI
- httpx
- Pydantic v2 + pydantic-settings
- Redis
- PostgreSQL
- Docker + Docker Compose
- GitHub Actions

## Architecture

```text
Client
    |
    | POST /batch
    v
FastAPI API Layer
    |
    | Dependency Injection
    v
Batch Execution Engine
    |-- Concurrency control (Semaphore)
    |-- Retry (Exponential backoff + jitter)
    |-- Timeout wrapper
    v
Provider Adapter (OpenAI)

Background path:
Redis Queue <-> Worker Runtime -> Batch Execution Engine -> Provider
```

## Repository Map

- `app/main.py`: FastAPI application entrypoint
- `app/api/routes/batch.py`: `POST /batch` endpoint
- `app/api/dependencies.py`: dependency injection wiring
- `app/services/batch_engine.py`: core async batch execution logic
- `app/providers/base.py`: provider interface
- `app/providers/openai_provider.py`: OpenAI adapter
- `app/core/settings.py`: typed environment configuration
- `app/core/retry.py`: retry policy
- `app/core/timeout.py`: timeout wrapper
- `app/worker/main.py`: worker process entrypoint
- `app/worker/runner.py`: worker runtime loop
- `app/infra/redis_queue.py`: Redis queue adapter
- `tests/`: unit + async integration tests
- `benchmarks/`: performance and profiling scripts

## Quick Start (Local)

1. Create environment file:

```bash
cp .env.example .env
```

2. Set `OPENAI_API_KEY` in `.env`.

3. Install dependencies:

```bash
make install
```

4. Start API locally:

```bash
make dev
```

5. Open docs:

```text
http://localhost:8000/docs
```

## Docker Compose Stack

Start full stack (API + Worker + Redis + Postgres):

```bash
docker compose up --build
```

Stop stack:

```bash
docker compose down
```

## API Example

Request:

```bash
curl -X POST http://localhost:8000/batch \
    -H "Content-Type: application/json" \
    -d '{"prompts": ["Explain asyncio", "Explain Docker"], "concurrency": 5}'
```

Response shape:

```json
{
    "batch_id": "...",
    "metrics": {
        "total": 2,
        "succeeded": 2,
        "failed": 0,
        "timeout": 0,
        "cancelled": 0,
        "avg_latency_ms": 123.4,
        "p95_latency_ms": 140.1
    },
    "results": [
        {
            "request_id": "...",
            "prompt": "Explain asyncio",
            "status": "success",
            "output_text": "...",
            "error": null,
            "latency_ms": 120.8,
            "prompt_tokens": 15,
            "completion_tokens": 42,
            "total_tokens": 57,
            "estimated_cost_usd": 0.00003,
            "attempts": 1
        }
    ]
}
```

## Testing

Run all tests:

```bash
make test
```

Current test coverage includes:

- batch engine behavior with fake provider
- async API integration for `POST /batch`

## Benchmarks

Throughput:

```bash
python -m benchmarks.throughput --batch-size 300 --concurrency 20 --latency-ms 120
```

Latency percentiles:

```bash
python -m benchmarks.latency --batch-size 300 --concurrency 20 --latency-ms 120
```

Concurrency scaling:

```bash
python -m benchmarks.concurrency_scaling --batch-size 300 --concurrency-values 1,2,5,10,20,40
```

Memory usage:

```bash
python -m benchmarks.memory --batch-size 300 --concurrency 20 --latency-ms 120
```

## CI/CD

GitHub Actions workflow in `.github/workflows/ci.yml` runs:

- lint (ruff)
- type-check (mypy)
- tests (pytest)
- Docker image build
- Trivy image security scan

## Tradeoffs and Design Decisions

- Simplicity over full enterprise complexity:
    - worker queue uses Redis list operations (easy to reason about)
    - no distributed tracing stack yet
- Strong typing over dynamic shortcuts:
    - all API and domain payloads are typed
- Engine-first architecture:
    - business logic stays in `batch_engine`, not inside routes

## Scaling Discussion

Current scaling model:

- vertical: increase API/worker concurrency with semaphore limits
- horizontal: run multiple worker containers behind Redis queue

Potential bottlenecks to monitor:

- provider API rate limits
- queue depth growth under burst load
- DB write throughput once persistence is fully integrated

## Future Work

- Persist worker outcomes to Postgres for historical analytics
- Add idempotency keys for safe request retries
- Add dead-letter reprocessing policy and retry counters per job
- Add provider fallback routing and circuit breaker
- Add benchmark result export to CSV for graphing in CI

## Notes for Interview/Resume Framing

Describe this as:

"Built an async LLM batch platform with FastAPI and queue-based worker execution, implementing bounded concurrency, resilient retry/timeout handling, and containerized CI-tested deployment workflows."

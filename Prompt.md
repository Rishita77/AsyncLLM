You are a senior distributed systems engineer and Python platform architect.

Build a production-grade async LLM batch processing and evaluation platform.

The goal is to demonstrate:
- advanced Python
- asyncio
- distributed systems
- profiling
- Docker
- observability
- CI/CD
- performance engineering
- resilience engineering

This project must be resume-worthy and structured like a real infrastructure platform used internally at an AI company.

==================================================
HIGH LEVEL REQUIREMENTS
==================================================

Build a system that:
- accepts batches of prompts
- asynchronously sends them to LLM providers
- supports high concurrency
- handles retries/timeouts/rate limits
- tracks metrics
- benchmarks throughput/latency
- supports queue-based distributed workers
- is fully Dockerized
- includes observability and profiling

==================================================
TECH STACK
==================================================

Backend:
- Python 3.12+
- FastAPI
- asyncio
- httpx
- pydantic v2

Infrastructure:
- Redis
- PostgreSQL
- Docker
- Docker Compose

Observability:
- Prometheus
- Grafana
- OpenTelemetry

Performance:
- uvloop
- orjson
- msgspec

Tooling:
- pytest
- ruff
- mypy
- pre-commit
- GitHub Actions

==================================================
ARCHITECTURE REQUIREMENTS
==================================================

Create this structure:

app/
  api/
  core/
  providers/
  workers/
  schemas/
  services/
  observability/
  profiling/
  tests/

Requirements:
- clean architecture
- typed code everywhere
- dependency injection where appropriate
- proper async patterns
- bounded concurrency
- structured logging
- separation of concerns
- production-ready configs

==================================================
PHASE 1 REQUIREMENTS
==================================================

Implement:
1. FastAPI service
2. /batch endpoint
3. OpenAI provider abstraction
4. async batch execution engine
5. bounded concurrency using asyncio.Semaphore
6. retries with exponential backoff
7. timeout handling
8. metrics collection
9. typed request/response models
10. structured logging

Create:
- Dockerfile
- docker-compose.yml
- .env.example
- Makefile
- README.md

==================================================
BATCH EXECUTION ENGINE
==================================================

Core function:

async def batch_execute(prompts: list[str]) -> list[BatchResult]

Requirements:
- fully async
- configurable concurrency
- retry transient failures
- collect:
    latency
    tokens
    estimated cost
    status
- support cancellation safely
- no blocking I/O

==================================================
OBSERVABILITY
==================================================

Implement:
- Prometheus metrics
- request latency histograms
- throughput counters
- retry counters
- queue depth gauges
- OpenTelemetry tracing

==================================================
PROFILING
==================================================

Create benchmark scripts for:
- throughput
- latency
- memory usage
- concurrency scaling

Include:
- py-spy integration
- Scalene configs
- memory profiling scripts

==================================================
DOCKER REQUIREMENTS
==================================================

Use:
- multi-stage builds
- slim images
- proper layer caching
- non-root user
- healthchecks

Compose stack:
- API
- Redis
- Postgres
- Prometheus
- Grafana
- worker service

==================================================
TESTING REQUIREMENTS
==================================================

Implement:
- unit tests
- async integration tests
- provider mocks
- load tests

Use pytest-asyncio.

==================================================
CI/CD REQUIREMENTS
==================================================

GitHub Actions pipeline:
- lint
- type-check
- tests
- Docker build
- security scan

==================================================
README REQUIREMENTS
==================================================

Write a professional README including:
- architecture diagram
- setup instructions
- benchmark results
- concurrency graphs
- profiling screenshots
- scaling discussion
- tradeoffs
- future work

==================================================
ENGINEERING REQUIREMENTS
==================================================

Code should demonstrate:
- senior-level Python
- advanced asyncio usage
- proper error handling
- production-grade resiliency
- maintainability
- performance optimization

Avoid:
- toy architecture
- monolithic files
- blocking calls
- untyped code
- simplistic examples

==================================================
IMPLEMENTATION STRATEGY
==================================================

Proceed incrementally:
1. scaffold project
2. implement core async engine
3. add API
4. add provider layer
5. add Docker
6. add observability
7. add profiling
8. add tests
9. add CI/CD

At each phase:
- explain architectural decisions
- explain tradeoffs
- explain performance considerations

Generate complete working code.
Do not leave placeholders.

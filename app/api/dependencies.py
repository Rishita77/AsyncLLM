from collections.abc import AsyncIterator

from app.core.settings import Settings, get_settings
from app.providers.openai_provider import OpenAIProvider
from app.services.batch_processor import BatchExecutionEngine

def get_batch_execution_engine(settings: Settings) -> BatchExecutionEngine:
    provider = OpenAIProvider(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        timeout_seconds=settings.request_timeout_seconds,
    )
    return BatchExecutionEngine(provider=provider, settings=settings)

async def dependency_bundle() -> AsyncIterator[tuple[Settings, BatchExecutionEngine]]:
    settings = get_settings()
    engine = get_batch_execution_engine(settings)
    try:
        yield settings, engine
    finally:
        await engine.provider.aclose()
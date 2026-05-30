import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import dependency_bundle
from app.main import app
from app.providers.base import ProviderUsage, ProviderResult


class FakeProvider:
    async def execute(self, prompt: str) -> ProviderResult:
        return ProviderResult(
            output=f"ok: {prompt}", 
            usage=ProviderUsage(prompt_tokens=3, completion_tokens=4),
        )
        
    async def aclose(self) -> None:
        return None
    
    
@pytest.mark.asyncio
async def test_batch_endpoint_returns_typed_payload() -> None:
    # Override the provider dependency with our fake provider
    from app.core.settings import Settings
    from app.services.batch_processor import BatchExecutionEngine
    
    async def fake_dependency_bundle():
        settings = Settings(
            OPENAI_API_KEY="test_key"
        )
        engine = BatchExecutionEngine(provider=FakeProvider(), settings=settings)
        yield settings, engine
        
    app.dependency_overrides[dependency_bundle] = fake_dependency_bundle
    
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/batch", json={"prompts": ["test1", "test2"], "concurrency": 2})

    finally:
        app.dependency_overrides.clear()
    
      
    assert response.status_code == 200
    data = response.json()
    assert "batch_id" in data
    assert len(data["results"]) == 2
    assert data["metrics"]["total_requests"] == 2
    assert all(item["status"] == "success" for item in data["results"])
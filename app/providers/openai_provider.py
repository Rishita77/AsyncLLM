import httpx

from app.core.errors import ProviderConnectionError, ProviderRateLimitError
from app.providers.base import LLMProvider, ProviderResult, ProviderUsage


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, timeout_seconds: float):
        self._model = model
        self._client = httpx.AsyncClient(
            base_url="https://api.openai.com/v1",
            timeout=httpx.Timeout(timeout_seconds),
            headers={"Authorization": f"Bearer {api_key}"},
        )
        
    async def generate(self, prompt: str) -> ProviderResult:
            payload = {
                "model": self._model,
                "input": prompt,
            }
            response = await self._client.post("/responses", json=payload)
            
            if response.status_code == 429:
                raise ProviderRateLimitError("OpenAI API rate limit exceeded")
            if response.status_code >= 500:
                raise ProviderConnectionError(f"OpenAI API server error: {response.status_code}")
            
            response.raise_for_status()
            data = response.json()
            
            output_text = data.get("output") or ""
            usage_data = data.get("usage", {})
            usage = ProviderUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
            )
            return ProviderResult(output_text=output_text, usage=usage)
        
    async def aclose(self) -> None:
        await self._client.aclose()
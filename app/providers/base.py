from dataclasses import dataclass
from typing import Protocol

@dataclass(slots=True)
class ProviderUsage:
    prompt_tokens: int
    completion_tokens: int
    
    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens
    
@dataclass(slots=True)
class ProviderResult:
    output_text: str
    usage: ProviderUsage
    
class LLMProvider(Protocol):
    """Protocol for LLM providers"""
    
    async def generate(self, prompt: str) -> ProviderResult:
        ...
        
    async def aclose(self) -> None:
        ...
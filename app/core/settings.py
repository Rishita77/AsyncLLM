from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environemnt variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore",
    )
    
    app_name: str = "Async LLM Platform"
    environment: str = "dev"
    log_level: str = "INFO"
    
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = "gpt-4o-mini"
    
    max_concurrency: int = 5
    request_timeout_seconds: float = 20.0
    max_retries: int = 3
    retry_backoff_seconds: float = 0.5
    
    
    redis_url: str = "redis://localhost:6379/0"
    postgres_dsn: str = "postgresql://postgres:postgres@localhost:5432/async_llm"
    
    estimated_input_token_multiplier: float = 1.4
    estimated_output_tokens: int = 300
    input_token_usd_per_1m: float = 0.15
    output_token_usd_per_1m: float = 0.6 
    
    
@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()

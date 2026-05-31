from enum import Enum

from pydantic import BaseModel, Field


class BatchItemStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    
class BatchResult(BaseModel):
    request_id: str
    prompt: str
    status: BatchItemStatus
    output_text: str | None = None
    error: str | None = None
    latency_ms: float = Field(ge=0)
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)
    cost_usd: float = Field(ge=0)
    attempts: int = Field(ge=1)
    
class BatchMetrics(BaseModel):
    total_requests: int = Field(ge=0)
    successful_requests: int = Field(ge=0)
    failed_requests: int = Field(ge=0)
    timed_out_requests: int = Field(ge=0)
    cancelled_requests: int = Field(ge=0)
    average_latency_ms: float = Field(ge=0)
    p95_latency_ms: float = Field(ge=0)
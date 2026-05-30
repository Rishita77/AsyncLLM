from pydantic import BaseModel, Field

from app.models.domain import BatchResult, BatchMetrics


class BatchResponse(BaseModel):
    batch_id: str
    results: list[BatchResult]
    metrics: BatchMetrics
    
class BatchRequest(BaseModel):
    prompts: list[str] = Field(min_items=1, max_items=20)
    concurrency: int | None = Field(default=None, ge=1, le=4)
    
class HealthResponse(BaseModel):
    status: str 
    service: str
    
class ErrorResponse(BaseModel):
    error: str
    
    
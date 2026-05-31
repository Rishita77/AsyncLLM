import uuid

from fastapi import APIRouter, Depends

from app.api.dependencies import dependency_bundle
from app.core.settings import Settings
from app.services.batch_processor import BatchExecutionEngine, compute_batch_metrics
from app.models.api import BatchRequest, BatchResponse

router = APIRouter(tags=["batch"])

@router.post("/batch", response_model=BatchResponse)
async def submit_batch(
    payload: BatchRequest,
    dependencies: tuple[Settings, BatchExecutionEngine] = Depends(dependency_bundle),
) -> BatchResponse:
    settings, engine = dependencies
    batch_id = str(uuid.uuid4())
    
    batch_results = await engine.batch_execute(
        payload.prompts, 
        concurrency=payload.concurrency,
    )
    metrics = compute_batch_metrics(batch_results)
    
    return BatchResponse(
        batch_id=batch_id,
        results=batch_results,
        metrics=metrics,
    )
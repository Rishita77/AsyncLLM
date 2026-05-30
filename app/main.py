from fastapi import FastAPI

from app.core.settings import get_settings
from app.api.routes.batch import router as batch_router
from app.models.api import HealthResponse


settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(batch_router)

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)
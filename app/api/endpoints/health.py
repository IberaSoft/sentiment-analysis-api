"""Health check endpoints."""
import time
from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.core.model import sentiment_model
from app.schemas.response import HealthResponse, ModelInfoResponse
from app.utils.metrics import api_requests_total

router = APIRouter()

# Track startup time
startup_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    uptime = time.time() - startup_time
    model_loaded = sentiment_model is not None
    
    api_requests_total.labels(endpoint="/health", method="GET", status="200").inc()
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        uptime_seconds=uptime
    )


@router.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    """Get model information."""
    from app.config import settings
    
    api_requests_total.labels(endpoint="/model/info", method="GET", status="200").inc()
    
    return ModelInfoResponse(
        model_name="customer-sentiment-analyzer",
        version="1.0.0",
        base_model="distilbert-base-uncased",
        classes=["positive", "negative", "neutral"],
        accuracy=0.902,
        f1_score=0.89
    )


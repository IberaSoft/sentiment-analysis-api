"""Prediction endpoints."""
import time

from fastapi import APIRouter, HTTPException, Request

from app.core.cache import prediction_cache
from app.core.model import get_model
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse
from app.utils.logger import logger
from app.utils.metrics import (
    api_errors_total,
    api_requests_total,
    inference_duration_seconds,
    sentiment_predictions_total,
)

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_sentiment(request: PredictionRequest, http_request: Request):
    """Predict sentiment for a single text."""
    start_time = time.time()

    try:
        # Check cache first
        cached_result = prediction_cache.get(request.text)
        if cached_result:
            logger.info("Cache hit", extra={"text_preview": request.text[:50]})
            api_requests_total.labels(endpoint="/predict", method="POST", status="200").inc()
            return PredictionResponse(**cached_result)

        # Get model and predict
        model = get_model()
        result = model.predict(request.text)

        # Cache result
        prediction_cache.set(request.text, result)

        # Update metrics
        sentiment_predictions_total.labels(sentiment=result["sentiment"]).inc()
        inference_duration_seconds.observe(result["processing_time_ms"] / 1000)
        api_requests_total.labels(endpoint="/predict", method="POST", status="200").inc()

        # Log prediction
        logger.info(
            "Prediction made",
            extra={
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "processing_time_ms": result["processing_time_ms"],
            },
        )

        return PredictionResponse(**result)

    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}", exc_info=True)
        api_errors_total.labels(endpoint="/predict", error_type=type(e).__name__).inc()
        api_requests_total.labels(endpoint="/predict", method="POST", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

"""Batch prediction endpoints."""
import time

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.core.model import get_model
from app.schemas.request import BatchPredictionRequest
from app.schemas.response import BatchPredictionItem, BatchPredictionResponse
from app.utils.logger import logger
from app.utils.metrics import (api_errors_total, api_requests_total,
                               inference_duration_seconds,
                               sentiment_predictions_total)

router = APIRouter()


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(batch_request: BatchPredictionRequest):
    """Predict sentiment for multiple texts."""
    start_time = time.time()

    try:
        # Validate batch size
        if len(batch_request.texts) > 100:
            raise HTTPException(
                status_code=400, detail="Maximum batch size is 100 texts"
            )

        # Get model and predict
        model = get_model()
        predictions, processing_time = model.predict_batch(batch_request.texts)

        # Calculate average confidence
        total_confidence = sum(p["confidence"] for p in predictions)
        avg_confidence = total_confidence / len(predictions) if predictions else 0.0

        # Update metrics
        for pred in predictions:
            sentiment_predictions_total.labels(sentiment=pred["sentiment"]).inc()

        inference_duration_seconds.observe(processing_time / 1000)
        api_requests_total.labels(
            endpoint="/predict/batch", method="POST", status="200"
        ).inc()

        # Log batch prediction
        logger.info(
            "Batch prediction made",
            extra={
                "total_processed": len(predictions),
                "processing_time_ms": processing_time,
            },
        )

        return BatchPredictionResponse(
            predictions=[BatchPredictionItem(**p) for p in predictions],
            total_processed=len(predictions),
            avg_confidence=avg_confidence,
            processing_time_ms=processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch prediction: {str(e)}", exc_info=True)
        api_errors_total.labels(
            endpoint="/predict/batch", error_type=type(e).__name__
        ).inc()
        api_requests_total.labels(
            endpoint="/predict/batch", method="POST", status="500"
        ).inc()
        raise HTTPException(
            status_code=500, detail=f"Batch prediction failed: {str(e)}"
        )

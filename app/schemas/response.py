"""Response schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class SentimentScores(BaseModel):
    """Sentiment scores for each class."""

    positive: float = Field(..., ge=0.0, le=1.0)
    negative: float = Field(..., ge=0.0, le=1.0)
    neutral: float = Field(..., ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    """Single prediction response."""

    sentiment: str = Field(..., description="Predicted sentiment (positive, negative, neutral)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    scores: SentimentScores = Field(..., description="Scores for each sentiment class")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class BatchPredictionItem(BaseModel):
    """Single item in batch prediction."""

    text: str
    sentiment: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""

    predictions: list[BatchPredictionItem] = Field(..., description="List of predictions")
    total_processed: int = Field(..., ge=0)
    avg_confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class ModelInfoResponse(BaseModel):
    """Model information response."""

    model_name: str
    version: str
    base_model: str
    classes: list[str]
    accuracy: float = Field(..., ge=0.0, le=1.0)
    f1_score: float = Field(..., ge=0.0, le=1.0)


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool
    uptime_seconds: float

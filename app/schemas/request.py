"""Request schemas."""
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Single prediction request."""
    text: str = Field(..., description="Text to analyze", min_length=1, max_length=5000)


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    texts: list[str] = Field(..., description="List of texts to analyze", min_items=1, max_items=100)


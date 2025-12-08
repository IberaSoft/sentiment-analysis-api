"""Application configuration."""
import os
from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Model Configuration
    model_name: str = os.getenv("MODEL_NAME", "IberaSoft/customer-sentiment-analyzer")

    # API Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_batch_size: int = int(os.getenv("MAX_BATCH_SIZE", "32"))
    cache_size: int = int(os.getenv("CACHE_SIZE", "1000"))
    workers: int = int(os.getenv("WORKERS", "2"))

    # Device Configuration
    device: Optional[str] = os.getenv("DEVICE", None)
    device_id: Optional[int] = (
        int(os.getenv("DEVICE_ID", "0")) if os.getenv("DEVICE_ID") else None
    )

    # HuggingFace Token (for private models)
    hf_token: Optional[str] = os.getenv("HF_TOKEN", None)

    # API Info
    api_version: str = "v1"
    api_title: str = "Customer Sentiment Analysis API"
    api_description: str = (
        "Production-ready sentiment analysis API powered by fine-tuned DistilBERT"
    )

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()

"""Text preprocessing utilities."""
import re
from typing import Optional


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def preprocess_text(text: str) -> str:
    """Preprocess text for sentiment analysis."""
    if not text:
        return ""

    # Clean text
    text = clean_text(text)

    # Convert to lowercase for consistency
    # Note: DistilBERT tokenizer handles this, but we do it for consistency
    text = text.lower()

    return text

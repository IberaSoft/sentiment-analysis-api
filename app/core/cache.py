"""Response caching utilities."""
import hashlib
from functools import lru_cache
from typing import Optional, Tuple

from app.config import settings


class PredictionCache:
    """LRU cache for predictions."""

    def __init__(self, maxsize: int = None):
        """Initialize cache."""
        self.maxsize = maxsize or settings.cache_size
        self._cache = {}
        self._access_order = []

    def _hash_key(self, text: str) -> str:
        """Generate hash key for text."""
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text: str) -> Optional[dict]:
        """Get cached prediction."""
        key = self._hash_key(text)
        if key in self._cache:
            # Move to end (most recently used)
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None

    def set(self, text: str, prediction: dict) -> None:
        """Cache prediction."""
        key = self._hash_key(text)

        # Remove oldest if cache is full
        if len(self._cache) >= self.maxsize and key not in self._cache:
            oldest_key = self._access_order.pop(0)
            del self._cache[oldest_key]

        # Add/update entry
        self._cache[key] = prediction
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

    def clear(self) -> None:
        """Clear cache."""
        self._cache.clear()
        self._access_order.clear()

    def size(self) -> int:
        """Get cache size."""
        return len(self._cache)


# Global cache instance
prediction_cache = PredictionCache()

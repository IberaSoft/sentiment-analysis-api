"""Prometheus metrics."""
from prometheus_client import Counter, Histogram, Gauge

# Prediction metrics
sentiment_predictions_total = Counter(
    "sentiment_predictions_total",
    "Total predictions by sentiment",
    ["sentiment"]
)

inference_duration_seconds = Histogram(
    "inference_duration_seconds",
    "Inference latency in seconds",
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

api_requests_total = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint", "method", "status"]
)

api_errors_total = Counter(
    "api_errors_total",
    "Total API errors",
    ["endpoint", "error_type"]
)

model_loaded = Gauge(
    "model_loaded",
    "Whether the model is loaded (1) or not (0)"
)


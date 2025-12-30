# API Reference

**Base URL**: `http://localhost:8000/api/v1`

**Interactive Docs**: Visit `/docs` for Swagger UI

**Authentication**: None (add API keys for production)

## Endpoints

### POST /predict

Analyze sentiment for a single text.

**Request:**
```json
{"text": "Great product, highly recommend!"}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.94,
  "scores": {"positive": 0.94, "negative": 0.03, "neutral": 0.03},
  "processing_time_ms": 35
}
```

### POST /predict/batch

Analyze multiple texts (max 100 per request).

**Request:**
```json
{
  "texts": ["Excellent service!", "Terrible experience.", "It's okay"]
}
```

**Response:**
```json
{
  "predictions": [
    {"text": "Excellent service!", "sentiment": "positive", "confidence": 0.96},
    {"text": "Terrible experience.", "sentiment": "negative", "confidence": 0.91},
    {"text": "It's okay", "sentiment": "neutral", "confidence": 0.78}
  ],
  "total_processed": 3,
  "avg_confidence": 0.88,
  "processing_time_ms": 87
}
```

### GET /model/info

Model information and metrics.

**Response:**
```json
{
  "model_name": "customer-sentiment-analyzer",
  "version": "1.0.0",
  "base_model": "distilbert-base-uncased",
  "classes": ["positive", "negative", "neutral"],
  "accuracy": 0.902
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{"status": "healthy", "model_loaded": true, "uptime_seconds": 3600}
```

## Error Format

```json
{"detail": "Error message"}
```

## Usage Examples

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={"text": "This product is amazing!"}
)
print(response.json())
```

### JavaScript

```javascript
fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'This product is amazing!'})
})
.then(res => res.json())
.then(data => console.log(data));
```


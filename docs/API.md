# API Documentation

## Overview

The Customer Sentiment Analysis API provides REST endpoints for analyzing sentiment in customer reviews using a fine-tuned DistilBERT model.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required. For production deployments, consider adding API keys or OAuth2.

## Endpoints

### 1. Single Prediction

**Endpoint:** `POST /predict`

**Description:** Analyze sentiment for a single text.

**Request Body:**
```json
{
  "text": "Great product, highly recommend!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.94,
  "scores": {
    "positive": 0.94,
    "negative": 0.03,
    "neutral": 0.03
  },
  "processing_time_ms": 35
}
```

**Status Codes:**
- `200 OK`: Successful prediction
- `400 Bad Request`: Invalid request body
- `500 Internal Server Error`: Server error

### 2. Batch Prediction

**Endpoint:** `POST /predict/batch`

**Description:** Analyze sentiment for multiple texts in a single request.

**Request Body:**
```json
{
  "texts": [
    "Excellent service!",
    "Terrible experience.",
    "It's okay, nothing special."
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "text": "Excellent service!",
      "sentiment": "positive",
      "confidence": 0.96
    },
    {
      "text": "Terrible experience.",
      "sentiment": "negative",
      "confidence": 0.91
    },
    {
      "text": "It's okay, nothing special.",
      "sentiment": "neutral",
      "confidence": 0.78
    }
  ],
  "total_processed": 3,
  "avg_confidence": 0.88,
  "processing_time_ms": 87
}
```

**Status Codes:**
- `200 OK`: Successful batch prediction
- `400 Bad Request`: Invalid request body or batch size exceeded
- `500 Internal Server Error`: Server error

**Limits:**
- Maximum batch size: 100 texts per request

### 3. Model Information

**Endpoint:** `GET /model/info`

**Description:** Get information about the loaded model.

**Response:**
```json
{
  "model_name": "customer-sentiment-analyzer",
  "version": "1.0.0",
  "base_model": "distilbert-base-uncased",
  "classes": ["positive", "negative", "neutral"],
  "accuracy": 0.902,
  "f1_score": 0.89
}
```

### 4. Health Check

**Endpoint:** `GET /health`

**Description:** Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime_seconds": 3600
}
```

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider adding rate limiting based on your requirements.

## Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI with interactive API testing.

## Examples

### cURL

```bash
# Single prediction
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# Batch prediction
curl -X POST "http://localhost:8000/api/v1/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great!", "Bad!", "Okay"]}'
```

### Python

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={"text": "This product is amazing!"}
)
print(response.json())

# Batch prediction
response = requests.post(
    "http://localhost:8000/api/v1/predict/batch",
    json={"texts": ["Great!", "Bad!", "Okay"]}
)
print(response.json())
```

### JavaScript

```javascript
// Single prediction
fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'This product is amazing!' })
})
.then(res => res.json())
.then(data => console.log(data));
```


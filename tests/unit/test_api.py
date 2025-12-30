"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_model():
    """Mock sentiment model."""
    with patch('app.core.model.get_model') as mock_get_model:
        mock_model_instance = Mock()
        mock_model_instance.predict.return_value = {
            "sentiment": "positive",
            "confidence": 0.95,
            "scores": {"positive": 0.95, "negative": 0.03, "neutral": 0.02},
            "processing_time_ms": 35.0
        }
        mock_model_instance.predict_batch.return_value = (
            [
                {"text": "Great!", "sentiment": "positive", "confidence": 0.95},
                {"text": "Bad!", "sentiment": "negative", "confidence": 0.90}
            ],
            50.0
        )
        mock_get_model.return_value = mock_model_instance
        yield mock_model_instance


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """Test health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "uptime_seconds" in data


def test_model_info_endpoint(client):
    """Test model info endpoint."""
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data
    assert "classes" in data


def test_predict_endpoint(client):
    """Test predict endpoint."""
    # Mock the model
    mock_model_instance = Mock()
    mock_model_instance.predict.return_value = {
        "sentiment": "positive",
        "confidence": 0.95,
        "scores": {"positive": 0.95, "negative": 0.03, "neutral": 0.02},
        "processing_time_ms": 35.0
    }
    
    with patch('app.api.endpoints.predict.get_model', return_value=mock_model_instance), \
         patch('app.api.endpoints.predict.prediction_cache') as mock_cache:
        mock_cache.get.return_value = None  # No cache hit
        response = client.post(
            "/api/v1/predict",
            json={"text": "This is great!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "positive"
        assert data["confidence"] == 0.95


def test_batch_predict_endpoint(client):
    """Test batch predict endpoint."""
    mock_model_instance = Mock()
    mock_model_instance.predict_batch.return_value = (
        [
            {"text": "Great!", "sentiment": "positive", "confidence": 0.95},
            {"text": "Bad!", "sentiment": "negative", "confidence": 0.90}
        ],
        50.0
    )
    
    with patch('app.api.endpoints.batch.get_model', return_value=mock_model_instance):
        response = client.post(
            "/api/v1/predict/batch",
            json={"texts": ["Great!", "Bad!"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["predictions"]) == 2
        assert data["total_processed"] == 2


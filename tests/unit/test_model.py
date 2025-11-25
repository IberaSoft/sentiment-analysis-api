"""Tests for model module."""
import pytest
from unittest.mock import Mock, patch

from app.core.model import SentimentModel, get_model


@patch('app.core.model.AutoTokenizer')
@patch('app.core.model.AutoModelForSequenceClassification')
@patch('app.core.model.pipeline')
def test_model_initialization(mock_pipeline, mock_model_class, mock_tokenizer_class):
    """Test model initialization."""
    # Mock the pipeline return value
    mock_classifier = Mock()
    mock_classifier.return_value = [[
        {"label": "POSITIVE", "score": 0.9},
        {"label": "NEGATIVE", "score": 0.05},
        {"label": "NEUTRAL", "score": 0.05}
    ]]
    mock_pipeline.return_value = mock_classifier
    
    # Mock tokenizer and model
    mock_tokenizer = Mock()
    mock_model = Mock()
    mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
    mock_model_class.from_pretrained.return_value = mock_model
    
    # Initialize model
    model = SentimentModel()
    
    assert model.model is not None
    assert model.tokenizer is not None
    assert model.classifier is not None


@patch('app.core.model.AutoTokenizer')
@patch('app.core.model.AutoModelForSequenceClassification')
@patch('app.core.model.pipeline')
def test_model_predict(mock_pipeline, mock_model_class, mock_tokenizer_class):
    """Test model prediction."""
    # Mock pipeline
    mock_classifier = Mock()
    mock_classifier.return_value = [[
        {"label": "POSITIVE", "score": 0.9},
        {"label": "NEGATIVE", "score": 0.05},
        {"label": "NEUTRAL", "score": 0.05}
    ]]
    mock_pipeline.return_value = mock_classifier
    
    # Mock tokenizer and model
    mock_tokenizer = Mock()
    mock_model = Mock()
    mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
    mock_model_class.from_pretrained.return_value = mock_model
    
    # Initialize and predict
    model = SentimentModel()
    result = model.predict("This is great!")
    
    assert "sentiment" in result
    assert "confidence" in result
    assert "scores" in result
    assert "processing_time_ms" in result
    assert result["sentiment"] in ["positive", "negative", "neutral"]


def test_model_predict_empty_text():
    """Test prediction with empty text."""
    with patch('app.core.model.AutoTokenizer'), \
         patch('app.core.model.AutoModelForSequenceClassification'), \
         patch('app.core.model.pipeline'):
        model = SentimentModel()
        result = model.predict("")
        
        assert result["sentiment"] == "neutral"
        assert result["confidence"] == 0.5


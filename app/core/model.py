"""Model loading and inference."""
import time
from typing import Any, Dict, List, Optional, Tuple

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

from app.config import settings
from app.core.preprocessing import preprocess_text
from app.utils.logger import logger
from app.utils.metrics import model_loaded


class SentimentModel:
    """Sentiment analysis model wrapper."""
    
    def __init__(self):
        """Initialize model."""
        self.model = None
        self.tokenizer = None
        self.classifier = None
        self.device = self._get_device()
        self.classes = ["negative", "neutral", "positive"]
        self.label_map = {0: "negative", 1: "neutral", 2: "positive"}
        self._load_model()
    
    def _get_device(self) -> str:
        """Get device for model inference."""
        if settings.device:
            return settings.device
        
        if torch.cuda.is_available():
            device_id = settings.device_id or 0
            return f"cuda:{device_id}"
        
        return "cpu"
    
    def _load_model(self) -> None:
        """Load model from HuggingFace."""
        try:
            logger.info(f"Loading model: {settings.model_name}")
            logger.info(f"Using device: {self.device}")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(
                settings.model_name,
                token=settings.hf_token
            )
            
            model = AutoModelForSequenceClassification.from_pretrained(
                settings.model_name,
                token=settings.hf_token
            )
            
            # Move model to device
            model.to(self.device)
            model.eval()
            
            # Create pipeline
            self.classifier = pipeline(
                "sentiment-analysis",
                model=model,
                tokenizer=tokenizer,
                device=0 if "cuda" in self.device else -1,
                return_all_scores=True
            )
            
            self.model = model
            self.tokenizer = tokenizer
            
            model_loaded.set(1)
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)
            model_loaded.set(0)
            raise
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Predict sentiment for a single text."""
        start_time = time.time()
        
        # Preprocess
        processed_text = preprocess_text(text)
        
        if not processed_text:
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "scores": {"positive": 0.33, "negative": 0.33, "neutral": 0.34}
            }
        
        # Predict
        results = self.classifier(processed_text)
        
        # Process results
        scores = {}
        for result in results[0]:
            label = result["label"].lower()
            score = result["score"]
            scores[label] = score
        
        # Ensure all classes are present
        for cls in self.classes:
            if cls not in scores:
                scores[cls] = 0.0
        
        # Get predicted sentiment (highest score)
        predicted_label = max(scores.items(), key=lambda x: x[1])[0]
        confidence = scores[predicted_label]
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return {
            "sentiment": predicted_label,
            "confidence": confidence,
            "scores": scores,
            "processing_time_ms": processing_time
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        """Predict sentiment for multiple texts."""
        start_time = time.time()
        
        # Preprocess all texts
        processed_texts = [preprocess_text(text) for text in texts]
        
        # Filter out empty texts
        valid_texts = []
        valid_indices = []
        for i, text in enumerate(processed_texts):
            if text:
                valid_texts.append(text)
                valid_indices.append(i)
        
        if not valid_texts:
            # Return neutral predictions for all
            return [
                {
                    "text": text,
                    "sentiment": "neutral",
                    "confidence": 0.5
                }
                for text in texts
            ]
        
        # Predict in batches
        batch_size = settings.max_batch_size
        predictions = []
        
        for i in range(0, len(valid_texts), batch_size):
            batch = valid_texts[i:i + batch_size]
            batch_results = self.classifier(batch)
            
            for j, result in enumerate(batch_results):
                # Process results
                scores = {}
                for item in result:
                    label = item["label"].lower()
                    score = item["score"]
                    scores[label] = score
                
                # Ensure all classes are present
                for cls in self.classes:
                    if cls not in scores:
                        scores[cls] = 0.0
                
                # Get predicted sentiment
                predicted_label = max(scores.items(), key=lambda x: x[1])[0]
                confidence = scores[predicted_label]
                
                predictions.append({
                    "text": texts[valid_indices[i + j]],
                    "sentiment": predicted_label,
                    "confidence": confidence
                })
        
        # Fill in empty texts with neutral predictions
        result_predictions = []
        prediction_idx = 0
        for i, text in enumerate(texts):
            if i in valid_indices:
                result_predictions.append(predictions[prediction_idx])
                prediction_idx += 1
            else:
                result_predictions.append({
                    "text": text,
                    "sentiment": "neutral",
                    "confidence": 0.5
                })
        
        processing_time = (time.time() - start_time) * 1000
        
        return result_predictions, processing_time


# Global model instance
sentiment_model: Optional[SentimentModel] = None


def get_model() -> SentimentModel:
    """Get or initialize model instance."""
    global sentiment_model
    if sentiment_model is None:
        sentiment_model = SentimentModel()
    return sentiment_model


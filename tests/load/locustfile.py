"""Locust load testing configuration."""
from locust import HttpUser, task, between


class SentimentAPIUser(HttpUser):
    """Load test user for sentiment API."""
    wait_time = between(1, 3)
    
    @task(3)
    def predict_sentiment(self):
        """Test single prediction endpoint."""
        self.client.post(
            "/api/v1/predict",
            json={"text": "This is a great product! I love it."},
            headers={"Content-Type": "application/json"}
        )
    
    @task(1)
    def batch_predict(self):
        """Test batch prediction endpoint."""
        self.client.post(
            "/api/v1/predict/batch",
            json={
                "texts": [
                    "Excellent service!",
                    "Terrible experience.",
                    "It's okay, nothing special."
                ]
            },
            headers={"Content-Type": "application/json"}
        )
    
    @task(2)
    def health_check(self):
        """Test health endpoint."""
        self.client.get("/api/v1/health")
    
    @task(1)
    def model_info(self):
        """Test model info endpoint."""
        self.client.get("/api/v1/model/info")


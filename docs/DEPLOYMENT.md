# Deployment Guide

This guide covers various deployment options for the Sentiment Analysis API.

## Quick Start with Docker

### Build and Run

```bash
# Build image
docker build -t sentiment-api:latest .

# Run container
docker run -d \
  --name sentiment-api \
  -p 8000:8000 \
  -e MODEL_NAME=IberaSoft/customer-sentiment-analyzer \
  sentiment-api:latest
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your settings

# Run API
uvicorn app.main:app --reload --port 8000
```

## Production Deployment Options

### Option 1: HuggingFace Spaces

1. Fork this repository
2. Create a new Space on HuggingFace
3. Connect your GitHub repository
4. The Space will auto-deploy!

See the live demo: [HuggingFace Spaces](https://huggingface.co/spaces/IberaSoft/sentiment-analyzer-demo)

### Option 2: Cloud VPS (DigitalOcean, Linode, etc.)

#### Step 1: Setup Server

```bash
# On your server
sudo apt update
sudo apt install -y docker.io docker-compose git

# Clone repository
git clone https://github.com/IberaSoft/sentiment-analysis-api.git
cd sentiment-analysis-api
```

#### Step 2: Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env
nano .env
```

#### Step 3: Start Services

```bash
# Start with Docker Compose
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

#### Step 4: Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install -y nginx

# Create configuration
sudo nano /etc/nginx/sites-available/sentiment-api
```

Add configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/sentiment-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: Setup SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 3: AWS EC2

1. Launch EC2 instance (Ubuntu 22.04 LTS)
2. Follow VPS deployment steps above
3. Configure security groups to allow HTTP/HTTPS traffic
4. Optionally use Elastic IP for static IP address

### Option 4: AWS ECS/Fargate

1. Build and push Docker image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure Application Load Balancer
5. Set up auto-scaling

### Option 5: Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/sentiment-api

# Deploy
gcloud run deploy sentiment-api \
  --image gcr.io/PROJECT_ID/sentiment-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 6: Azure Container Instances

```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image sentiment-api:latest .

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name sentiment-api \
  --image myregistry.azurecr.io/sentiment-api:latest \
  --dns-name-label sentiment-api \
  --ports 8000
```

## Environment Variables

### Required

- `MODEL_NAME`: HuggingFace model identifier (default: `IberaSoft/customer-sentiment-analyzer`)

### Optional

- `LOG_LEVEL`: Logging level (default: `INFO`)
- `MAX_BATCH_SIZE`: Maximum batch size for predictions (default: `32`)
- `CACHE_SIZE`: LRU cache size (default: `1000`)
- `WORKERS`: Number of Uvicorn workers (default: `2`)
- `DEVICE`: Device for inference (`cpu` or `cuda`, default: auto-detect)
- `DEVICE_ID`: GPU device ID (default: `0`)
- `HF_TOKEN`: HuggingFace token for private models

## Monitoring

### Prometheus Metrics

Metrics are available at `http://localhost:8000/metrics`

Key metrics:
- `sentiment_predictions_total`: Total predictions by sentiment
- `inference_duration_seconds`: Inference latency
- `api_requests_total`: Total API requests
- `api_errors_total`: Total API errors
- `model_loaded`: Model loading status

### Logging

Logs are structured JSON for easy parsing. Configure log aggregation (e.g., ELK stack, CloudWatch, etc.)

## Scaling

### Horizontal Scaling

Run multiple instances behind a load balancer:

```bash
# Scale with Docker Compose
docker-compose up -d --scale api=3
```

### Vertical Scaling

- Increase `WORKERS` for more concurrent requests
- Use GPU for faster inference
- Increase `MAX_BATCH_SIZE` for better throughput

## Health Checks

The API provides a health check endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Use this for:
- Load balancer health checks
- Container orchestration (Kubernetes liveness/readiness probes)
- Monitoring systems

## Security Considerations

1. **API Authentication**: Add API keys or OAuth2 for production
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **HTTPS**: Always use HTTPS in production
4. **Secrets Management**: Use environment variables or secret management services
5. **Network Security**: Restrict access with firewalls/VPCs
6. **Input Validation**: Already handled by Pydantic schemas

## Backup and Recovery

- Model files are downloaded from HuggingFace on startup
- No persistent storage required for the model
- Consider backing up:
  - Configuration files
  - Logs
  - Metrics data

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.


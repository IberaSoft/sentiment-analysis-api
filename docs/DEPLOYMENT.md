# Deployment Guide

## Quick Start

### Docker (Recommended)

```bash
# Build and run
docker build -t sentiment-api:latest .
docker run -d --name sentiment-api -p 8000:8000 sentiment-api:latest

# Or use Docker Compose
docker-compose up -d
```

### Local Development

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

API available at: `http://localhost:8000/docs`

## Production Deployment

### HuggingFace Spaces

**Easiest option for demos:**

1. Fork this repository
2. Create a Space on HuggingFace
3. Connect your GitHub repo
4. Auto-deploys on push

See: [SPACES_GUIDE.md](SPACES_GUIDE.md)

### Cloud VPS (DigitalOcean, Linode, AWS EC2)

```bash
# Setup server
sudo apt update
sudo apt install -y docker.io docker-compose git

# Clone and start
git clone https://github.com/IberaSoft/sentiment-analysis-api.git
cd sentiment-analysis-api
cp .env.example .env
docker-compose up -d
```

### Nginx Reverse Proxy

```bash
sudo apt install -y nginx
```

Create `/etc/nginx/sites-available/sentiment-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/sentiment-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d your-domain.com  # SSL
```

### Cloud Platforms

**Google Cloud Run:**

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/sentiment-api
gcloud run deploy sentiment-api \
  --image gcr.io/PROJECT_ID/sentiment-api \
  --platform managed \
  --allow-unauthenticated
```

**AWS ECS/Fargate:** Push image to ECR, create task definition and service

**Azure Container Instances:** Use `az container create` with ACR image

## Environment Variables

Create `.env` file:

```bash
# Required
MODEL_NAME=IberaSoft/customer-sentiment-analyzer

# Optional
LOG_LEVEL=INFO
MAX_BATCH_SIZE=32
WORKERS=2
DEVICE=cpu  # or cuda
HF_TOKEN=your_token_here  # for private models
```

## Monitoring

**Metrics**: Available at `http://localhost:8000/metrics`

- `sentiment_predictions_total`
- `inference_duration_seconds`
- `api_requests_total`
- `api_errors_total`

**Logs**: Structured JSON format, compatible with ELK, CloudWatch, etc.

## Scaling

**Horizontal**: Run multiple instances with Docker Compose

```bash
docker-compose up -d --scale api=3
```

**Vertical**: Increase `WORKERS`, use GPU, or increase `MAX_BATCH_SIZE`

## Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Use for load balancers, Kubernetes probes, or monitoring.

## Security

- Add API authentication (API keys/OAuth2)
- Implement rate limiting
- Use HTTPS in production
- Secure environment variables
- Configure firewalls/VPCs

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.


# Troubleshooting

## Model Issues

### Model Not Found

**Error**: `Model not found` or `404 Client Error`

**Fix:**

```bash
# Verify model name in .env
MODEL_NAME=IberaSoft/customer-sentiment-analyzer

# For private models, add token
HF_TOKEN=your_token_here

# Test manually
python -c "from transformers import AutoModel; AutoModel.from_pretrained('IberaSoft/customer-sentiment-analyzer')"
```

### Model Loading Timeout

**Fix**: Check network speed or pre-download model:

```python
from transformers import AutoModel
AutoModel.from_pretrained(
    "IberaSoft/customer-sentiment-analyzer", 
    cache_dir="./models"
)
```

## Performance Issues

### Slow Inference

**Fix**: Enable GPU or optimize batch size:

```bash
# Use GPU
DEVICE=cuda DEVICE_ID=0

# Increase batch size
MAX_BATCH_SIZE=64

# Or use quantized model (see training/optimize.py)
```

### Out of Memory

**Fix**:

```bash
# Reduce batch size
MAX_BATCH_SIZE=16
```

Or increase Docker memory in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 4G
```

## API Issues

### 500 Internal Server Error

**Fix**: Check logs and health:

```bash
docker-compose logs -f api
curl http://localhost:8000/api/v1/health
```

### 422 Validation Error

**Fix**: Verify request format:

- Use `Content-Type: application/json` header
- Text max 5000 characters
- Batch requests max 100 items

### CORS Errors

**Fix**: CORS enabled by default. For production, restrict in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"]
)
```

## Docker Issues

### Container Won't Start

**Fix**: Check logs:

```bash
docker logs sentiment-api

# Check port availability
lsof -i :8000
```

### Image Build Fails

**Fix**: Clear cache and rebuild:

```bash
docker build --no-cache -t sentiment-api:latest .
```

## Connection Issues

### Cannot Connect

**Fix**:

```bash
# Verify API is running
curl http://localhost:8000/api/v1/health

# Check port mapping
docker ps

# Check if port is in use
lsof -i :8000
```

## Common Errors

**ModuleNotFoundError**: Run from project root or set PYTHONPATH

**CUDA out of memory**: Reduce batch size or switch to CPU

**Connection timeout**: Check network and HuggingFace Hub status

**Tests failing**: Install dev dependencies with `pip install -r requirements-dev.txt`

**No logs**: Set `LOG_LEVEL=DEBUG` in `.env` and check `docker-compose logs -f`


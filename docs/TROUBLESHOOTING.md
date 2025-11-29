# Troubleshooting Guide

Common issues and solutions for the Sentiment Analysis API.

## Model Loading Issues

### Model Not Found

**Symptoms:**
- `Model not found` error
- `404 Client Error: Not Found for url`

**Solutions:**
1. Verify model name in `.env` file:
   ```
   MODEL_NAME=IberaSoft/customer-sentiment-analyzer
   ```
2. Check internet connection (model downloads from HuggingFace)
3. Verify HuggingFace Hub status: https://status.huggingface.co
4. For private models, ensure `HF_TOKEN` is set
5. Try downloading manually:
   ```python
   from transformers import AutoModel
   AutoModel.from_pretrained("IberaSoft/customer-sentiment-analyzer")
   ```

### Model Loading Timeout

**Symptoms:**
- Model takes too long to load
- Timeout errors

**Solutions:**
1. Check network connection speed
2. Increase timeout in Docker/container settings
3. Pre-download model to local cache:
   ```python
   from transformers import AutoModel
   model = AutoModel.from_pretrained("IberaSoft/customer-sentiment-analyzer", cache_dir="./models")
   ```

## Performance Issues

### Slow Inference

**Symptoms:**
- High latency (>100ms per request)
- Low throughput

**Solutions:**
1. **Use GPU** if available:
   ```bash
   DEVICE=cuda DEVICE_ID=0
   ```
2. **Enable quantization** (see `training/optimize.py`)
3. **Batch requests** together instead of single requests
4. **Increase batch size** in `.env`:
   ```
   MAX_BATCH_SIZE=64
   ```
5. **Use ONNX runtime** for 2-3x speedup (requires model conversion)

### High Memory Usage

**Symptoms:**
- Out of memory errors
- Container killed

**Solutions:**
1. **Reduce batch size**:
   ```
   MAX_BATCH_SIZE=16
   ```
2. **Use quantized model** (smaller memory footprint)
3. **Increase Docker memory limits**:
   ```yaml
   # docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 4G
   ```
4. **Clear model cache** periodically
5. **Use CPU** if GPU memory is limited

## API Issues

### 500 Internal Server Error

**Symptoms:**
- All requests return 500
- Error logs show exceptions

**Solutions:**
1. Check application logs:
   ```bash
   docker-compose logs -f api
   ```
2. Verify model is loaded:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
3. Check environment variables
4. Verify dependencies are installed correctly

### Invalid Request Errors

**Symptoms:**
- `422 Unprocessable Entity` errors
- Validation errors

**Solutions:**
1. Check request format matches API schema
2. Verify `Content-Type: application/json` header
3. Check text length (max 5000 characters)
4. For batch requests, ensure batch size ≤ 100

### CORS Errors

**Symptoms:**
- Browser shows CORS errors
- Requests blocked from frontend

**Solutions:**
1. CORS is enabled by default for all origins
2. For production, restrict origins in `app/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       ...
   )
   ```

## Docker Issues

### Container Won't Start

**Symptoms:**
- Container exits immediately
- `docker ps` shows no running containers

**Solutions:**
1. Check logs:
   ```bash
   docker logs sentiment-api
   ```
2. Verify Dockerfile syntax
3. Check port availability:
   ```bash
   lsof -i :8000
   ```
4. Verify environment variables

### Image Build Fails

**Symptoms:**
- `docker build` fails
- Dependency installation errors

**Solutions:**
1. Check internet connection
2. Verify Python version (3.11+)
3. Clear Docker cache:
   ```bash
   docker build --no-cache -t sentiment-api:latest .
   ```
4. Check Dockerfile for syntax errors

## Network Issues

### Cannot Connect to API

**Symptoms:**
- Connection refused
- Timeout errors

**Solutions:**
1. Verify API is running:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
2. Check firewall settings
3. Verify port mapping in Docker:
   ```bash
   docker ps
   # Should show 0.0.0.0:8000->8000/tcp
   ```
4. Check if port is already in use:
   ```bash
   lsof -i :8000
   ```

## Logging Issues

### No Logs Appearing

**Symptoms:**
- Logs not visible
- Empty log files

**Solutions:**
1. Check log level in `.env`:
   ```
   LOG_LEVEL=DEBUG
   ```
2. Verify logging configuration in `app/utils/logger.py`
3. Check Docker logs:
   ```bash
   docker-compose logs -f
   ```

## Testing Issues

### Tests Failing

**Symptoms:**
- `pytest` fails
- Import errors

**Solutions:**
1. Install dev dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Run tests with verbose output:
   ```bash
   pytest -v
   ```
3. Check Python version (3.11+)
4. Verify test environment setup

## Getting Help

If you're still experiencing issues:

1. Check the [GitHub Issues](https://github.com/IberaSoft/sentiment-analysis-api/issues)
2. Review application logs for detailed error messages
3. Verify your environment matches the requirements
4. Check HuggingFace model page for model-specific issues

## Common Error Messages

### `ModuleNotFoundError: No module named 'app'`

**Solution:** Run from project root directory or set `PYTHONPATH`

### `CUDA out of memory`

**Solution:** Reduce batch size or use CPU

### `Connection timeout`

**Solution:** Check network connection and HuggingFace Hub status

### `Invalid model identifier`

**Solution:** Verify model name and HuggingFace token (for private models)


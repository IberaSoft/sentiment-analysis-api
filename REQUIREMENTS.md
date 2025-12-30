# Requirements Files Guide

This document explains the purpose of each requirements file and how to use them.

## File Structure

```
├── requirements.txt           # Main dependencies (API + HuggingFace Spaces)
├── requirements-dev.txt       # Development and testing dependencies
└── requirements-training.txt  # Training-specific dependencies
```

## Requirements Files

### `requirements.txt` ⭐ Main File

**Purpose:** Core dependencies for both the FastAPI application and HuggingFace Spaces.

**Used by:**
- FastAPI application (production deployment)
- HuggingFace Spaces (Gradio demo)
- Docker containers

**Includes:**
- FastAPI and Uvicorn (API framework)
- Transformers and PyTorch (ML model)
- Gradio (UI for Spaces)
- Prometheus (monitoring)
- Pydantic (data validation)

**Installation:**
```bash
pip install -r requirements.txt
```

**Note:** HuggingFace Spaces automatically uses this file. Do NOT create a separate `requirements-spaces.txt`.

### `requirements-dev.txt` 🛠️ Development

**Purpose:** Additional tools for development, testing, and code quality.

**Used by:**
- Local development
- CI/CD pipelines
- Code quality checks

**Includes:**
- All dependencies from `requirements.txt` (via `-r requirements.txt`)
- pytest (testing framework)
- black, flake8, isort (code formatting and linting)
- mypy (type checking)
- pre-commit (git hooks)
- locust (load testing)
- ipython, jupyter (development tools)

**Installation:**
```bash
pip install -r requirements-dev.txt
```

This automatically installs production dependencies + dev tools.

### `requirements-training.txt` 🎓 Training

**Purpose:** Dependencies specific to model training workflows.

**Used by:**
- Training scripts in `/training` folder
- Model fine-tuning
- Dataset preparation

**Includes:**
- transformers, torch (ML frameworks)
- datasets (HuggingFace datasets library)
- scikit-learn (evaluation metrics)
- accelerate (distributed training)
- huggingface-hub (model upload)
- requests (HTTP client)

**Installation:**
```bash
pip install -r requirements-training.txt
```

## Usage Scenarios

### 1. Running the FastAPI Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Running the Gradio Demo Locally

```bash
# Install dependencies (same as API)
pip install -r requirements.txt

# Run Gradio app
python app.py
```

### 3. Development and Testing

```bash
# Install all dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
black app/ tests/
flake8 app/ tests/
isort app/ tests/
```

### 4. Training a Model

```bash
# Install training dependencies
pip install -r requirements-training.txt

# Prepare dataset
python training/prepare_dataset.py

# Train model
python training/train.py --data-path ./data
```

## HuggingFace Spaces

**Important:** HuggingFace Spaces automatically looks for `requirements.txt` in the root directory.

### What to upload to Spaces:
- ✅ `requirements.txt` - **Required** (used automatically)
- ✅ `app.py` - Your Gradio application
- ✅ `README.md` - Space documentation (optional)

### What NOT to upload:
- ❌ `requirements-dev.txt` - Not needed in Spaces
- ❌ `requirements-training.txt` - Not needed in Spaces
- ❌ `app/` folder - Not needed (Spaces uses `app.py` directly)

### Deploying to Spaces:

1. **Via Git:**
   ```bash
   git clone https://huggingface.co/spaces/YourUsername/your-space
   cd your-space
   
   # Copy files
   cp /path/to/requirements.txt .
   cp /path/to/app.py .
   
   # Commit and push
   git add requirements.txt app.py
   git commit -m "Update dependencies"
   git push
   ```

2. **Via Web UI:**
   - Go to your Space
   - Upload/edit `requirements.txt`
   - Upload/edit `app.py`

The Space will automatically rebuild when you push changes.

## Dependency Updates

When updating dependencies for security or compatibility:

1. **Update `requirements.txt`** - This affects both API and Spaces
2. **Update `requirements-training.txt`** - If training dependencies need updates
3. **Test locally:**
   ```bash
   pip install -r requirements.txt
   pytest tests/
   python app.py  # Test Gradio
   ```
4. **Commit and push to GitHub**
5. **Push to HuggingFace Spaces** (it will pick up the new `requirements.txt`)

## Version Pinning

All dependencies are pinned to specific versions (e.g., `gradio==4.44.1`) to ensure:
- Reproducible builds
- Consistent behavior across environments
- Security (we control when to update)

To update a specific package:
```bash
# Check latest version
pip index versions package-name

# Update in requirements.txt
# Test thoroughly before committing
```

## Docker

The Docker build uses `requirements.txt`:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

## Common Issues

### Issue: "No module named 'transformers'" in Spaces
**Solution:** Ensure `requirements.txt` (not `requirements-spaces.txt`) is in your Space root.

### Issue: Dependency conflicts
**Solution:** Use a virtual environment to isolate dependencies:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### Issue: Slow installation
**Solution:** Use pip cache or install without dependencies for specific packages:
```bash
pip install --no-deps package-name
```

## Summary

- **`requirements.txt`** → Use for everything (API, Spaces, Docker)
- **`requirements-dev.txt`** → Use for local development only
- **`requirements-training.txt`** → Use for model training only
- **HuggingFace Spaces** → Always uses `requirements.txt` (nothing else needed)

---

**Last Updated:** December 30, 2025

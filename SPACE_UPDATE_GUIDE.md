# HuggingFace Space Update Guide

## ✅ Yes, you need to update both files in your Space

Your HuggingFace Space needs the updated `app.py` and `requirements.txt` files to work correctly.

## Files to Update

### 1. `app.py` - **REQUIRED UPDATE**
The Space's current `app.py` likely has issues. You need to replace it with our fixed version that:
- Uses `DistilBertTokenizer` and `DistilBertForSequenceClassification` directly
- Bypasses the missing `model_type` in config.json
- Has proper error handling

### 2. `requirements.txt` - **REQUIRED UPDATE**
The Space needs all dependencies including:
- `gradio==4.19.0`
- `plotly==5.18.0`
- `transformers==4.53.0`
- `torch==2.8.0`
- `sentencepiece==0.1.99`

## How to Update

### Option 1: If Space is connected to GitHub repo (Recommended)

1. **Push your changes to GitHub:**
   ```bash
   git push origin main
   ```

2. **The Space will auto-update** - HuggingFace Spaces automatically syncs with connected repos

3. **Restart the Space** (if needed):
   - Go to Space Settings → Restart this Space

### Option 2: Manual upload via HuggingFace web interface

1. **Go to your Space:**
   - https://huggingface.co/spaces/IberaSoft/sentiment-analyzer-demo

2. **Click "Files and versions" tab**

3. **Update `app.py`:**
   - Click on `app.py`
   - Click "Edit" or "Replace"
   - Copy the contents from your local `app.py` file
   - Save

4. **Update `requirements.txt`:**
   - Click on `requirements.txt`
   - Click "Edit" or "Replace"
   - Copy the contents from your local `requirements.txt` file
   - Save

5. **Restart the Space:**
   - Go to Settings → Restart this Space
   - Wait for build to complete

## Quick Copy-Paste

### `app.py` - First 20 lines (verify it matches):
```python
"""Gradio app for HuggingFace Spaces demo."""
import gradio as gr
from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification
import os
import torch

# Initialize model
MODEL_NAME = os.getenv("MODEL_NAME", "IberaSoft/customer-sentiment-analyzer")

# Load model
print(f"Loading model: {MODEL_NAME}")
classifier = None
try:
    # Try to load with token if available (for private models)
    hf_token = os.getenv("HF_TOKEN")
    
    # Load using DistilBERT classes directly (bypasses config.json model_type requirement)
    print("Loading tokenizer...")
    tokenizer = DistilBertTokenizer.from_pretrained(
        MODEL_NAME,
        token=hf_token if hf_token else None
    )
```

### `requirements.txt` - Full content:
```
# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# ML dependencies
transformers==4.53.0
torch==2.8.0
sentencepiece==0.1.99

# Gradio (for HuggingFace Spaces demo)
gradio==4.19.0
plotly==5.18.0

# Monitoring
prometheus-client==0.19.0

# Utilities
python-multipart==0.0.18
```

## Verification Checklist

After updating, verify:

- [ ] `app.py` uses `DistilBertTokenizer` and `DistilBertForSequenceClassification`
- [ ] `requirements.txt` includes `gradio==4.19.0` and `plotly==5.18.0`
- [ ] Space restarts without errors
- [ ] Model loads successfully (check logs)
- [ ] Demo works - can input text and get predictions

## Current Status

✅ **Local files are correct:**
- `app.py` - Fixed to use DistilBERT classes directly
- `requirements.txt` - Has all required dependencies

⚠️ **Space needs update:**
- Space's `app.py` - Needs to be replaced
- Space's `requirements.txt` - Needs to be updated

## After Update

Once you update both files and restart the Space:
1. Check the logs - should see "Model loaded successfully!"
2. Test the demo with sample text
3. Verify predictions work correctly

The Space should work perfectly after these updates! 🎉


# HuggingFace Spaces Deployment Guide

## Overview

Deploy your sentiment analysis model as an interactive demo on HuggingFace Spaces using Gradio.

**Live Demo**: [HuggingFace Spaces](https://huggingface.co/spaces/IberaSoft/sentiment-analyzer-demo)

## Required Files

These files must be in your Space's root directory:

1. **app.py** - Gradio application
2. **requirements.txt** - All dependencies
3. **README.md** - Space description (optional)

## Quick Start

### Option 1: GitHub Integration (Recommended)

1. Fork this repository
2. Create a new Space on HuggingFace
3. Connect your GitHub repository
4. The Space auto-deploys on every push

### Option 2: Manual Upload

1. Go to your Space on HuggingFace
2. Click "Files and versions" → "Add file"
3. Upload `app.py` and `requirements.txt`
4. The Space builds automatically

## Requirements

Your `requirements.txt` must include:

```txt
gradio==4.19.0
plotly==5.18.0
transformers==4.53.0
torch==2.8.0
sentencepiece==0.1.99
```

## Environment Variables

Set these in Space Settings → Variables and secrets:

- **HF_TOKEN** (optional): Required for private models
- **MODEL_NAME** (optional): Defaults to `IberaSoft/customer-sentiment-analyzer`

## Model Repository Fix

If you encounter "model not recognized" errors, the model repository is missing `model_type` in `config.json`.

### Fix Using Script

```bash
# Get HuggingFace token from: https://huggingface.co/settings/tokens
export HF_TOKEN="your_token_here"

python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer
```

This adds the missing `model_type` and tokenizer files to your model repository.

## Troubleshooting

### ModuleNotFoundError

**Cause**: Missing dependency in `requirements.txt`

**Fix**: Verify all required packages are listed and restart the Space

### Model Loading Fails

**Cause**: Missing `model_type` or tokenizer files

**Fix**: Run the `fix_model_repo.py` script (see above)

### @gr.cache AttributeError

**Cause**: Using deprecated Gradio decorator

**Fix**: Remove `@gr.cache` from your code (not available in Gradio 4.x)

## Updating Your Space

### Via GitHub

```bash
git push origin main
```

The Space auto-updates within a few minutes.

### Via Web Interface

1. Go to your Space → "Files and versions"
2. Click on the file to edit
3. Make changes and commit
4. Space rebuilds automatically

## Testing Locally

Before deploying, test your Gradio app locally:

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860` to test the interface.

## Verification Checklist

After deployment:

- [ ] Space loads without errors
- [ ] Model loads successfully (check build logs)
- [ ] Can input text and receive predictions
- [ ] Confidence scores display correctly

## Common Issues

**Space stuck building**: Check logs for missing dependencies or syntax errors

**Model not found**: Verify model is public or HF_TOKEN is set correctly

**Gradio version conflicts**: Ensure you're using Gradio 4.19.0 or newer

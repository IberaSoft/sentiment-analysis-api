# HuggingFace Space Setup Guide

This guide explains how to set up the HuggingFace Space demo.

## Files Required for Space

The following files should be in the root of your Space repository:

1. **app.py** - Main Gradio application (✅ Created)
2. **requirements.txt** - Dependencies (⚠️ See note below)
3. **README.md** - Space description (✅ Created as README_SPACE.md)

## Important Notes

### Requirements File

For HuggingFace Spaces, the requirements file **must** be named `requirements.txt` in the root directory.

**Option 1: Copy requirements-spaces.txt to requirements.txt**
```bash
cp requirements-spaces.txt requirements.txt
```

**Option 2: Use the Space's requirements file directly**
When creating/updating the Space, ensure `requirements-spaces.txt` is renamed to `requirements.txt` in the Space repository.

### Environment Variables

If your model is private, set the `HF_TOKEN` environment variable in the Space settings:
- Go to Space Settings → Variables and secrets
- Add `HF_TOKEN` with your HuggingFace token

You can also set `MODEL_NAME` if you want to use a different model.

### Model Access

The model `IberaSoft/customer-sentiment-analyzer` must be:
- Public, OR
- Accessible with the provided `HF_TOKEN`

## Common Issues Fixed

1. ✅ **Label Format Handling**: The app now handles different label formats (POSITIVE, positive, LABEL_0, etc.)
2. ✅ **Error Handling**: Better error messages and fallback handling
3. ✅ **Model Loading**: Support for private models with token authentication
4. ✅ **Score Normalization**: Proper handling of score normalization

## Testing Locally

Before deploying to Spaces, test locally:

```bash
# Install dependencies
pip install -r requirements-spaces.txt

# Run the app
python app.py
```

## Deployment

1. Create a new Space on HuggingFace
2. Connect your GitHub repository
3. Ensure `app.py` and `requirements.txt` are in the root
4. Set environment variables if needed
5. The Space will auto-deploy!


# HuggingFace Spaces Migration Guide

## Overview

This guide explains how to update your HuggingFace Space to use the consolidated `requirements.txt` file instead of the deprecated `requirements-spaces.txt`.

## Why the Change?

- **HuggingFace Spaces convention**: Spaces automatically look for `requirements.txt`, not `requirements-spaces.txt`
- **Simplified maintenance**: One file works for both API and Spaces deployments
- **Avoid confusion**: Eliminates the need to maintain separate requirements files

## Migration Steps

### Step 1: Update Your HuggingFace Space

#### Option A: Via Web UI (Easiest)

1. **Navigate to your Space:**
   ```
   https://huggingface.co/spaces/YourUsername/your-space
   ```

2. **Delete old file (if exists):**
   - Click "Files" tab
   - Find `requirements-spaces.txt`
   - Click the file → "Delete this file"
   - Commit deletion

3. **Update requirements.txt:**
   - Click "Files" tab
   - Click `requirements.txt` (or "Add file" → "Create new file" if it doesn't exist)
   - Replace/add this content:
     ```txt
     # Core API dependencies
     fastapi==0.115.6
     uvicorn[standard]==0.34.0
     pydantic==2.10.5
     pydantic-settings==2.7.1

     # ML dependencies (required for both API and HuggingFace Spaces)
     transformers==4.53.0
     torch==2.8.0
     sentencepiece==0.1.99

     # Gradio UI (for HuggingFace Spaces)
     # Note: This file is used directly by HuggingFace Spaces
     gradio==4.44.1
     plotly==5.18.0

     # Monitoring (API only)
     prometheus-client==0.19.0

     # Utilities (API only)
     python-multipart==0.0.18
     ```
   - Commit changes

4. **Verify app.py:**
   - Ensure line 3 is: `from transformers import pipeline`
   - NOT: `from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification`

5. **Wait for rebuild:**
   - The Space will automatically rebuild
   - Check the build logs for any errors
   - Test your Space once it's running

#### Option B: Via Git (Advanced)

1. **Clone your Space:**
   ```bash
   git clone https://huggingface.co/spaces/YourUsername/your-space
   cd your-space
   ```

2. **Copy updated requirements.txt from your repo:**
   ```bash
   cp /path/to/sentiment-analysis-api/requirements.txt .
   ```

3. **Remove old file (if exists):**
   ```bash
   git rm requirements-spaces.txt  # Only if it exists
   ```

4. **Commit and push:**
   ```bash
   git add requirements.txt
   git commit -m "Migrate to consolidated requirements.txt

   - Updated Gradio to 4.44.1 for security fixes
   - Removed requirements-spaces.txt (now using requirements.txt)
   - Updated all dependencies to latest secure versions"
   git push
   ```

5. **Monitor the rebuild:**
   - Go to your Space URL
   - Check build logs
   - Test functionality

### Step 2: Update Your Local Repository

If you have a local clone of your GitHub repository:

```bash
cd /path/to/sentiment-analysis-api

# Pull latest changes
git pull origin main

# Verify requirements-spaces.txt is gone
ls requirements*.txt
# Should show: requirements.txt, requirements-dev.txt, requirements-training.txt
```

## Verification Checklist

After migration, verify:

- ✅ Space builds successfully without errors
- ✅ Gradio interface loads correctly
- ✅ Model predictions work (test with example inputs)
- ✅ No "ModuleNotFoundError" in build logs
- ✅ `requirements-spaces.txt` is deleted from Space
- ✅ `requirements.txt` exists in Space root

## Troubleshooting

### Error: "No module named 'transformers'"

**Cause:** Space is not finding or reading `requirements.txt`

**Solution:**
1. Verify the file is named exactly `requirements.txt` (not `Requirements.txt` or `requirements-spaces.txt`)
2. Verify it's in the root directory of your Space
3. Check the file content includes `transformers==4.53.0`
4. Trigger a rebuild by making a small change and committing

### Error: "No module named 'gradio'"

**Cause:** `gradio` is missing from `requirements.txt`

**Solution:**
Add this line to `requirements.txt`:
```txt
gradio==4.44.1
```

### Space builds but shows blank page

**Cause:** Usually an error in `app.py`

**Solution:**
1. Check build logs for Python errors
2. Verify `app.py` line 3: `from transformers import pipeline`
3. Check for syntax errors in `app.py`

### Build timeout

**Cause:** Installing PyTorch takes time, especially on CPU-only containers

**Solution:**
- Wait patiently (first build can take 5-10 minutes)
- Consider using a smaller PyTorch version if needed
- Check Space settings for hardware acceleration options

## What's Different?

### Before (Old Setup):
```
Space Root/
├── requirements-spaces.txt  ❌ (Spaces didn't use this)
├── requirements.txt         ⚠️ (May be missing or outdated)
└── app.py
```

### After (New Setup):
```
Space Root/
├── requirements.txt         ✅ (Used by Spaces automatically)
└── app.py
```

## Benefits of New Setup

1. **Automatic detection**: HF Spaces finds `requirements.txt` automatically
2. **Less confusion**: No ambiguity about which file to use
3. **Easier updates**: Single file to maintain for dependency updates
4. **Industry standard**: Follows Python/HuggingFace conventions
5. **Better documentation**: Clear purpose and usage

## Future Updates

When updating dependencies in the future:

1. Update `requirements.txt` in your GitHub repo
2. Push to GitHub
3. Copy the updated file to your HuggingFace Space (or sync via Git)
4. Space automatically rebuilds with new dependencies

## Need Help?

If you encounter issues during migration:

1. Check build logs in your Space
2. Refer to [REQUIREMENTS.md](../REQUIREMENTS.md) for detailed documentation
3. Review [SECURITY_UPDATES.md](../SECURITY_UPDATES.md) for recent changes
4. Check HuggingFace Spaces documentation: https://huggingface.co/docs/hub/spaces

---

**Migration Date:** December 30, 2025
**Gradio Version:** 4.44.1
**Status:** Recommended for all Spaces

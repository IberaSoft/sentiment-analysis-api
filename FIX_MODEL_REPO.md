# Fix Model Repository - Clean Solution

## Problem

The model repository `IberaSoft/customer-sentiment-analyzer` is missing:
1. `model_type` in `config.json`
2. Tokenizer files (`vocab.txt`, `tokenizer_config.json`)

This causes errors when loading the model.

## Clean Solution

Instead of adding workarounds in the code, **fix the model repository** by adding the missing files.

## How to Fix

### Step 0: Get Your HuggingFace Token

You need a HuggingFace token to upload files to the model repository.

**How to get it:**
1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name it (e.g., "sentiment-analysis-api")
4. Select **"Write"** type (needed to upload files)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

The token looks like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Set it as environment variable:**
```bash
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Or use it directly in the command (see Step 1).

📖 **Full guide**: See [docs/HF_TOKEN_GUIDE.md](docs/HF_TOKEN_GUIDE.md) for detailed instructions.

### Step 1: Run the Fix Script

```bash
# Option 1: Using environment variable
export HF_TOKEN="your_token_here"
python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer

# Option 2: Pass token directly
python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer \
  --token hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

This script will:
1. ✅ Add `model_type: "distilbert"` to `config.json` if missing
2. ✅ Upload missing tokenizer files from the base model (`distilbert-base-uncased`)
3. ✅ Ensure all necessary files are present

### Step 2: Verify

After running the script, the model should load normally:

```python
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="IberaSoft/customer-sentiment-analyzer"
)
# Should work without errors!
```

## What the Script Does

1. **Fixes config.json**: Adds `"model_type": "distilbert"` if missing
2. **Adds tokenizer files**: Downloads tokenizer files from `distilbert-base-uncased` and uploads them to your model repo
3. **Verifies**: Checks that all necessary files are present

## After Fixing

Once the model repository is fixed:
- ✅ `app.py` can use simple `pipeline()` call (no workarounds needed)
- ✅ Model loads normally without fallbacks
- ✅ Clean, maintainable code

## Current app.py (Clean Version)

After fixing the model repository, `app.py` is simple and clean:

```python
classifier = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    token=hf_token if hf_token else None,
    return_all_scores=True
)
```

No workarounds, no fallbacks - just clean code! 🎉


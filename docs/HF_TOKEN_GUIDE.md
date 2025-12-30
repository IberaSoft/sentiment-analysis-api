# HuggingFace Token Guide

## What is HF_TOKEN?

Authentication token for accessing private models and uploading to HuggingFace Hub.

## Get Your Token

### Step 1: Login

Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### Step 2: Create Token

1. Click "New token"
2. Name: `sentiment-analysis-api`
3. Type: **Write** (for uploads) or **Read** (for private models)
4. Click "Generate token"
5. **Copy immediately** (you can't see it again!)

Token format: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Use Your Token

### Environment Variable

```bash
# Linux/macOS
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Windows PowerShell
$env:HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### .env File

```bash
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Command Line

```bash
python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer \
  --token hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### HuggingFace Spaces

1. Go to Space Settings → Variables and secrets
2. Add variable:
   - Name: `HF_TOKEN`
   - Value: Your token
3. Click "Add"

## Security

**Never commit tokens to Git!**

✅ Use `.env` file (add to `.gitignore`)
✅ Use environment variables
✅ Use Spaces secrets
❌ Never hardcode in code

## Verify Token

```bash
huggingface-cli whoami
```

Should display your username if working correctly.

## Token Types

- **Read**: Download private models/datasets
- **Write**: Upload and modify repositories (needed for this project)

## Troubleshooting

**Invalid token**: Verify token starts with `hf_` and has correct permissions

**Permission denied**: Ensure you own the repository and token type is "Write"

**Token not found**: Check with `echo $HF_TOKEN` or verify `.env` file location


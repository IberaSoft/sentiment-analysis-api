# How to Get Your HuggingFace Token

## What is HF_TOKEN?

The HuggingFace token (`HF_TOKEN`) is an authentication token that allows you to:
- Access private models and datasets
- Upload models and datasets to HuggingFace Hub
- Use HuggingFace APIs and tools

## How to Get Your Token

### Step 1: Create/Login to HuggingFace Account

1. Go to [HuggingFace.co](https://huggingface.co)
2. Click **"Sign Up"** (if new) or **"Log In"** (if you have an account)
3. Complete the registration/login process

### Step 2: Generate Access Token

1. **Click on your profile icon** (top right corner)
2. Select **"Settings"** from the dropdown menu
3. In the left sidebar, click **"Access Tokens"**
4. Click **"New token"** button
5. Configure your token:
   - **Token name**: Give it a descriptive name (e.g., "sentiment-analysis-api")
   - **Type**: Select **"Write"** (for uploading models) or **"Read"** (for accessing private models)
   - For this project, use **"Write"** to upload/fix models
6. Click **"Generate token"**

### Step 3: Copy Your Token

⚠️ **Important**: Copy the token immediately! You won't be able to see it again.

The token will look something like:
```
hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## How to Use the Token

### Option 1: Environment Variable (Recommended)

**Linux/macOS:**
```bash
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Windows (Command Prompt):**
```cmd
set HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Option 2: In .env File

Create or edit `.env` file in your project root:

```bash
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Then load it in your application (Python automatically loads `.env` with `python-dotenv` or `pydantic-settings`).

### Option 3: Pass as Command Line Argument

```bash
python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer \
  --token hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Option 4: HuggingFace Spaces Environment Variable

If using HuggingFace Spaces:

1. Go to your Space: https://huggingface.co/spaces/IberaSoft/sentiment-analyzer-demo
2. Click **"Settings"** tab
3. Scroll to **"Variables and secrets"** section
4. Click **"New variable"**
5. Set:
   - **Name**: `HF_TOKEN`
   - **Value**: Your token (starts with `hf_`)
6. Click **"Add"**

The token will be available as an environment variable in your Space.

## Security Best Practices

⚠️ **Never commit tokens to Git!**

1. ✅ Use `.env` file and add it to `.gitignore`
2. ✅ Use environment variables
3. ✅ Use HuggingFace Spaces secrets
4. ❌ Never hardcode tokens in code
5. ❌ Never commit tokens to version control

## Verify Your Token Works

Test your token:

```bash
# Using huggingface-cli
huggingface-cli whoami

# Or in Python
from huggingface_hub import whoami
print(whoami())
```

If it works, you'll see your username. If not, check that:
- Token is correct
- Token has the right permissions (Read/Write)
- Token hasn't been revoked

## Token Types

- **Read Token**: Can download private models/datasets
- **Write Token**: Can upload models/datasets and modify repositories
- **Admin Token**: Full access (use with caution)

For this project, you need a **Write token** to:
- Fix the model repository (upload missing files)
- Upload new model versions
- Update model files

## Troubleshooting

### "Invalid token" error
- Check that you copied the entire token (starts with `hf_`)
- Verify token hasn't expired or been revoked
- Ensure token has correct permissions (Write for uploads)

### "Permission denied" error
- Make sure you own the model repository or have write access
- Verify token type is "Write" not just "Read"

### Token not found
- Check environment variable is set: `echo $HF_TOKEN`
- Verify `.env` file is in the correct location
- Ensure your code is reading the environment variable correctly

## Quick Reference

**Get Token:**
1. https://huggingface.co → Profile → Settings → Access Tokens → New token

**Use Token:**
```bash
export HF_TOKEN="your_token_here"
```

**Test Token:**
```bash
huggingface-cli whoami
```

## Links

- [HuggingFace Access Tokens Documentation](https://huggingface.co/docs/hub/security-tokens)
- [HuggingFace Settings Page](https://huggingface.co/settings/tokens)
- [HuggingFace Hub Documentation](https://huggingface.co/docs/hub)


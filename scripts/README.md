# Scripts Directory

This directory contains utility scripts for various tasks related to model management, deployment, and testing.

## Scripts Overview

### Model Management

#### `upload_to_hf.py`
Upload a trained model directory to HuggingFace Hub.

**Use case**: Upload a locally trained model after training is complete.

```bash
python scripts/upload_to_hf.py \
  --model-dir ./models/customer-sentiment-v1 \
  --repo-name IberaSoft/customer-sentiment-analyzer \
  --token $HF_TOKEN
```

#### `upload_base_model.py`
Upload a configured base DistilBERT model (without training) to HuggingFace Hub.

**Use case**: Initialize a model repository with a base model configured for 3-class sentiment analysis.

```bash
python scripts/upload_base_model.py \
  --repo-name IberaSoft/customer-sentiment-analyzer \
  --base-model distilbert-base-uncased \
  --token $HF_TOKEN
```

**Note**: This uploads the base model without training. For production use, train the model using `training/train.py`.

#### `fix_model_repo.py`
Fix a HuggingFace model repository by adding missing files (config.json, tokenizer files).

**Use case**: Repair a model repository that's missing required files or has configuration issues.

```bash
python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer \
  --token $HF_TOKEN
```

### Data Management

#### `download_data.py`
Download and inspect a dataset from HuggingFace.

**Use case**: Verify dataset availability and structure before training.

```bash
python scripts/download_data.py \
  --dataset-name IberaSoft/ecommerce-reviews-sentiment \
  --output-dir ./data
```

**Note**: For preparing training/validation/test splits, use `training/prepare_dataset.py` instead.

### Testing & Benchmarking

#### `benchmark.py`
Benchmark API performance with concurrent requests.

**Use case**: Load test the deployed API to measure latency and throughput.

```bash
python scripts/benchmark.py \
  --url http://localhost:8000/api/v1/predict \
  --num-requests 100 \
  --num-threads 10 \
  --text "This is a test review"
```

## Script vs Training Folder

### `/scripts` - Utility Scripts
- One-off operations
- Model repository management
- API testing and benchmarking
- Data inspection

### `/training` - Training Pipeline
- **`train.py`**: Main training script (includes upload functionality)
- **`evaluate.py`**: Model evaluation on test data
- **`prepare_dataset.py`**: Dataset preparation and splitting
- **`optimize.py`**: Model optimization (quantization)

## Common Workflows

### Full Training Pipeline
```bash
# 1. Prepare dataset
python training/prepare_dataset.py \
  --dataset-name IberaSoft/ecommerce-reviews-sentiment \
  --output-dir ./data

# 2. Train model (with upload to HF Hub)
python training/train.py \
  --data-path ./data \
  --output-dir ./models/customer-sentiment-v1 \
  --num-epochs 3 \
  --push-to-hub \
  --hub-repo-name IberaSoft/customer-sentiment-analyzer \
  --hub-token $HF_TOKEN

# 3. Evaluate model
python training/evaluate.py \
  --model-dir ./models/customer-sentiment-v1 \
  --test-data ./data/test.jsonl
```

### Upload Pre-trained Model
```bash
# If you already have a trained model locally
python scripts/upload_to_hf.py \
  --model-dir ./models/customer-sentiment-v1 \
  --repo-name IberaSoft/customer-sentiment-analyzer \
  --token $HF_TOKEN
```

### Fix Model Repository
```bash
# If your HF model repository has issues
python scripts/fix_model_repo.py \
  --model-id IberaSoft/customer-sentiment-analyzer \
  --token $HF_TOKEN
```

### Benchmark API
```bash
# Test deployed API performance
python scripts/benchmark.py \
  --url http://localhost:8000/api/v1/predict \
  --num-requests 1000 \
  --num-threads 20
```

## Environment Variables

- `HF_TOKEN`: HuggingFace API token (can be set instead of using --token flag)

## Dependencies

All scripts require the dependencies listed in `requirements.txt` or `requirements-training.txt`.

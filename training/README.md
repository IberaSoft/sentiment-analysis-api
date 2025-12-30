# Training Directory

This directory contains the complete training pipeline for the sentiment analysis model.

## Scripts

### `train.py`
Main training script that handles model training and optional upload to HuggingFace Hub.

**Features**:
- Train DistilBERT-based sentiment classifier
- Support for local and HuggingFace Hub datasets
- Automatic evaluation and metric tracking
- Optional push to HuggingFace Hub
- Configuration file support

**Usage**:
```bash
# Train locally
python training/train.py \
  --base-model distilbert-base-uncased \
  --data-path ./data \
  --output-dir ./models/customer-sentiment-v1 \
  --num-epochs 3 \
  --batch-size 16 \
  --learning-rate 2e-5

# Train and upload to HuggingFace Hub
python training/train.py \
  --base-model distilbert-base-uncased \
  --data-path ./data \
  --output-dir ./models/customer-sentiment-v1 \
  --num-epochs 3 \
  --push-to-hub \
  --hub-repo-name IberaSoft/customer-sentiment-analyzer \
  --hub-token $HF_TOKEN

# Using a config file
python training/train.py --config config.json
```

**Config file format** (`config.json`):
```json
{
  "base_model": "distilbert-base-uncased",
  "data_path": "./data",
  "output_dir": "./models/customer-sentiment-v1",
  "num_epochs": 3,
  "batch_size": 16,
  "learning_rate": 2e-5,
  "push_to_hub": true,
  "hub_repo_name": "IberaSoft/customer-sentiment-analyzer"
}
```

### `prepare_dataset.py`
Prepare and split dataset from HuggingFace Hub into train/validation/test sets.

**Usage**:
```bash
python training/prepare_dataset.py \
  --dataset-name IberaSoft/ecommerce-reviews-sentiment \
  --output-dir ./data \
  --train-size 15000 \
  --val-size 3000 \
  --test-size 2000
```

**Output**: Creates `train.jsonl`, `val.jsonl`, and `test.jsonl` in the output directory.

### `evaluate.py`
Evaluate a trained model on test data.

**Usage**:
```bash
python training/evaluate.py \
  --model-dir ./models/customer-sentiment-v1 \
  --test-data ./data/test.jsonl
```

**Metrics**:
- Accuracy
- F1 Score (weighted)
- Precision
- Recall
- Confusion Matrix

### `optimize.py`
Optimize trained models using quantization to reduce size.

**Usage**:
```bash
python training/optimize.py \
  --model-dir ./models/customer-sentiment-v1 \
  --output-dir ./models/customer-sentiment-v1-quantized \
  --method quantize
```

**Benefits**:
- Reduced model size (~75% smaller)
- Faster inference on CPU
- Minimal accuracy loss

## Complete Training Workflow

### 1. Prepare Dataset
```bash
python training/prepare_dataset.py \
  --dataset-name IberaSoft/ecommerce-reviews-sentiment \
  --output-dir ./data \
  --train-size 15000 \
  --val-size 3000 \
  --test-size 2000
```

### 2. Train Model
```bash
python training/train.py \
  --base-model distilbert-base-uncased \
  --data-path ./data \
  --output-dir ./models/customer-sentiment-v1 \
  --num-epochs 3 \
  --batch-size 16 \
  --learning-rate 2e-5 \
  --push-to-hub \
  --hub-repo-name IberaSoft/customer-sentiment-analyzer
```

### 3. Evaluate Model
```bash
python training/evaluate.py \
  --model-dir ./models/customer-sentiment-v1 \
  --test-data ./data/test.jsonl
```

### 4. (Optional) Optimize Model
```bash
python training/optimize.py \
  --model-dir ./models/customer-sentiment-v1 \
  --output-dir ./models/customer-sentiment-v1-quantized \
  --method quantize
```

## Data Format

Training data should be in JSONL format with the following structure:

```json
{"text": "This product is amazing!", "label": 2}
{"text": "Terrible service.", "label": 0}
{"text": "It's okay, nothing special.", "label": 1}
```

**Labels**:
- `0`: Negative
- `1`: Neutral
- `2`: Positive

## Training Tips

### Hyperparameters
- **Learning Rate**: Start with `2e-5` (default for BERT models)
- **Batch Size**: `16` or `32` depending on GPU memory
- **Epochs**: `3-5` (more epochs may lead to overfitting)

### GPU vs CPU
- **GPU**: Significantly faster training (recommended)
- **CPU**: Slower but works for small datasets

### Monitoring
- Check logs in `{output_dir}/logs` for training progress
- Evaluation runs after each epoch
- Best model is automatically saved based on F1 score

## Environment Variables

- `HF_TOKEN`: HuggingFace API token for private models/datasets

## Dependencies

Install training dependencies:
```bash
pip install -r requirements-training.txt
```

## Notes

- Training data must be prepared before running `train.py`
- The model automatically saves checkpoints after each epoch
- Only the best model (based on F1 score) is kept
- Use `--push-to-hub` to automatically upload after training

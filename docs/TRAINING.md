# Model Training Guide

## Prerequisites

- Python 3.11+
- GPU recommended (30-60 min training) or CPU (2-3 hours)
- HuggingFace account

## Quick Start

### 1. Prepare Dataset

```bash
cd training
python prepare_dataset.py \
  --output-dir ./data \
  --train-size 15000 \
  --val-size 3000 \
  --test-size 2000
```

### 2. Train Model

```bash
python train.py \
  --base-model distilbert-base-uncased \
  --data-path ./data \
  --output-dir ./models/customer-sentiment-v1 \
  --num-epochs 3 \
  --batch-size 16 \
  --learning-rate 2e-5
```

Or use the config file:

```bash
python train.py --config configs/training_config.yaml
```

### 3. Evaluate Model

```bash
python evaluate.py \
  --model-dir ./models/customer-sentiment-v1 \
  --test-data ./data/test.jsonl
```

Expected results: ~90% accuracy, ~0.89 F1 score

### 4. Optimize (Optional)

Reduce model size by 4x:

```bash
python optimize.py \
  --model-dir ./models/customer-sentiment-v1 \
  --output-dir ./models/customer-sentiment-v1-quantized \
  --method quantize
```

### 5. Upload to HuggingFace

```bash
export HF_TOKEN="your_token_here"

python ../scripts/upload_to_hf.py \
  --model-dir ./models/customer-sentiment-v1 \
  --repo-name your-username/your-model-name
```

## Training on Your Own Dataset

### Step 1: Prepare Data

Create a JSONL file with your reviews:

```json
{"text": "Great product!", "label": 2}
{"text": "Not bad, but could be better", "label": 1}
{"text": "Terrible quality", "label": 0}
```

Labels: `0` = negative, `1` = neutral, `2` = positive

### Step 2: Update Dataset Path

Edit `prepare_dataset.py` to point to your data file.

### Step 3: Train

Run the training commands above.

## Configuration

Edit `configs/training_config.yaml` to customize:

```yaml
base_model: "distilbert-base-uncased"
num_epochs: 3
batch_size: 16
learning_rate: 2e-5
weight_decay: 0.01
```

## Monitor Training

View training progress with TensorBoard:

```bash
tensorboard --logdir ./models/customer-sentiment-v1/logs
```

## Hyperparameter Tips

- **Learning Rate**: 2e-5 (try 1e-5 or 5e-5 if needed)
- **Batch Size**: 16 (adjust based on GPU memory)
- **Epochs**: 3-5 typically sufficient

## Troubleshooting

**Out of memory**: Reduce batch size or enable gradient accumulation

**Slow training**: Use GPU, increase batch size, or try a smaller base model

**Poor accuracy**: Check data quality, increase epochs, or adjust learning rate


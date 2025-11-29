# Training Guide

This guide explains how to train and fine-tune the sentiment analysis model.

## Prerequisites

- Python 3.11+
- CUDA-capable GPU (recommended for faster training)
- HuggingFace account and access to the dataset

## Dataset

The model is trained on the `IberaSoft/ecommerce-reviews-sentiment` dataset, which contains 20,000 labeled customer reviews.

## Training Steps

### 1. Prepare Dataset

Split the dataset into train/validation/test sets:

```bash
cd training
python prepare_dataset.py \
  --output-dir ./data \
  --train-size 15000 \
  --val-size 3000 \
  --test-size 2000
```

### 2. Train Model

Train the model using the prepared dataset:

```bash
python train.py \
  --base-model distilbert-base-uncased \
  --data-path ./data \
  --output-dir ./models/customer-sentiment-v1 \
  --num-epochs 3 \
  --batch-size 16 \
  --learning-rate 2e-5
```

Or use a config file:

```bash
python train.py --config configs/training_config.yaml
```

### 3. Evaluate Model

Evaluate the trained model on the test set:

```bash
python evaluate.py \
  --model-dir ./models/customer-sentiment-v1 \
  --test-data ./data/test.jsonl
```

### 4. Optimize Model (Optional)

Quantize the model to reduce size:

```bash
python optimize.py \
  --model-dir ./models/customer-sentiment-v1 \
  --output-dir ./models/customer-sentiment-v1-quantized \
  --method quantize
```

### 5. Upload to HuggingFace

Upload your trained model to HuggingFace Hub:

```bash
python ../scripts/upload_to_hf.py \
  --model-dir ./models/customer-sentiment-v1 \
  --repo-name your-username/your-model-name \
  --token your_hf_token
```

## Training Configuration

Edit `configs/training_config.yaml` to customize training parameters:

```yaml
base_model: "distilbert-base-uncased"
data_path: "./data"
output_dir: "./models/customer-sentiment-v1"
num_epochs: 3
batch_size: 16
learning_rate: 2e-5
weight_decay: 0.01
warmup_steps: 500
logging_steps: 100
eval_strategy: "epoch"
save_strategy: "epoch"
save_total_limit: 2
```

## Fine-tuning on Your Data

To fine-tune on your own dataset:

1. **Prepare your data** in JSONL format:
```json
{"text": "Your review text", "label": 2}
```
Where labels are: 0=negative, 1=neutral, 2=positive

2. **Update the dataset path** in `prepare_dataset.py` or use your own script

3. **Train** using the same commands above

## Hyperparameter Tuning

Key hyperparameters to tune:

- **Learning Rate**: Start with 2e-5, try 1e-5 or 5e-5
- **Batch Size**: Adjust based on GPU memory (16, 32, 64)
- **Epochs**: 3-5 epochs usually sufficient
- **Weight Decay**: 0.01 for regularization

## Monitoring Training

Training logs are saved to `{output_dir}/logs`. Use TensorBoard:

```bash
tensorboard --logdir ./models/customer-sentiment-v1/logs
```

## Expected Results

With the default configuration, you should achieve:
- **Accuracy**: ~90%
- **F1 Score**: ~0.89
- **Training Time**: ~30-60 minutes on GPU

## Troubleshooting

### Out of Memory

- Reduce batch size
- Use gradient accumulation
- Enable mixed precision training

### Slow Training

- Use GPU if available
- Increase batch size
- Use a smaller model (e.g., distilbert-base-uncased)

### Poor Performance

- Check data quality
- Increase training epochs
- Adjust learning rate
- Try different base models


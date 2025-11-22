"""Train sentiment analysis model."""
import argparse
import json
from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import load_dataset, Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support


def load_data(data_path: str):
    """Load training data."""
    dataset = load_dataset("json", data_files={
        "train": str(Path(data_path) / "train.jsonl"),
        "val": str(Path(data_path) / "val.jsonl")
    })
    return dataset


def tokenize_function(examples, tokenizer):
    """Tokenize examples."""
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )


def compute_metrics(eval_pred):
    """Compute evaluation metrics."""
    predictions, labels = eval_pred
    predictions = predictions.argmax(axis=-1)
    
    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="weighted")
    precision, recall, _, _ = precision_recall_fscore_support(
        labels, predictions, average="weighted", zero_division=0
    )
    
    return {
        "accuracy": accuracy,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }


def train(
    base_model: str = "distilbert-base-uncased",
    data_path: str = "./data",
    output_dir: str = "./models/customer-sentiment-v1",
    num_epochs: int = 3,
    batch_size: int = 16,
    learning_rate: float = 2e-5
):
    """Train the model."""
    print(f"Loading base model: {base_model}")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForSequenceClassification.from_pretrained(
        base_model,
        num_labels=3
    )
    
    # Load data
    print("Loading dataset...")
    dataset = load_data(data_path)
    
    # Tokenize
    print("Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True
    )
    
    # Ensure labels are integers
    def format_labels(examples):
        if "label" in examples:
            # Convert labels to integers if they're strings
            labels = examples["label"]
            if isinstance(labels[0], str):
                label_map = {"negative": 0, "neutral": 1, "positive": 2}
                examples["label"] = [label_map.get(l.lower(), 1) for l in labels]
        return examples
    
    tokenized_dataset = tokenized_dataset.map(format_labels, batched=True)
    
    # Set format for PyTorch
    tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=100,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        save_total_limit=2,
    )
    
    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["val"],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save model
    print(f"Saving model to {output_dir}")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    # Evaluate
    print("Evaluating...")
    eval_results = trainer.evaluate()
    print(f"Evaluation results: {eval_results}")
    
    print("Training completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train sentiment analysis model")
    parser.add_argument("--base-model", default="distilbert-base-uncased")
    parser.add_argument("--data-path", default="./data")
    parser.add_argument("--output-dir", default="./models/customer-sentiment-v1")
    parser.add_argument("--num-epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--config", help="Path to config file (optional)")
    
    args = parser.parse_args()
    
    # Load config if provided
    if args.config:
        with open(args.config, "r") as f:
            config = json.load(f)
            args.base_model = config.get("base_model", args.base_model)
            args.data_path = config.get("data_path", args.data_path)
            args.output_dir = config.get("output_dir", args.output_dir)
            args.num_epochs = config.get("num_epochs", args.num_epochs)
            args.batch_size = config.get("batch_size", args.batch_size)
            args.learning_rate = config.get("learning_rate", args.learning_rate)
    
    train(
        base_model=args.base_model,
        data_path=args.data_path,
        output_dir=args.output_dir,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate
    )


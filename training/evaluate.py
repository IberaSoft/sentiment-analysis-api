"""Evaluate trained model."""
import argparse
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from datasets import load_dataset
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_recall_fscore_support,
    confusion_matrix
)


def evaluate(
    model_dir: str,
    test_data: str
):
    """Evaluate model on test data."""
    print(f"Loading model from: {model_dir}")
    
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    
    # Create pipeline
    classifier = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        return_all_scores=True
    )
    
    # Load test data
    print(f"Loading test data from: {test_data}")
    test_dataset = load_dataset("json", data_files=test_data)
    
    if "train" in test_dataset:
        test_data = test_dataset["train"]
    else:
        test_data = test_dataset[list(test_dataset.keys())[0]]
    
    # Get predictions
    print("Running predictions...")
    texts = test_data["text"]
    true_labels = test_data["label"]
    
    predictions = []
    predicted_labels = []
    
    for text in texts:
        result = classifier(text)
        # Get label with highest score
        best_label = max(result[0], key=lambda x: x["score"])
        label_name = best_label["label"].lower()
        
        # Map label name to index
        label_map = {"negative": 0, "neutral": 1, "positive": 2}
        predicted_labels.append(label_map.get(label_name, 1))
        predictions.append(result[0])
    
    # Calculate metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels, average="weighted")
    precision, recall, _, _ = precision_recall_fscore_support(
        true_labels, predicted_labels, average="weighted", zero_division=0
    )
    cm = confusion_matrix(true_labels, predicted_labels)
    
    print("\n" + "="*50)
    print("Evaluation Results")
    print("="*50)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print("\nConfusion Matrix:")
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print(f"Actual Neg  {cm[0]}")
    print(f"       Neu  {cm[1]}")
    print(f"       Pos  {cm[2]}")
    print("="*50)
    
    return {
        "accuracy": accuracy,
        "f1": f1,
        "precision": precision,
        "recall": recall,
        "confusion_matrix": cm.tolist()
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate trained model")
    parser.add_argument("--model-dir", required=True, help="Path to trained model directory")
    parser.add_argument("--test-data", required=True, help="Path to test data JSONL file")
    
    args = parser.parse_args()
    evaluate(args.model_dir, args.test_data)


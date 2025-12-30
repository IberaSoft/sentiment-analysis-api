"""Upload a configured base DistilBERT model as a starting point."""
import argparse
import os
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


def upload_base_model(
    repo_name: str = "IberaSoft/customer-sentiment-analyzer",
    base_model: str = "distilbert-base-uncased",
    token: str = None,
):
    """Upload base model configured for 3-class sentiment to HuggingFace Hub."""
    
    print(f"Loading base model: {base_model}")
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForSequenceClassification.from_pretrained(
        base_model,
        num_labels=3,
        id2label={0: "negative", 1: "neutral", 2: "positive"},
        label2id={"negative": 0, "neutral": 1, "positive": 2}
    )
    
    print(f"Pushing model to HuggingFace Hub: {repo_name}")
    model.push_to_hub(repo_name, token=token)
    tokenizer.push_to_hub(repo_name, token=token)
    
    print(f"✓ Model uploaded to: https://huggingface.co/{repo_name}")
    print("Note: This is the base model configured for 3-class sentiment.")
    print("For production, train on your custom dataset using train_and_upload.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload base model to HuggingFace Hub")
    parser.add_argument("--repo-name", default="IberaSoft/customer-sentiment-analyzer")
    parser.add_argument("--base-model", default="distilbert-base-uncased")
    parser.add_argument("--token", required=True, help="HuggingFace token")
    
    args = parser.parse_args()
    
    upload_base_model(
        repo_name=args.repo_name,
        base_model=args.base_model,
        token=args.token
    )

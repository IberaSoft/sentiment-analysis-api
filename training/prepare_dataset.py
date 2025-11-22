"""Prepare dataset for training."""
import argparse
import json
from pathlib import Path
from datasets import load_dataset, Dataset


def prepare_dataset(
    dataset_name: str = "IberaSoft/ecommerce-reviews-sentiment",
    output_dir: str = "./data",
    train_size: int = 15000,
    val_size: int = 3000,
    test_size: int = 2000
):
    """Prepare dataset splits."""
    print(f"Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name)
    
    # Get the main split (usually 'train')
    if "train" in dataset:
        full_dataset = dataset["train"]
    else:
        # Use the first available split
        full_dataset = dataset[list(dataset.keys())[0]]
    
    # Shuffle dataset
    full_dataset = full_dataset.shuffle(seed=42)
    
    # Split dataset
    total_size = len(full_dataset)
    print(f"Total dataset size: {total_size}")
    
    # Adjust sizes if needed
    if train_size + val_size + test_size > total_size:
        ratio = total_size / (train_size + val_size + test_size)
        train_size = int(train_size * ratio)
        val_size = int(val_size * ratio)
        test_size = total_size - train_size - val_size
        print(f"Adjusted sizes - Train: {train_size}, Val: {val_size}, Test: {test_size}")
    
    # Create splits
    train_dataset = full_dataset.select(range(train_size))
    val_dataset = full_dataset.select(range(train_size, train_size + val_size))
    test_dataset = full_dataset.select(
        range(train_size + val_size, train_size + val_size + test_size)
    )
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save splits
    train_dataset.to_json(str(output_path / "train.jsonl"))
    val_dataset.to_json(str(output_path / "val.jsonl"))
    test_dataset.to_json(str(output_path / "test.jsonl"))
    
    print(f"Dataset prepared successfully!")
    print(f"Train: {len(train_dataset)} samples")
    print(f"Val: {len(val_dataset)} samples")
    print(f"Test: {len(test_dataset)} samples")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare dataset for training")
    parser.add_argument("--dataset-name", default="IberaSoft/ecommerce-reviews-sentiment")
    parser.add_argument("--output-dir", default="./data")
    parser.add_argument("--train-size", type=int, default=15000)
    parser.add_argument("--val-size", type=int, default=3000)
    parser.add_argument("--test-size", type=int, default=2000)
    
    args = parser.parse_args()
    prepare_dataset(
        dataset_name=args.dataset_name,
        output_dir=args.output_dir,
        train_size=args.train_size,
        val_size=args.val_size,
        test_size=args.test_size
    )


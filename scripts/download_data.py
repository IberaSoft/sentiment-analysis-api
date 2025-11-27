"""Download dataset from HuggingFace."""
import argparse
from datasets import load_dataset


def download_data(dataset_name: str = "IberaSoft/ecommerce-reviews-sentiment", output_dir: str = "./data"):
    """Download dataset from HuggingFace."""
    print(f"Downloading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name)
    
    print(f"Dataset downloaded successfully!")
    print(f"Splits available: {list(dataset.keys())}")
    
    for split_name, split_data in dataset.items():
        print(f"{split_name}: {len(split_data)} samples")
    
    return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download dataset from HuggingFace")
    parser.add_argument("--dataset-name", default="IberaSoft/ecommerce-reviews-sentiment")
    parser.add_argument("--output-dir", default="./data")
    
    args = parser.parse_args()
    download_data(args.dataset_name, args.output_dir)


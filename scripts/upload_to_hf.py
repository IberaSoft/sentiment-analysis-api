"""Upload model to HuggingFace Hub."""
import argparse
from pathlib import Path
from huggingface_hub import HfApi, login


def upload_model(
    model_dir: str,
    repo_name: str,
    token: str = None
):
    """Upload model to HuggingFace Hub."""
    model_path = Path(model_dir)
    
    if not model_path.exists():
        raise ValueError(f"Model directory does not exist: {model_dir}")
    
    print(f"Uploading model from {model_dir} to {repo_name}")
    
    # Login if token provided
    if token:
        login(token=token)
    
    # Initialize API
    api = HfApi()
    
    # Create repo if it doesn't exist
    try:
        api.create_repo(repo_id=repo_name, exist_ok=True)
    except Exception as e:
        print(f"Note: {e}")
    
    # Upload model
    api.upload_folder(
        folder_path=str(model_path),
        repo_id=repo_name,
        repo_type="model"
    )
    
    print(f"Model uploaded successfully to: https://huggingface.co/{repo_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload model to HuggingFace Hub")
    parser.add_argument("--model-dir", required=True, help="Path to model directory")
    parser.add_argument("--repo-name", required=True, help="HuggingFace repo name (e.g., username/model-name)")
    parser.add_argument("--token", help="HuggingFace token (optional, can use HF_TOKEN env var)")
    
    args = parser.parse_args()
    upload_model(args.model_dir, args.repo_name, args.token)


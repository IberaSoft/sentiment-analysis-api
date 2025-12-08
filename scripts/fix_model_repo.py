"""Fix model repository by ensuring all necessary files are present."""
import argparse
from pathlib import Path
from huggingface_hub import HfApi, login
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, AutoConfig
import json
import os


def fix_model_repository(
    model_id: str,
    token: str = None
):
    """Ensure model repository has all necessary files."""
    print(f"Fixing model repository: {model_id}")
    
    if token:
        login(token=token)
    
    api = HfApi()
    
    try:
        # Check what files exist
        print("Checking existing files...")
        try:
            files = api.list_repo_files(repo_id=model_id, repo_type="model")
            print(f"Existing files: {files}")
        except Exception as e:
            print(f"Could not list files: {e}")
            files = []
        
        # Download and fix config.json
        print("\n1. Fixing config.json...")
        try:
            config_url = f"https://huggingface.co/{model_id}/resolve/main/config.json"
            import requests
            response = requests.get(config_url)
            
            if response.status_code == 200:
                config = response.json()
                
                # Add model_type if missing
                if "model_type" not in config:
                    print("  Adding model_type: distilbert")
                    config["model_type"] = "distilbert"
                    
                    # Upload fixed config
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(config, f, indent=2)
                        temp_path = f.name
                    
                    try:
                        api.upload_file(
                            path_or_fileobj=temp_path,
                            path_in_repo="config.json",
                            repo_id=model_id,
                            repo_type="model"
                        )
                        print("  ✓ config.json fixed")
                    finally:
                        Path(temp_path).unlink()
                else:
                    print(f"  ✓ config.json already has model_type: {config['model_type']}")
            else:
                print(f"  Warning: Could not download config.json (status {response.status_code})")
        except Exception as e:
            print(f"  Error fixing config.json: {e}")
        
        # Upload tokenizer files from base model if missing
        print("\n2. Checking tokenizer files...")
        tokenizer_files = ["vocab.txt", "tokenizer_config.json"]
        missing_files = []
        
        for file in tokenizer_files:
            if file not in files:
                missing_files.append(file)
        
        if missing_files:
            print(f"  Missing tokenizer files: {missing_files}")
            print("  Downloading tokenizer from base model...")
            
            # Download tokenizer files from base model
            base_model = "distilbert-base-uncased"
            tokenizer = DistilBertTokenizer.from_pretrained(base_model)
            
            # Save tokenizer files temporarily
            import tempfile
            temp_dir = Path(tempfile.mkdtemp())
            
            try:
                tokenizer.save_pretrained(str(temp_dir))
                
                # Upload missing files
                for file in missing_files:
                    local_file = temp_dir / file
                    if local_file.exists():
                        api.upload_file(
                            path_or_fileobj=str(local_file),
                            path_in_repo=file,
                            repo_id=model_id,
                            repo_type="model"
                        )
                        print(f"  ✓ Uploaded {file}")
                    else:
                        print(f"  Warning: {file} not found in tokenizer")
                
                # Also upload special_tokens_map.json if it exists
                special_tokens = temp_dir / "special_tokens_map.json"
                if special_tokens.exists() and "special_tokens_map.json" not in files:
                    api.upload_file(
                        path_or_fileobj=str(special_tokens),
                        path_in_repo="special_tokens_map.json",
                        repo_id=model_id,
                        repo_type="model"
                    )
                    print(f"  ✓ Uploaded special_tokens_map.json")
            finally:
                # Cleanup
                import shutil
                shutil.rmtree(temp_dir)
        else:
            print("  ✓ All tokenizer files present")
        
        print("\n✓ Model repository fixed!")
        print(f"\nModel should now load correctly: {model_id}")
        
    except Exception as e:
        print(f"Error fixing model repository: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix model repository by adding missing files")
    parser.add_argument("--model-id", default="IberaSoft/customer-sentiment-analyzer", help="HuggingFace model ID")
    parser.add_argument("--token", help="HuggingFace token (or set HF_TOKEN env var)")
    
    args = parser.parse_args()
    
    token = args.token or os.getenv("HF_TOKEN")
    if not token:
        print("Warning: No token provided. Some operations may fail if model is private.")
    
    success = fix_model_repository(args.model_id, token)
    
    if success:
        print("\n✓ Done! The model repository now has all necessary files.")
        print("You can now use the model normally without workarounds.")
    else:
        print("\n✗ Failed to fix model repository")
        exit(1)


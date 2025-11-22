"""Optimize model (quantization, ONNX export, etc.)."""
import argparse
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def quantize_model(model_dir: str, output_dir: str):
    """Quantize model to reduce size."""
    print(f"Loading model from: {model_dir}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    
    # Dynamic quantization
    print("Quantizing model...")
    quantized_model = torch.quantization.quantize_dynamic(
        model,
        {torch.nn.Linear},
        dtype=torch.qint8
    )
    
    # Save quantized model
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving quantized model to: {output_dir}")
    quantized_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Compare sizes
    original_size = sum(p.numel() * 4 for p in model.parameters()) / (1024 * 1024)  # MB
    quantized_size = sum(p.numel() for p in quantized_model.parameters()) / (1024 * 1024)  # MB
    
    print(f"\nModel size comparison:")
    print(f"Original: {original_size:.2f} MB")
    print(f"Quantized: {quantized_size:.2f} MB")
    print(f"Reduction: {(1 - quantized_size/original_size)*100:.1f}%")
    
    print("Quantization completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize model")
    parser.add_argument("--model-dir", required=True, help="Path to model directory")
    parser.add_argument("--output-dir", required=True, help="Output directory for optimized model")
    parser.add_argument("--method", default="quantize", choices=["quantize"], help="Optimization method")
    
    args = parser.parse_args()
    
    if args.method == "quantize":
        quantize_model(args.model_dir, args.output_dir)


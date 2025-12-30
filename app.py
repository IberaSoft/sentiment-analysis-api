"""Gradio app for HuggingFace Spaces demo."""
import gradio as gr
from transformers import pipeline
import os

# Initialize model
MODEL_NAME = os.getenv("MODEL_NAME", "IberaSoft/customer-sentiment-analyzer")

# Load model
print(f"Loading model: {MODEL_NAME}")
classifier = None
try:
    # Try to load with token if available (for private models)
    hf_token = os.getenv("HF_TOKEN")
    
    # Use pipeline directly - it handles model loading automatically
    classifier = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        token=hf_token if hf_token else None,
        top_k=None  # Returns all scores
    )
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
    classifier = None


def analyze_sentiment(text):
    """Analyze sentiment of input text."""
    if not text or not text.strip():
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "scores": {"positive": 0.33, "negative": 0.33, "neutral": 0.34}
        }
    
    if classifier is None:
        return {
            "error": "Model not loaded. Please check the logs."
        }
    
    try:
        # Get predictions
        results = classifier(text)
        
        # Process results - handle different label formats
        scores = {}
        label_mapping = {
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral",
            "pos": "positive",
            "neg": "negative",
            "neu": "neutral",
            "POSITIVE": "positive",
            "NEGATIVE": "negative",
            "NEUTRAL": "neutral",
            "LABEL_0": "negative",  # Common HF format
            "LABEL_1": "neutral",
            "LABEL_2": "positive"
        }
        
        for result in results[0]:
            label = result["label"]
            score = result["score"]
            # Normalize label
            normalized_label = label_mapping.get(label, label.lower())
            # Map to standard labels
            if normalized_label not in ["positive", "negative", "neutral"]:
                # Try to infer from label name
                label_lower = label.lower()
                if "pos" in label_lower:
                    normalized_label = "positive"
                elif "neg" in label_lower:
                    normalized_label = "negative"
                else:
                    normalized_label = "neutral"
            
            # Accumulate scores (in case of duplicate labels)
            if normalized_label in scores:
                scores[normalized_label] = max(scores[normalized_label], score)
            else:
                scores[normalized_label] = score
        
        # Ensure all classes are present with default values
        for cls in ["positive", "negative", "neutral"]:
            if cls not in scores:
                scores[cls] = 0.0
        
        # Normalize scores to sum to 1.0
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        
        # Get predicted sentiment (highest score)
        predicted_label = max(scores.items(), key=lambda x: x[1])[0]
        confidence = scores[predicted_label]
        
        return {
            "sentiment": predicted_label,
            "confidence": round(confidence, 4),
            "scores": {
                "positive": round(scores.get("positive", 0.0), 4),
                "negative": round(scores.get("negative", 0.0), 4),
                "neutral": round(scores.get("neutral", 0.0), 4)
            }
        }
    except Exception as e:
        return {
            "error": f"Prediction failed: {str(e)}"
        }


def format_output(result):
    """Format output for display."""
    if "error" in result:
        return f"❌ Error: {result['error']}"
    
    sentiment = result["sentiment"]
    confidence = result["confidence"]
    scores = result["scores"]
    
    # Emoji based on sentiment
    emoji_map = {
        "positive": "😊",
        "negative": "😞",
        "neutral": "😐"
    }
    emoji = emoji_map.get(sentiment, "😐")
    
    output = f"{emoji} **Sentiment: {sentiment.upper()}**\n\n"
    output += f"**Confidence:** {confidence:.2%}\n\n"
    output += "**Score Breakdown:**\n"
    output += f"- Positive: {scores['positive']:.2%}\n"
    output += f"- Negative: {scores['negative']:.2%}\n"
    output += f"- Neutral: {scores['neutral']:.2%}\n"
    
    return output


# Create Gradio interface
# Note: theme parameter moved to launch() in Gradio 6.0, but we keep it here for compatibility
with gr.Blocks(title="Customer Sentiment Analysis") as demo:
    gr.Markdown(
        """
        # 🎭 Customer Sentiment Analysis
        
        Analyze the sentiment of customer reviews using a fine-tuned DistilBERT model.
        
        **Model:** [IberaSoft/customer-sentiment-analyzer](https://huggingface.co/IberaSoft/customer-sentiment-analyzer)
        """
    )
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Enter your text",
                placeholder="Type your customer review here...",
                lines=5,
                max_lines=10
            )
            analyze_btn = gr.Button("Analyze Sentiment", variant="primary")
        
        with gr.Column():
            output = gr.Markdown(label="Result")
    
    # Examples
    gr.Examples(
        examples=[
            ["This product is amazing! I love it so much."],
            ["Terrible experience. Would not recommend."],
            ["It's okay, nothing special but works fine."],
            ["Excellent service and fast delivery. Highly recommend!"],
            ["Poor quality product. Very disappointed."]
        ],
        inputs=text_input
    )
    
    # Event handlers
    analyze_btn.click(
        fn=lambda x: format_output(analyze_sentiment(x)),
        inputs=text_input,
        outputs=output
    )
    
    text_input.submit(
        fn=lambda x: format_output(analyze_sentiment(x)),
        inputs=text_input,
        outputs=output
    )
    
    gr.Markdown(
        """
        ---
        ### About
        This demo uses a fine-tuned DistilBERT model trained on e-commerce customer reviews.
        The model can classify text as **positive**, **negative**, or **neutral** with high accuracy.
        
        **Dataset:** [IberaSoft/ecommerce-reviews-sentiment](https://huggingface.co/datasets/IberaSoft/ecommerce-reviews-sentiment)
        """
    )


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())


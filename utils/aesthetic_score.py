# Aesthetic Score

import torch
import clip
from PIL import Image

# Load model once
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_aesthetic_score(image_path):
    """
    Uses CLIP to compute similarity between image and aesthetic prompts.
    
    Args:
        image_path (str): Path to image file

    Returns:
        dict: {
            'best_prompt': str,
            'score': float,
            'feedback': str
        }
    """
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    # Prompts (can be expanded)
    prompts = [
        "a clean product photo on a white background",
        "a professional studio shot of a product",
        "a blurry low-quality photo",
        "a cluttered messy product photo",
        "a well-lit and sharp product image",
        "an overexposed amateur product photo"
    ]

    text_tokens = clip.tokenize(prompts).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_tokens)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    best_idx = similarity.argmax().item()
    best_prompt = prompts[best_idx]
    score = similarity[0][best_idx].item()

    feedback = {
        0: "Clean and ecommerce-ready image!",
        1: "Looks professional — great studio-like quality.",
        2: "Blurry image. Try stabilizing the camera.",
        3: "Background is distracting. Keep it clean and minimal.",
        4: "Very good lighting and sharpness!",
        5: "Overexposed — reduce lighting or avoid direct flash."
    }.get(best_idx, "Image looks okay, but could be improved.")

    return {
        'best_prompt': best_prompt,
        'score': score,
        'feedback': feedback
    }

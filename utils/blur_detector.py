# Blur Detector

import cv2
import numpy as np

def calculate_blur_score(image, threshold=100.0):
    """
    Calculates the blur score of an image using variance of Laplacian.
    
    Args:
        image (np.ndarray): Input image (BGR or grayscale).
        threshold (float): Threshold to consider image blurry.

    Returns:
        dict: {
            'blur_score': float,
            'is_blurry': bool,
            'feedback': str
        }
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Compute the Laplacian and its variance
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    blur_score = laplacian.var()

    is_blurry = blur_score < threshold

    feedback = (
        "Image appears sharp." if not is_blurry
        else "Image looks blurry. Try using a tripod or better focus."
    )

    return {
        'blur_score': blur_score,
        'is_blurry': is_blurry,
        'feedback': feedback
    }

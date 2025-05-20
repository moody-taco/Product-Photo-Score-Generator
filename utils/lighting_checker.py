# Lighting Checker

import cv2
import numpy as np

def analyze_lighting(image, low_thresh=40, high_thresh=200, dark_pct_limit=0.5, bright_pct_limit=0.5):
    """
    Analyzes lighting quality based on image brightness histogram.

    Args:
        image (np.ndarray): Input image (BGR or grayscale).
        low_thresh (int): Pixel intensity below this is considered dark.
        high_thresh (int): Pixel intensity above this is considered too bright.
        dark_pct_limit (float): Fraction of pixels allowed to be dark before flagging.
        bright_pct_limit (float): Same for overly bright pixels.

    Returns:
        dict: {
            'mean_brightness': float,
            'is_dark': bool,
            'is_bright': bool,
            'feedback': str
        }
    """
    # Convert to grayscale if not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    mean_brightness = np.mean(gray)

    # Calculate histogram-based brightness distribution
    total_pixels = gray.size
    dark_pixels = np.sum(gray < low_thresh)
    bright_pixels = np.sum(gray > high_thresh)

    dark_ratio = dark_pixels / total_pixels
    bright_ratio = bright_pixels / total_pixels

    is_dark = dark_ratio > dark_pct_limit
    is_bright = bright_ratio > bright_pct_limit

    if is_dark:
        feedback = "Image is too dark. Try using better lighting or increasing exposure."
    elif is_bright:
        feedback = "Image is overexposed. Consider reducing brightness or avoiding direct light."
    else:
        feedback = "Lighting looks good."

    return {
        'mean_brightness': mean_brightness,
        'is_dark': is_dark,
        'is_bright': is_bright,
        'feedback': feedback
    }

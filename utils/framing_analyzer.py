# Framing Analyzer

import cv2
import numpy as np

def check_centering(image, margin_ratio=0.2):
    """
    Checks whether the main object in the image is roughly centered.
    
    Args:
        image (np.ndarray): Input BGR image
        margin_ratio (float): Tolerance ratio from center (0.2 = 20%)

    Returns:
        dict: {
            'is_centered': bool,
            'object_center': (x, y),
            'image_center': (x, y),
            'feedback': str
        }
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert if background is light
    if np.mean(gray) > 127:
        thresh = cv2.bitwise_not(thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return {
            'is_centered': False,
            'feedback': 'Could not detect object. Try using a plain background.'
        }

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    object_center = (x + w // 2, y + h // 2)

    img_h, img_w = image.shape[:2]
    image_center = (img_w // 2, img_h // 2)

    # Check distance from center
    margin_w = img_w * margin_ratio
    margin_h = img_h * margin_ratio

    dx = abs(object_center[0] - image_center[0])
    dy = abs(object_center[1] - image_center[1])

    is_centered = dx <= margin_w and dy <= margin_h

    feedback = (
        "Object appears well-centered." if is_centered
        else "Object is off-center. Try positioning it closer to the middle."
    )

    return {
        'is_centered': is_centered,
        'object_center': object_center,
        'image_center': image_center,
        'feedback': feedback
    }

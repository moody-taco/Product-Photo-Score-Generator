# Feedback Generator

def generate_feedback(analysis_results):
    """
    Aggregates individual module results into an overall score and feedback.

    Args:
        analysis_results (dict): Dictionary containing outputs from:
            - blur_detector
            - lighting_checker
            - framing_analyzer
            - aesthetic_score

    Returns:
        dict: {
            'final_score': float (0–100),
            'grade': str (Excellent / Good / Needs Improvement),
            'summary': str
        }
    """

    # Extract and score each component (0–25 points each)
    score = 0
    blur = analysis_results.get('blur', {})
    lighting = analysis_results.get('lighting', {})
    framing = analysis_results.get('framing', {})
    aesthetic = analysis_results.get('aesthetic', {})

    # Blur score (sharp = +25)
    if not blur.get('is_blurry', True):
        score += 25

    # Lighting (good = +25)
    if not lighting.get('is_dark', True) and not lighting.get('is_bright', True):
        score += 25

    # Framing (centered = +20)
    if framing.get('is_centered', False):
        score += 20

    # Aesthetic score (normalized to 30 max)
    aesthetic_confidence = aesthetic.get('score', 0.0)  # range [0,1]
    score += min(aesthetic_confidence * 30, 30)

    # Cap total at 100
    final_score = min(score, 100)

    # Grade label
    if final_score >= 85:
        grade = "Excellent"
    elif final_score >= 60:
        grade = "Good"
    else:
        grade = "Needs Improvement"

    # Combine all feedback into a paragraph
    summary = "\n".join([
        f"- Blur Check: {blur.get('feedback', '')}",
        f"- Lighting: {lighting.get('feedback', '')}",
        f"- Framing: {framing.get('feedback', '')}",
        f"- Aesthetic: {aesthetic.get('feedback', '')}"
    ])

    return {
        'final_score': round(final_score, 1),
        'grade': grade,
        'summary': summary
    }

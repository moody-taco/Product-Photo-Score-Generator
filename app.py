import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

import warnings
warnings.filterwarnings("ignore")

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  
os.environ["PYTHONWARNINGS"] = "ignore" 

from utils.blur_detector import calculate_blur_score
from utils.lighting_checker import analyze_lighting
from utils.framing_analyzer import check_centering
from utils.aesthetic_score import get_aesthetic_score

st.set_page_config(page_title="Smart Product Image Checker", layout="centered")
st.title("🧠 Smart Product Image Checker")
st.caption("Upload your product image to get instant feedback on blur, lighting, framing, and overall aesthetics.")

uploaded_file = st.file_uploader("Upload a product photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Save temporarily for OpenCV + CLIP processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        image.save(temp.name)
        image_path = temp.name

    # Load image with OpenCV
    image_cv = cv2.imread(image_path)

    # Run analysis modules
    with st.spinner("Analyzing image..."):
        blur_result = calculate_blur_score(image_cv)
        lighting_result = analyze_lighting(image_cv)
        framing_result = check_centering(image_cv)
        aesthetic_result = get_aesthetic_score(image_path)

    # Display results
    st.subheader("🔍 Results")

    st.markdown(f"**🟠 Blur Score:** `{blur_result['blur_score']:.2f}`")
    st.markdown(f"**🟠 Lighting:** {lighting_result['feedback']}")
    st.markdown(f"**🟠 Framing:** {framing_result.get('feedback', 'N/A')}")
    st.markdown(f"**🟠 Aesthetic:** {aesthetic_result['feedback']} *(confidence: {aesthetic_result['score']:.2f})*")

    # Generate final score (simple weighted average)
    sharpness_score = min(blur_result["blur_score"] / 100.0, 1.0)  # Normalize
    lighting_penalty = 0.2 if lighting_result["is_dark"] or lighting_result["is_bright"] else 0
    centering_bonus = 0.1 if framing_result.get("is_centered") else 0
    aesthetic_score = aesthetic_result["score"]

    final_score = (sharpness_score + aesthetic_score + centering_bonus - lighting_penalty) / 2
    final_score = max(0, min(final_score, 1))

    st.subheader("📊 Final Verdict")
    st.metric(label="⭐ Overall Image Score", value=f"{final_score*100:.1f} / 100")

    if final_score > 0.85:
        st.success("Great product image! You're ready to post.")
    elif final_score > 0.6:
        st.info("Good image. A few improvements could make it pop.")
    else:
        st.warning("This photo needs work. Check lighting, blur, or background.")

    # Clean up
    os.unlink(image_path)

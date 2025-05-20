# 🧠 Product Photo Score Generator

An AI-powered tool that evaluates product images for quality before you upload them to platforms like Shopee, Lazada, Amazon, or your own store. Get instant feedback on blur, lighting, framing, and aesthetic appeal — all in one click.

---

## 🚀 Features

✅ Detects if your photo is **blurry**  
✅ Checks if **lighting** is too dark or overexposed  
✅ Evaluates if your product is **centered**  
✅ Scores the overall **aesthetic appeal** using OpenAI's CLIP  
✅ Gives a final **score out of 100** with easy-to-understand feedback

---

## 🖼️ Example

Upload your product photo:

> ✨ “Great image! Sharp, well-lit, and professionally framed.”  
> ⚠️ “Image is blurry and overexposed. Try using diffused lighting.”

---

## 🛠️ How It Works

| Module            | Technique                                  |
|-------------------|---------------------------------------------|
| Blur Detection    | Variance of Laplacian (OpenCV)             |
| Lighting Check    | Histogram-based brightness analysis        |
| Framing Check     | Contour analysis + object centering        |
| Aesthetic Scoring | CLIP-based prompt similarity               |

---

## 🧪 Try It Locally

```bash
git clone https://github.com/moody-taco/product-photo-score-generator.git
cd smart-product-image-checker
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 File Structure

```
Product-Photo-Score-Generator/
├── app.py                  
├── utils/
│   ├── blur_detector.py
│   ├── lighting_checker.py
│   ├── framing_analyzer.py
│   ├── aesthetic_score.py
│   └── feedback_generator.py
├── assets/
│   └── sample_images/
├── requirements.txt
└── README.md
```

---


## 💡 Use Cases

- Online sellers and small businesses  
- Inexperienced product photographers  
- Marketplace listing QA tools  
- UX researchers building photo recommendation systems

---

## 📚 References

- [OpenAI CLIP](https://github.com/openai/CLIP)  
- [OpenCV Documentation](https://docs.opencv.org/)  
- [Streamlit Docs](https://docs.streamlit.io/)

import os
import re
import joblib
import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="Fake News Detector | BSc. CSIT Project",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Load CSS & JS Files (Separated Architecture)
CSS_PATH = os.path.join("static", "css", "style.css")
JS_PATH = os.path.join("static", "js", "script.js")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if os.path.exists(JS_PATH):
    with open(JS_PATH, "r", encoding="utf-8") as f:
        components.html(f"<script>{f.read()}</script>", height=0, width=0)


# Load Machine Learning Model & Vectorizer
@st.cache_resource
def load_ml_assets():
    try:
        vec = joblib.load("vectorizer.jb")
        mdl = joblib.load("lr_model.jb")
        return vec, mdl
    except Exception as e:
        st.error(f"Error loading model assets: {e}")
        return None, None


vectorization, model = load_ml_assets()


# Text Preprocessing Function (Regex NLP Cleaning matching training pipeline)
def wordopt(text: str) -> str:
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d", "", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Initialize Session State
if "news_text" not in st.session_state:
    st.session_state["news_text"] = ""

# UI Header Section
st.markdown(
    """
<div class="app-header">
    <div class="header-title-group">
        <h1>📰 Fake News Detection System</h1>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Main Input Form Section
st.markdown("### Analyze News Article")
st.markdown(
    "Paste the headline or full content of the news article below to check its authenticity."
)


def clear_text():
    if "news_text" in st.session_state:
        st.session_state["news_text"] = ""


# Textarea Input
st.text_area(
    label="News Text Input",
    key="news_text",
    height=180,
    placeholder="Enter news text here...",
    label_visibility="collapsed",
)
user_input = st.session_state["news_text"]

# Counter bar
char_count = len(user_input)
word_count = len(user_input.strip().split()) if user_input.strip() else 0

st.markdown(
    f"""
<div class="counter-bar">
    <span>Characters: <strong id="js-char-count">{char_count}</strong></span>
    <span>Words: <strong id="js-word-count">{word_count}</strong></span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Submit Predict & Clear Buttons side by side
col_clear_btn, col_predict = st.columns(2)
with col_clear_btn:
    st.button("Clear text", use_container_width=True, on_click=clear_text)

with col_predict:
    btn_predict = st.button(
        "Check Authenticity", type="primary", use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# Prediction Processing & Result Card
if btn_predict:
    if not user_input.strip():
        st.warning("Please enter some news article to analyze.")
    elif model is None or vectorization is None:
        st.error("Machine Learning model assets failed to load.")
    else:
        with st.spinner("Analyzing text features and running classification model..."):
            # Preprocess & Vectorize
            cleaned_text = wordopt(user_input)
            if not cleaned_text:
                cleaned_text = user_input.lower()

            transformed_input = vectorization.transform([cleaned_text])
            prediction = model.predict(transformed_input)[0]

            # Get Confidence Probabilities if available
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(transformed_input)[0]
                fake_prob = round(float(probs[0]) * 100, 1)
                real_prob = round(float(probs[1]) * 100, 1)
            else:
                fake_prob = 0.0 if prediction == 1 else 100.0
                real_prob = 100.0 if prediction == 1 else 0.0

            # Render Results
            if prediction == 1:
                st.markdown(
                    f"""
                <div class="result-card real-news">
                    <div class="result-header">
                        <div class="result-icon">✓</div>
                        <h2 class="result-title">Verdict: REAL NEWS</h2>
                    </div>
                    <p class="result-detail">
                        The model classifies this news article as <strong>Genuine / Authentic</strong> with 
                        <strong>{real_prob}%</strong> confidence probability.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="result-card fake-news">
                    <div class="result-header">
                        <div class="result-icon">✕</div>
                        <h2 class="result-title">Verdict: FAKE NEWS</h2>
                    </div>
                    <p class="result-detail">
                        The model classifies this news article as <strong>Deceptive / Misinformation</strong> with 
                        <strong>{fake_prob}%</strong> confidence probability.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Detailed metrics breakdown
            with st.expander(
                "📊 View Detailed Probability Breakdown & Preprocessed Text"
            ):
                st.progress(
                    real_prob / 100.0, text=f"Real News Probability: {real_prob}%"
                )
                st.progress(
                    fake_prob / 100.0, text=f"Fake News Probability: {fake_prob}%"
                )
                st.markdown("**NLP Cleaned Text (`wordopt` output):**")
                st.code(cleaned_text if cleaned_text else "None", language="text")

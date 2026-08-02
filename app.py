import os
import re
import joblib
import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Load CSS & JS Files (Separated Architecture)
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "model")
CSS_PATH = os.path.join(BASE_DIR, "static", "css", "style.css")
JS_PATH = os.path.join(BASE_DIR, "static", "js", "script.js")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if os.path.exists(JS_PATH):
    with open(JS_PATH, "r", encoding="utf-8") as f:
        components.html(f"<script>{f.read()}</script>", height=0, width=0)

# Model Mapping Dictionary
MODEL_FILES = {
    "Logistic Regression": os.path.join(MODEL_DIR, "lr_model.jb"),
    "Decision Tree": os.path.join(MODEL_DIR, "dtc_model.jb"),
    "Gradient Boosting": os.path.join(MODEL_DIR, "gbc_model.jb"),
    "Random Forest": os.path.join(MODEL_DIR, "rfc_model.jb"),
}


# Load Vectorizer once
@st.cache_resource
def load_vectorizer():
    try:
        return joblib.load(os.path.join(MODEL_DIR, "vectorizer.jb"))
    except Exception as e:
        st.error(f"Error loading vectorizer: {e}")
        return None


# Load Model dynamically based on selection
@st.cache_resource
def load_model(filename: str):
    try:
        return joblib.load(filename)
    except Exception as e:
        st.error(f"Error loading model ({filename}): {e}")
        return None


vectorization = load_vectorizer()


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

# Main Input Form Section Header Row: Title on Left, Small Algorithm Dropdown on Right
col_title, col_algo = st.columns([1.6, 0.5], vertical_alignment="center")

with col_title:
    st.markdown("### Analyze News Article")

with col_algo:
    selected_algorithm = st.selectbox(
        "Algorithm Selector",
        options=list(MODEL_FILES.keys()),
        index=0,
        label_visibility="collapsed",
        help="Select classification algorithm",
    )

st.markdown(
    "Paste the headline or full content of the news article below to check its authenticity."
)

# Load selected model
model = load_model(MODEL_FILES[selected_algorithm])


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
        with st.spinner(f"Analyzing text features using {selected_algorithm}..."):
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
                        The <strong>{selected_algorithm}</strong> model classifies this news article as <strong>Genuine / Authentic</strong> with 
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
                        The <strong>{selected_algorithm}</strong> model classifies this news article as <strong>Deceptive / Misinformation</strong> with 
                        <strong>{fake_prob}%</strong> confidence probability.
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Detailed metrics breakdown
            with st.expander(
                f"📊 View Detailed Breakdown ({selected_algorithm}) & Preprocessed Text"
            ):
                st.progress(
                    real_prob / 100.0, text=f"Real News Probability: {real_prob}%"
                )
                st.progress(
                    fake_prob / 100.0, text=f"Fake News Probability: {fake_prob}%"
                )
                st.markdown("**NLP Cleaned Text (`wordopt` output):**")
                st.code(cleaned_text if cleaned_text else "None", language="text")

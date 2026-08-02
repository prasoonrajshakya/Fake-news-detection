# 📰 Fake News Detection System

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

An Artificial Intelligence & Machine Learning project built for **BSc. CSIT 4th Semester (AI Subject)**. This system detects whether a news article is real or fake using Natural Language Processing (NLP) text preprocessing, TF-IDF feature extraction, and multiple machine learning classifiers. The project now also includes a Streamlit web interface for real-time prediction and result visualization.

---

## 📌 Table of Contents
- [About the Project](#-about-the-project)
- [Dataset Details](#-dataset-details)
- [Tech Stack & Libraries](#-tech-stack--libraries)
- [Project Workflow](#-project-workflow)
- [Model Performance & Results](#-model-performance--results)
- [Installation & Setup](#-installation--setup)
- [Project Structure](#-project-structure)
- [Roadmap & Upcoming Features](#-roadmap--upcoming-features)
- [Author](#-author)

---

## 🎯 About the Project

In the digital era, the rapid spread of misinformation and fake news poses significant challenges to society. This project aims to build an automated machine learning classification model capable of distinguishing between legitimate and deceptive news articles based on textual features.

---

## 📊 Dataset Details

The model is trained and evaluated using combined datasets:
1. **True.csv**: Genuine news articles.
2. **Fake.csv**: Fake/fabricated news articles.
3. **FA-KES-Dataset.csv**: Additional dataset of fake and real news for broader generalization.

These datasets are merged and labeled to build a binary classification system for distinguishing between real and fake news content.

---

## 🛠️ Tech Stack & Libraries

- **Programming Language**: Python
- **Environment**: Jupyter Notebook + Streamlit Web App
- **Data Handling**: `pandas`, `numpy`
- **Text Processing / NLP**: `re` (Regular Expressions)
- **Machine Learning**: `scikit-learn` (`TfidfVectorizer`, `LogisticRegression`, `DecisionTreeClassifier`, `RandomForestClassifier`, `GradientBoostingClassifier`, `train_test_split`, `classification_report`)
- **Model Serialization**: `joblib`
- **Web Interface**: `streamlit`

---

## 🔄 Project Workflow

1. **Data Collection & Merging**: Concatenating real and fake news datasets with proper binary labels (`1` for Real, `0` for Fake).
2. **Data Cleaning & Preprocessing**:
   - Converting text to lowercase.
   - Removing URLs (`http/https`) and HTML tags.
   - Removing punctuation marks, symbols, digits, and newline characters.
3. **Feature Extraction (TF-IDF)**:
   - Vectorizing cleaned text into numerical feature vectors using `TfidfVectorizer`.
4. **Train-Test Split**:
   - Splitting data into 70% training set and 30% testing set.
5. **Model Training & Evaluation**:
   - Training classification models.
   - Evaluating performance using Accuracy Score, Precision, Recall, and F1-Score.
6. **Web Application Deployment**:
   - Loading the saved vectorizer and trained model in `app.py`.
   - Accepting user input from the Streamlit interface and predicting the label in real time.

---

## 📈 Model Performance & Results

- **Primary Model**: Logistic Regression
- **Achieved Accuracy**: **98% (0.98)**
- **Train-Test Split**: 70:30 ratio
- **Evaluation Metrics**: Precision, Recall, F1-Score, and Support via `classification_report`

---

## 🚀 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ignotus-8/Fake-news-detection.git
   cd Fake-news-detection
   ```

2. **Set up Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Web App**:
   ```bash
   streamlit run app.py
   ```

5. **Optional**: Run the Jupyter Notebook for training and experimentation:
   ```bash
   jupyter notebook "Fake-news detection.ipynb"
   ```

---

## 📁 Project Structure

```
├── app.py                      # Streamlit web application for live fake news classification
├── Fake-news detection.ipynb   # Main Jupyter notebook containing data preprocessing & model training
├── dataset/
│   ├── FA-KES-Dataset.csv      # Secondary dataset of news articles
│   ├── Fake.csv                # Dataset containing fake news samples
│   └── True.csv                # Dataset containing genuine news samples
├── model/
│   ├── dtc_model.jb            # Decision Tree classifier
│   ├── gbc_model.jb            # Gradient Boosting classifier
│   ├── lr_model.jb             # Logistic Regression classifier
│   ├── rfc_model.jb            # Random Forest classifier
│   └── vectorizer.jb           # TF-IDF vectorizer used for preprocessing
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Ignored files (e.g., venv, checkpoints)
```

---

## 🔮 Roadmap & Upcoming Features

- [x] Data cleaning, preprocessing & regex normalization
- [x] Feature extraction with TF-IDF Vectorizer
- [x] Baseline Logistic Regression model (~98% accuracy)
- [x] Evaluate additional ML algorithms (Decision Tree, Random Forest, Gradient Boosting)
- [x] Develop an interactive Web Interface (Streamlit) for real-time news verification

---

## 👤 Author

Developed by **[@ignotus-8](https://github.com/ignotus-8)** for BSc. CSIT 4th Semester (AI Subject).

# 🩺 Multiple Disease Prediction System

An end-to-end Machine Learning web application that predicts the likelihood of multiple diseases using trained Machine Learning models. The application provides an interactive interface built with Streamlit and allows users to select a disease, enter the required medical parameters, and receive a prediction instantly.

The project currently supports:

- 🩸 Diabetes Prediction
- ❤️ Heart Disease Prediction
- 🧠 Parkinson's Disease Prediction

The trained models are serialized and integrated into a Streamlit application for real-time inference.

---

## 🚀 Live Demo

🌐 **Streamlit App:**  
https://multiple-disease-prediction-2e8vrv2rymtnu8sjrfq7gf.streamlit.app/

---

## 📌 Project Overview

The goal of this project is to build a simple and interactive Machine Learning application that demonstrates how trained ML models can be integrated into a user-facing web application.

Instead of training the models every time the application starts, the trained models are saved as `.sav` files and loaded directly by the Streamlit application.

### Workflow

```text
Medical Dataset
       │
       ▼
Data Preprocessing
       │
       ▼
Model Training
       │
       ▼
Trained ML Model
       │
       ▼
Model Serialization (.sav)
       │
       ▼
Streamlit Application
       │
       ▼
User Input
       │
       ▼
Model Prediction
       │
       ▼
Prediction Result

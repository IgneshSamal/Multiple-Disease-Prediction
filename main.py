# -*- coding: utf-8 -*-
"""
Multiple Disease Prediction System
Author: ignes
Redesigned: Premium ML Health Assistant
"""

import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedPredict AI",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

  /* ── Base reset ── */
  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0A0F1C;
    color: #E8F0FE;
  }

  .stApp {
    background: linear-gradient(135deg, #0A0F1C 0%, #0D1626 60%, #0A1A2E 100%);
  }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060B14 0%, #0D1626 100%);
    border-right: 1px solid rgba(0, 212, 200, 0.15);
  }

  section[data-testid="stSidebar"] * {
    color: #E8F0FE !important;
  }

  /* ── Sidebar logo area ── */
  .sidebar-logo {
    text-align: center;
    padding: 28px 16px 20px;
    border-bottom: 1px solid rgba(0, 212, 200, 0.12);
    margin-bottom: 12px;
  }
  .sidebar-logo .logo-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 6px;
    filter: drop-shadow(0 0 12px rgba(0, 212, 200, 0.6));
  }
  .sidebar-logo .logo-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #00D4C8 !important;
    letter-spacing: 0.03em;
  }
  .sidebar-logo .logo-sub {
    font-size: 0.72rem;
    color: #5E7A9A !important;
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* ── Page hero header ── */
  .page-hero {
    background: linear-gradient(90deg, rgba(0,212,200,0.08) 0%, rgba(0,212,200,0.02) 100%);
    border: 1px solid rgba(0, 212, 200, 0.18);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
  }
  .page-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00D4C8, #0077FF, #00D4C8);
    background-size: 200% 100%;
    animation: pulse-bar 3s ease-in-out infinite;
  }
  @keyframes pulse-bar {
    0%, 100% { background-position: 0% 50%; }
    50%       { background-position: 100% 50%; }
  }
  .page-hero .hero-badge {
    display: inline-block;
    background: rgba(0, 212, 200, 0.12);
    border: 1px solid rgba(0, 212, 200, 0.35);
    color: #00D4C8;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
  }
  .page-hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E8F0FE;
    margin: 0 0 8px;
    line-height: 1.2;
  }
  .page-hero h1 span {
    color: #00D4C8;
  }
  .page-hero p {
    color: #7A9BB5;
    font-size: 0.9rem;
    font-weight: 300;
    margin: 0;
    max-width: 600px;
  }
  .hero-icon {
    position: absolute;
    right: 36px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.12;
  }

  /* ── Section label ── */
  .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    color: #00D4C8;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 20px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0, 212, 200, 0.12);
  }

  /* ── Input card group ── */
  .input-group-card {
    background: rgba(14, 22, 40, 0.8);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 24px 24px 8px;
    margin-bottom: 20px;
    backdrop-filter: blur(8px);
  }
  .input-group-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    color: #5E7A9A;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 16px;
  }

  /* ── Streamlit inputs override ── */
  .stTextInput > label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: #7A9BB5 !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 4px !important;
  }

  .stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #E8F0FE !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
  }

  .stTextInput > div > div > input:focus {
    border-color: #00D4C8 !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 200, 0.12) !important;
    outline: none !important;
  }

  /* ── Primary button ── */
  .stButton > button {
    background: linear-gradient(135deg, #00D4C8 0%, #0077FF 100%) !important;
    color: #0A0F1C !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 36px !important;
    width: 100% !important;
    margin-top: 16px !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 20px rgba(0, 212, 200, 0.25) !important;
  }

  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0, 212, 200, 0.4) !important;
  }

  .stButton > button:active {
    transform: translateY(0) !important;
  }

  /* ── Result banners ── */
  .result-positive {
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.15) 0%, rgba(255, 71, 87, 0.05) 100%);
    border: 1px solid rgba(255, 71, 87, 0.4);
    border-left: 4px solid #FF4757;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 24px;
    animation: fade-in 0.4s ease;
  }
  .result-negative {
    background: linear-gradient(135deg, rgba(0, 212, 200, 0.12) 0%, rgba(0, 212, 200, 0.03) 100%);
    border: 1px solid rgba(0, 212, 200, 0.35);
    border-left: 4px solid #00D4C8;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 24px;
    animation: fade-in 0.4s ease;
  }
  @keyframes fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .result-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .result-positive .result-label { color: #FF4757; }
  .result-negative .result-label { color: #00D4C8; }
  .result-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #E8F0FE;
    margin: 0;
  }
  .result-sub {
    font-size: 0.78rem;
    color: #5E7A9A;
    margin-top: 6px;
  }

  /* ── Stat pills ── */
  .stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 28px;
    flex-wrap: wrap;
  }
  .stat-pill {
    background: rgba(0, 212, 200, 0.06);
    border: 1px solid rgba(0, 212, 200, 0.18);
    border-radius: 8px;
    padding: 10px 18px;
    flex: 1;
    min-width: 130px;
  }
  .stat-pill .stat-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #00D4C8;
  }
  .stat-pill .stat-lbl {
    font-size: 0.7rem;
    color: #5E7A9A;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
  }

  /* ── Disclaimer ── */
  .disclaimer {
    background: rgba(255, 193, 7, 0.06);
    border: 1px solid rgba(255, 193, 7, 0.2);
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 28px;
    font-size: 0.75rem;
    color: #8A7A5A;
    line-height: 1.6;
  }
  .disclaimer strong { color: #FFC107; }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }

  /* ── Option menu override ── */
  .nav-link {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
  }
  .nav-link.active {
    background: rgba(0, 212, 200, 0.15) !important;
    color: #00D4C8 !important;
  }
</style>
""", unsafe_allow_html=True)


# ── Model loading ─────────────────────────────────────────────────────────────
working_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_models():
    base = 'D:/Project 1 - Multiple Disease Prediction/multiple-disease-prediction-streamlit-app/saved_models/'
    return {
        'diabetes':      pickle.load(open(base + 'diabetes_model.sav', 'rb')),
        'heart_disease': pickle.load(open(base + 'heart_disease_model.sav', 'rb')),
        'parkinsons':    pickle.load(open(base + 'parkinsons_model.sav', 'rb')),
    }

models = load_models()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <span class="logo-icon">🧬</span>
      <div class="logo-title">MedPredict AI</div>
      <div class="logo-sub">Clinical ML Suite · v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=['Diabetes', 'Heart Disease', "Parkinson's"],
        icons=['droplet-fill', 'heart-pulse-fill', 'person-fill-gear'],
        default_index=0,
        styles={
            "container":      {"padding": "0", "background-color": "transparent"},
            "icon":           {"color": "#00D4C8", "font-size": "16px"},
            "nav-link":       {
                "font-size": "0.85rem", "color": "#7A9BB5",
                "padding": "10px 16px", "border-radius": "8px",
                "margin-bottom": "4px", "font-family": "'IBM Plex Sans', sans-serif"
            },
            "nav-link-selected": {
                "background-color": "rgba(0, 212, 200, 0.1)",
                "color": "#00D4C8", "font-weight": "600"
            },
        },
    )

    st.markdown("""
    <div style="position:absolute; bottom:24px; left:16px; right:16px;">
      <div style="font-size:0.68rem; color:#2E4060; text-align:center; line-height:1.6;">
        Models trained on clinical datasets.<br>
        For research & portfolio use only.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Helper: render result banner ──────────────────────────────────────────────
def show_result(positive: bool, positive_msg: str, negative_msg: str, positive_sub: str, negative_sub: str):
    if positive:
        st.markdown(f"""
        <div class="result-positive">
          <div class="result-label">⚠ Prediction Result</div>
          <p class="result-text">{positive_msg}</p>
          <p class="result-sub">{positive_sub}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-negative">
          <div class="result-label">✓ Prediction Result</div>
          <p class="result-text">{negative_msg}</p>
          <p class="result-sub">{negative_sub}</p>
        </div>
        """, unsafe_allow_html=True)


def disclaimer():
    st.markdown("""
    <div class="disclaimer">
      <strong>⚕ Clinical Disclaimer</strong> — This tool uses machine learning models trained on
      publicly available datasets. Predictions are probabilistic and intended for
      <strong>research and educational purposes only</strong>.
      Always consult a licensed medical professional for clinical decisions.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DIABETES
# ══════════════════════════════════════════════════════════════════════════════
if selected == 'Diabetes':

    st.markdown("""
    <div class="page-hero">
      <div class="hero-badge">Model · SVM Classifier</div>
      <h1>Diabetes <span>Risk Prediction</span></h1>
      <p>Enter the patient's clinical measurements below. The model evaluates eight biomarkers
         to predict the likelihood of Type-2 Diabetes Mellitus.</p>
      <span class="hero-icon">💉</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-pill"><div class="stat-val">768</div><div class="stat-lbl">Training Samples</div></div>
      <div class="stat-pill"><div class="stat-val">8</div><div class="stat-lbl">Biomarkers</div></div>
      <div class="stat-pill"><div class="stat-val">~77%</div><div class="stat-lbl">Accuracy</div></div>
      <div class="stat-pill"><div class="stat-val">PIMA</div><div class="stat-lbl">Dataset</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">— Patient Biomarkers</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Reproductive & Metabolic</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: Pregnancies = st.text_input('Pregnancies', placeholder='e.g. 2')
    with c2: Glucose = st.text_input('Plasma Glucose (mg/dL)', placeholder='e.g. 120')
    with c3: BMI = st.text_input('BMI (kg/m²)', placeholder='e.g. 28.5')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Vascular & Endocrine</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: BloodPressure = st.text_input('Diastolic BP (mmHg)', placeholder='e.g. 72')
    with c2: Insulin = st.text_input('2-hr Serum Insulin (μU/mL)', placeholder='e.g. 85')
    with c3: DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', placeholder='e.g. 0.627')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Body Composition & Demographics</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: SkinThickness = st.text_input('Triceps Skin Fold Thickness (mm)', placeholder='e.g. 20')
    with c2: Age = st.text_input('Age (years)', placeholder='e.g. 33')
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button('Run Diabetes Prediction →'):
        try:
            user_input = [float(x) for x in [
                Pregnancies, Glucose, BloodPressure, SkinThickness,
                Insulin, BMI, DiabetesPedigreeFunction, Age
            ]]
            pred = models['diabetes'].predict([user_input])[0]
            show_result(
                pred == 1,
                positive_msg="High likelihood of Diabetes Mellitus detected.",
                negative_msg="No significant markers for Diabetes detected.",
                positive_sub="Recommend fasting blood glucose confirmation test and endocrinologist referral.",
                negative_sub="Continue regular metabolic screening annually, especially post-45 years."
            )
        except ValueError:
            st.error("⚠ Please fill in all fields with valid numeric values before running the prediction.")

    disclaimer()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HEART DISEASE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == 'Heart Disease':

    st.markdown("""
    <div class="page-hero">
      <div class="hero-badge">Model · Logistic Regression</div>
      <h1>Heart Disease <span>Detection</span></h1>
      <p>Input 13 cardiovascular parameters. The model identifies patterns associated with
         coronary artery disease using the Cleveland Heart Disease dataset.</p>
      <span class="hero-icon">🫀</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-pill"><div class="stat-val">303</div><div class="stat-lbl">Training Samples</div></div>
      <div class="stat-pill"><div class="stat-val">13</div><div class="stat-lbl">Features</div></div>
      <div class="stat-pill"><div class="stat-val">~85%</div><div class="stat-lbl">Accuracy</div></div>
      <div class="stat-pill"><div class="stat-val">UCI</div><div class="stat-lbl">Dataset</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">— Cardiovascular Parameters</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Demographics</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: age = st.text_input('Age (years)', placeholder='e.g. 54', key='hd_age')
    with c2: sex = st.text_input('Sex (1 = Male, 0 = Female)', placeholder='e.g. 1')
    with c3: cp = st.text_input('Chest Pain Type (0–3)', placeholder='0=typical, 3=asymptomatic')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Blood & Lipid Panel</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: trestbps = st.text_input('Resting BP (mmHg)', placeholder='e.g. 130')
    with c2: chol = st.text_input('Serum Cholesterol (mg/dL)', placeholder='e.g. 250')
    with c3: fbs = st.text_input('Fasting Blood Sugar >120 mg/dL (1=Yes)', placeholder='0 or 1')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Cardiac Function</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: restecg = st.text_input('Resting ECG (0–2)', placeholder='e.g. 0')
    with c2: thalach = st.text_input('Max Heart Rate Achieved', placeholder='e.g. 150')
    with c3: exang = st.text_input('Exercise-Induced Angina (1=Yes)', placeholder='0 or 1')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">ST Segment & Vessels</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: oldpeak = st.text_input('ST Depression', placeholder='e.g. 1.5')
    with c2: slope = st.text_input('ST Slope (0–2)', placeholder='e.g. 1')
    with c3: ca = st.text_input('Major Vessels (0–3)', placeholder='e.g. 0')
    with c4: thal = st.text_input('Thalassemia (0–2)', placeholder='0=normal, 2=reversible')
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button('Run Heart Disease Prediction →'):
        try:
            user_input = [float(x) for x in [
                age, sex, cp, trestbps, chol, fbs,
                restecg, thalach, exang, oldpeak, slope, ca, thal
            ]]
            pred = models['heart_disease'].predict([user_input])[0]
            show_result(
                pred == 1,
                positive_msg="Indicators of coronary artery disease detected.",
                negative_msg="No significant cardiac disease markers detected.",
                positive_sub="Recommend ECG stress test, echocardiogram, and cardiology consultation.",
                negative_sub="Maintain heart-healthy lifestyle; re-screen at next annual physical."
            )
        except ValueError:
            st.error("⚠ Please fill in all 13 fields with valid numeric values before running the prediction.")

    disclaimer()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PARKINSON'S
# ══════════════════════════════════════════════════════════════════════════════
elif selected == "Parkinson's":

    st.markdown("""
    <div class="page-hero">
      <div class="hero-badge">Model · SVM · Voice Biomarker Analysis</div>
      <h1>Parkinson's <span>Disease Prediction</span></h1>
      <p>Provide 22 sustained phonation (voice recording) features. The model detects
         dysphonia patterns that are early indicators of Parkinson's disease.</p>
      <span class="hero-icon">🧠</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-pill"><div class="stat-val">195</div><div class="stat-lbl">Training Samples</div></div>
      <div class="stat-pill"><div class="stat-val">22</div><div class="stat-lbl">Voice Features</div></div>
      <div class="stat-pill"><div class="stat-val">~87%</div><div class="stat-lbl">Accuracy</div></div>
      <div class="stat-pill"><div class="stat-val">Oxford</div><div class="stat-lbl">Dataset</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">— Vocal Biomarker Features</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Fundamental Frequency (Hz)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: fo = st.text_input('MDVP: Fo — Avg Vocal Freq', placeholder='e.g. 119.99')
    with c2: fhi = st.text_input('MDVP: Fhi — Max Vocal Freq', placeholder='e.g. 157.30')
    with c3: flo = st.text_input('MDVP: Flo — Min Vocal Freq', placeholder='e.g. 74.99')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Jitter Measures (Frequency Variation)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: Jitter_percent = st.text_input('Jitter %', placeholder='e.g. 0.00784')
    with c2: Jitter_Abs = st.text_input('Jitter Abs', placeholder='e.g. 0.00007')
    with c3: RAP = st.text_input('MDVP: RAP', placeholder='e.g. 0.00370')
    with c4: PPQ = st.text_input('MDVP: PPQ', placeholder='e.g. 0.00554')
    with c5: DDP = st.text_input('Jitter: DDP', placeholder='e.g. 0.01109')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Shimmer Measures (Amplitude Variation)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: Shimmer = st.text_input('MDVP: Shimmer', placeholder='e.g. 0.0954')
    with c2: Shimmer_dB = st.text_input('Shimmer (dB)', placeholder='e.g. 0.868')
    with c3: APQ3 = st.text_input('APQ3', placeholder='e.g. 0.0470')
    with c4: APQ5 = st.text_input('APQ5', placeholder='e.g. 0.0578')
    with c5: APQ = st.text_input('MDVP: APQ', placeholder='e.g. 0.0799')
    c1, c2 = st.columns(2)
    with c1: DDA = st.text_input('Shimmer: DDA', placeholder='e.g. 0.141')
    with c2: NHR = st.text_input('NHR — Noise-to-Harmonics', placeholder='e.g. 0.0127')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-group-card"><div class="input-group-title">Nonlinear Dynamics & Signal Complexity</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: HNR = st.text_input('HNR', placeholder='e.g. 21.03')
    with c2: RPDE = st.text_input('RPDE', placeholder='e.g. 0.4144')
    with c3: DFA = st.text_input('DFA', placeholder='e.g. 0.8154')
    with c4: spread1 = st.text_input('spread1', placeholder='e.g. -4.813')
    with c5: spread2 = st.text_input('spread2', placeholder='e.g. 0.2665')
    c1, c2 = st.columns(2)
    with c1: D2 = st.text_input('D2 — Correlation Dimension', placeholder='e.g. 2.301')
    with c2: PPE = st.text_input('PPE — Pitch Period Entropy', placeholder='e.g. 0.2842')
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Run Parkinson's Prediction →"):
        try:
            user_input = [float(x) for x in [
                fo, fhi, flo, Jitter_percent, Jitter_Abs,
                RAP, PPQ, DDP, Shimmer, Shimmer_dB,
                APQ3, APQ5, APQ, DDA, NHR, HNR,
                RPDE, DFA, spread1, spread2, D2, PPE
            ]]
            pred = models['parkinsons'].predict([user_input])[0]
            show_result(
                pred == 1,
                positive_msg="Dysphonia patterns consistent with Parkinson's disease detected.",
                negative_msg="Vocal biomarkers within normal ranges — no Parkinson's indicators.",
                positive_sub="Recommend DaTscan neuroimaging and neurologist evaluation.",
                negative_sub="Voice-based screening negative; continue routine neurological monitoring."
            )
        except ValueError:
            st.error("⚠ Please fill in all 22 fields with valid numeric values before running the prediction.")

    disclaimer()

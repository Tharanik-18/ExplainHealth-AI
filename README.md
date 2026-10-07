# ExplainHealth AI

### Conversational Multi-Disease Interpretable Machine Learning System

**ExplainHealth AI** is a production-style final-year machine learning and Explainable AI (XAI) healthcare risk-analysis system. It integrates five specialized disease-risk modules (Diabetes, Heart Disease, Breast Cancer, Lung Cancer, Stroke) trained on legitimate public healthcare datasets with local SHAP feature attributions, counterfactual what-if simulations, uncertainty detection, multi-model disagreement analysis, and a multilingual conversational interface (English, Tamil, Tanglish).

---

## 🏗️ 1. Architecture Overview (ML-First Design)

```
User (English / Tamil / Tanglish)
  ↓
Chat Interface (React / Next.js Dashboard)
  ↓
Conversation & Natural Language Slot Extraction (English / Tanglish)
  ↓
Input Reliability Check & OOD Detector (Hard Schema & 3xIQR Training Bounds)
  ↓
Disease Router (Diabetes, Heart, Breast Cancer, Lung Cancer, Stroke)
  ↓
Disease Preprocessing Pipeline (ColumnTransformer - Zero Data Leakage)
  ↓
Calibrated Machine Learning Model (Logistic Regression / Random Forest / XGBoost / LightGBM)
  ↓
Probability Calibration (Platt Sigmoid / Isotonic Regression)
  ↓
SHAP Explainability Engine (Local Feature Contributions: Why & Why Not)
  ↓
Counterfactual Engine ("What Would Change the Prediction?")
  ↓
Model Disagreement Engine (Multi-Architecture Variance Analysis)
  ↓
Personal Health Timeline & Multi-Disease Risk Profile Service
  ↓
Response Generator & Clinical Triage Layer
```

> **Strict Anti-Hallucination Protocol**: The LLM/chatbot layer handles only natural-language understanding, slot extraction, multilingual conversion, and natural language formatting. All disease risk probabilities, SHAP values, and counterfactuals are strictly calculated by real trained ML models and XAI engines.

---

## 🌟 2. Seven Novel Features

1. **Counterfactual Explanation Engine ("What Would Change the Prediction?")**: Mathematically searches for minimal perturbations in actionable patient features (BMI, Glucose, BP, Cholesterol, Smoking) while holding immutable features (Age, Sex, Genetics) constant to lower model risk estimates. Clearly framed as a mathematical simulation, not medical advice.
2. **Model Disagreement Engine**: Runs all trained candidate model families (Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM) on identical patient inputs, calculating spread and flagging architectural sensitivity.
3. **Prediction Uncertainty & Confidence Tiers**: Evaluates ensemble estimator variance and decision boundary proximity to output confidence ratings (*Higher confidence*, *Moderate confidence*, *Lower confidence*).
4. **Out-Of-Distribution (OOD) Input Reliability Check**: Validates patient parameters against physical limits and training cohort bounds (`Q1 - 3*IQR` to `Q3 + 3*IQR`), rejecting invalid entries (e.g. Age = 150) before inference.
5. **Personal Health Timeline**: Tracks user measurement history over time, rendering model-estimate trend line charts.
6. **Multi-Disease Risk Profile**: Evaluates all 5 disease modules independently on a unified patient profile without artificially combining probabilities into an unscientific single score.
7. **Mitchell et al. Model Cards**: Interactive model cards accessible at `/models/{disease}/model-card` documenting dataset provenance, sample sizes, cross-validation metrics, limitations, and fairness notes.

---

## 📊 3. Legitimate Public Healthcare Datasets

| Disease Module | Public Dataset Source | Samples | Features | Production Candidate Model | Test ROC-AUC | Test Recall |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Diabetes** | UCI / NIDDK Pima Indians Database | 768 | 8 | Random Forest | 0.8194 | 0.7593 |
| **Heart Disease** | UCI Cleveland Clinic Foundation | 303 | 13 | Random Forest | 0.9058 | 0.8788 |
| **Breast Cancer** | UCI Wisconsin Diagnostic (WDBC) | 569 | 30 | Logistic Regression | 0.9954 | 0.9524 |
| **Lung Cancer** | Public Survey Benchmark Dataset | 309 | 15 | Random Forest | 0.9635 | 0.9375 |
| **Stroke** | Healthcare Stroke Benchmark | 5,110 | 11 | Balanced Logistic Regression | 0.8393 | 0.8000 |

---

## 🚀 4. Quick Start & Execution

### Prerequisites
- Python 3.12+
- Node.js v20+ / npm

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download Legitimate Datasets & Train Models
```bash
python training/download_datasets.py
python training/record_metadata.py
python training/train_all.py
```

### Step 3: Run Backend FastAPI Server
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```
- API Swagger Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/health`

### Step 4: Run React Frontend Interface
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 5. Testing & Verification
```bash
pytest tests/test_prediction.py
```

---

## 🛡️ 6. Medical Safety Disclaimer
This system is an educational and research decision-support prototype. It provides machine-learning estimates based strictly on supplied parameters and should NOT be used for direct medical diagnosis or clinical treatment decisions.

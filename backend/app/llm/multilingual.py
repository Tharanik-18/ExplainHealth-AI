"""
Multilingual (English, Tamil, Tanglish) Intent and Disease Parser for ExplainHealth AI
Maps natural-language text in English, Tamil script, and Tanglish (phonetic Tamil in Roman script)
to normalized disease keys and intent categories.
"""

import re
from typing import Tuple, Dict, Any, Optional

DISEASE_KEYWORDS = {
    "diabetes": [
        "diabetes", "diabetic", "sugar", "glucose", "சர்க்கரை", "டயபெடீஸ்",
        "sugar risk", "diab", "type 2", "pima"
    ],
    "heart_disease": [
        "heart", "heart disease", "cardiac", "cardiovascular", "chest pain",
        "இதயம்", "இதய நோய்", "நெஞ்சு வலி", "heart risk", "cholesterol"
    ],
    "breast_cancer": [
        "breast", "breast cancer", "tumor", "breast mass", "mammogram",
        "மார்பக புற்றுநோய்", "மார்பக நோய்", "biopsy", "wdbc"
    ],
    "lung_cancer": [
        "lung", "lung cancer", "pulmonary", "smoking cough", "wheezing",
        "நுரையீரல்", "நுரையீரல் புற்றுநோய்", "lung risk", "cough"
    ],
    "stroke": [
        "stroke", "paralysis", "brain stroke", "cerebrovascular",
        "பக்கவாதம்", "மூளை பக்கவாதம்", "stroke risk", "hypertension"
    ]
}

INTENT_PATTERNS = {
    "disease_risk_analysis": [
        r"check", r"predict", r"risk", r"analyze", r"test", r"check pannanum",
        r"பார்க்கணும்", r"பண்ணணும்", r"கண்டுபிடி", r"assess", r"calculate"
    ],
    "what_if_analysis": [
        r"what if", r"counterfactual", r"change", r"lower risk", r"reduce risk",
        r"bmi 27", r"glucose 140", r"மாற்றினால்", r"மாத்தினா"
    ],
    "explain_prediction": [
        r"why", r"explain", r"shap", r"reason", r"ஏன்", r"விளக்கு", r"factors"
    ],
    "compare_models": [
        r"compare", r"disagreement", r"other models", r"xgboost vs", r"rf vs",
        r"ஒப்பிடு", r"மாற்று மாதிரிகள்"
    ],
    "view_health_trend": [
        r"trend", r"history", r"timeline", r"previous", r"வரலாறு", r"முந்தைய"
    ],
    "model_information": [
        r"model card", r"dataset", r"accuracy", r"training data", r"தரவுத்தளம்"
    ]
}

def detect_disease(text: str) -> Optional[str]:
    """Detects disease module target from user message."""
    text_lower = text.lower()
    for disease, keywords in DISEASE_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return disease
    return None

def detect_intent(text: str) -> str:
    """Detects primary conversational intent."""
    text_lower = text.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                return intent
    return "disease_risk_analysis"

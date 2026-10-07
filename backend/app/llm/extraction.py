"""
Natural Language Structured Information Extraction Engine
"""

import re
from typing import Dict, Any, Tuple, List, Optional

from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS
from backend.app.llm.multilingual import detect_disease, detect_intent

FEATURE_PATTERNS = {
    "age": [
        r"(?:age|years old|வயது|வயசு)\s*[:=]?\s*(\d{1,3})",
        r"(\d{1,3})\s*(?:years old|yrs old|வயது)"
    ],
    "glucose": [
        r"(?:glucose|sugar|blood sugar|ரத்த சர்க்கரை)\s*[:=]?\s*(\d{2,3})",
        r"(\d{2,3})\s*(?:mg/dl|mgdl)"
    ],
    "bmi": [
        r"(?:bmi|body mass index)\s*[:=]?\s*(\d{2}(?:\.\d{1,2})?)",
        r"(\d{2}(?:\.\d{1,2})?)\s*(?:bmi)"
    ],
    "blood_pressure": [
        r"(?:bp|blood pressure|bloodpressure|ரத்த அழுத்தம்)\s*[:=]?\s*(\d{2,3})",
        r"(\d{2,3})\s*(?:mmhg)"
    ],
    "insulin": [
        r"(?:insulin|இன்சுலின்)\s*[:=]?\s*(\d{1,3})"
    ],
    "pregnancies": [
        r"(?:pregnancies|pregnant|கர்ப்பம்)\s*[:=]?\s*(\d{1,2})"
    ],
    "chol": [
        r"(?:cholesterol|chol|கொலஸ்ட்ரால்)\s*[:=]?\s*(\d{2,3})"
    ],
    "trestbps": [
        r"(?:resting bp|trestbps|resting blood pressure)\s*[:=]?\s*(\d{2,3})"
    ],
    "thalach": [
        r"(?:max heart rate|heart rate|thalach|இதய துடிப்பு)\s*[:=]?\s*(\d{2,3})"
    ],
    "avg_glucose_level": [
        r"(?:avg glucose|average glucose|glucose level)\s*[:=]?\s*(\d{2,3}(?:\.\d{1,2})?)"
    ]
}

class ClinicalSlotExtractor:
    def extract_slots(self, text: str, disease: Optional[str] = None) -> Dict[str, Any]:
        extracted = {}
        text_lower = text.lower()
        
        for feature_key, patterns in FEATURE_PATTERNS.items():
            for pat in patterns:
                match = re.search(pat, text_lower)
                if match:
                    val_str = match.group(1)
                    try:
                        if "." in val_str:
                            extracted[feature_key] = float(val_str)
                        else:
                            extracted[feature_key] = int(val_str)
                        break
                    except ValueError:
                        pass
                        
        if "glucose" in extracted and "avg_glucose_level" not in extracted:
            extracted["avg_glucose_level"] = float(extracted["glucose"])
        if "bp" in text_lower and "trestbps" not in extracted and "blood_pressure" in extracted:
            extracted["trestbps"] = extracted["blood_pressure"]
            
        return extracted

    def get_missing_inputs(self, disease: str, existing_slots: Dict[str, Any]) -> Tuple[List[str], List[Dict[str, Any]]]:
        schema = DISEASE_SCHEMAS.get(disease, {})
        required = schema.get("required_features", [])
        features_meta = schema.get("features", {})
        
        missing_names = []
        missing_meta = []
        
        for req in required:
            if req not in existing_slots or existing_slots[req] is None:
                missing_names.append(req)
                if req in features_meta:
                    missing_meta.append(features_meta[req])
                    
        return missing_names, missing_meta

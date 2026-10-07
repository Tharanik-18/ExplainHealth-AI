"""
Model Disagreement Engine for ExplainHealth AI
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any

from backend.app.config import MODELS_DIR, PREPROCESSORS_DIR

class ModelDisagreementEngine:
    def __init__(self, disease: str):
        self.disease = disease
        self.preprocessor = joblib.load(os.path.join(PREPROCESSORS_DIR, f"{disease}_preprocessor.joblib"))
        self.all_models: Dict[str, Any] = joblib.load(os.path.join(MODELS_DIR, f"{disease}_all_models.joblib"))

    def compare_models(self, input_df: pd.DataFrame, threshold: float = 0.15) -> Dict[str, Any]:
        X_trans = self.preprocessor.transform(input_df)
        
        predictions = {}
        probabilities = {}
        
        for name, model in self.all_models.items():
            try:
                prob = float(model.predict_proba(X_trans)[0, 1])
                pred = int(model.predict(X_trans)[0])
                clean_name = name.replace("_", " ").title()
                probabilities[clean_name] = round(prob, 4)
                predictions[clean_name] = pred
            except Exception as e:
                pass
                
        prob_values = list(probabilities.values())
        if not prob_values:
            return {"disagreement_detected": False, "spread": 0.0, "models": {}}
            
        max_prob = max(prob_values)
        min_prob = min(prob_values)
        spread = round(max_prob - min_prob, 4)
        std_dev = round(float(np.std(prob_values)), 4)
        mean_prob = round(float(np.mean(prob_values)), 4)
        
        disagreement_detected = spread >= threshold
        
        if disagreement_detected:
            message = (
                f"Model disagreement detected: Predictions vary from {min_prob*100:.1f}% to {max_prob*100:.1f}% "
                f"(spread of {spread*100:.1f}%). The estimate is sensitive to model architecture choice "
                f"and should be interpreted with heightened clinical caution."
            )
        else:
            message = (
                f"High model consensus: All {len(prob_values)} candidate architectures produce closely aligned "
                f"estimates within a {spread*100:.1f}% margin (mean: {mean_prob*100:.1f}%)."
            )
            
        model_details = []
        for name, prob in probabilities.items():
            model_details.append({
                "model_name": name,
                "probability": prob,
                "percentage": f"{prob * 100:.1f}%",
                "risk_verdict": "Elevated Risk" if prob >= 0.50 else "Lower Risk"
            })
            
        return {
            "disease": self.disease,
            "disagreement_detected": disagreement_detected,
            "spread": spread,
            "std_deviation": std_dev,
            "mean_probability": mean_prob,
            "interpretation": message,
            "models_comparison": model_details
        }

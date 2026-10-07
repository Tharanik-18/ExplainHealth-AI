"""
Counterfactual Explanation Engine ("What Would Change the Prediction?")
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional

from backend.app.config import MODELS_DIR, PREPROCESSORS_DIR
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

class CounterfactualEngine:
    def __init__(self, disease: str):
        self.disease = disease
        self.schema = DISEASE_SCHEMAS.get(disease, {})
        self.model = joblib.load(os.path.join(MODELS_DIR, f"{disease}_production_model.joblib"))
        self.preprocessor = joblib.load(os.path.join(PREPROCESSORS_DIR, f"{disease}_preprocessor.joblib"))
        
    def generate_counterfactuals(
        self,
        current_input: Dict[str, Any],
        target_risk_threshold: float = 0.35,
        max_iterations: int = 150
    ) -> Dict[str, Any]:
        current_df = pd.DataFrame([current_input])
        current_trans = self.preprocessor.transform(current_df)
        current_prob = float(self.model.predict_proba(current_trans)[0, 1])
        
        if current_prob <= target_risk_threshold:
            goal_risk = max(0.10, current_prob * 0.7)
        else:
            goal_risk = target_risk_threshold
            
        features_meta = self.schema.get("features", {})
        actionable_features = [
            k for k, v in features_meta.items() 
            if v.get("actionable", False) and k in current_input
        ]
        
        if not actionable_features:
            return {
                "disease": self.disease,
                "current_probability": round(current_prob, 4),
                "counterfactual_found": False,
                "message": "No actionable features are present in this disease schema to generate what-if counterfactual scenarios."
            }
            
        scenario_moderate = current_input.copy()
        scenario_ideal = current_input.copy()
        
        for feat in actionable_features:
            meta = features_meta[feat]
            curr_val = current_input[feat]
            f_min = meta.get("min", 0)
            f_max = meta.get("max", 100)
            
            if meta["type"] == "numerical" and isinstance(curr_val, (int, float)):
                step_mod = curr_val - 0.15 * (curr_val - f_min)
                scenario_moderate[feat] = round(max(f_min, step_mod), 2)
                
                step_ideal = curr_val - 0.30 * (curr_val - f_min)
                scenario_ideal[feat] = round(max(f_min, step_ideal), 2)
                
            elif meta["type"] == "categorical":
                if feat in ["smoking", "alcohol_consuming", "smoking_status", "hypertension", "fbs"]:
                    if feat == "smoking":
                        scenario_moderate[feat] = 1
                        scenario_ideal[feat] = 1
                    elif feat == "smoking_status":
                        scenario_moderate[feat] = "never smoked"
                        scenario_ideal[feat] = "never smoked"
                    elif feat in ["hypertension", "fbs"]:
                        scenario_moderate[feat] = 0
                        scenario_ideal[feat] = 0
                        
        mod_df = pd.DataFrame([scenario_moderate])
        mod_prob = float(self.model.predict_proba(self.preprocessor.transform(mod_df))[0, 1])
        
        ideal_df = pd.DataFrame([scenario_ideal])
        ideal_prob = float(self.model.predict_proba(self.preprocessor.transform(ideal_df))[0, 1])
        
        def build_diff(scen: Dict[str, Any], prob: float, name: str):
            changes = []
            for f in actionable_features:
                c_val = current_input[f]
                s_val = scen[f]
                if c_val != s_val:
                    meta = features_meta[f]
                    changes.append({
                        "feature": f,
                        "label": meta.get("label", f),
                        "label_ta": meta.get("label_ta", f),
                        "current_value": c_val,
                        "scenario_value": s_val,
                        "unit": meta.get("unit", "")
                    })
            return {
                "scenario_name": name,
                "estimated_probability": round(prob, 4),
                "absolute_risk_reduction": round(max(0.0, current_prob - prob), 4),
                "modified_features": changes
            }
            
        scenarios = [
            build_diff(scenario_moderate, mod_prob, "Moderate Adjustment Scenario"),
            build_diff(scenario_ideal, ideal_prob, "Target Health Profile Scenario")
        ]
        
        disclaimer = (
            "IMPORTANT NOTICE: Under this machine-learning model, changing these specific input values "
            "while holding all other patient features constant produces a lower mathematical risk estimate. "
            "This represents a mathematical model simulation, NOT medical advice, diagnostic certainty, or clinical treatment recommendations."
        )
        
        return {
            "disease": self.disease,
            "current_probability": round(current_prob, 4),
            "target_threshold": round(goal_risk, 4),
            "counterfactual_found": True,
            "scenarios": scenarios,
            "disclaimer": disclaimer
        }

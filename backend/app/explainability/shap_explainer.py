"""
SHAP Explainability Engine for ExplainHealth AI
"""

import os
import joblib
import numpy as np
import pandas as pd
import shap
from typing import Dict, List, Any

from backend.app.config import MODELS_DIR, PREPROCESSORS_DIR, EXPLAINERS_DIR
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

class DiseaseSHAPExplainer:
    def __init__(self, disease: str):
        self.disease = disease
        self.schema = DISEASE_SCHEMAS.get(disease, {})
        
        # Load production model, preprocessor, and background sample
        self.model = joblib.load(os.path.join(MODELS_DIR, f"{disease}_production_model.joblib"))
        self.preprocessor = joblib.load(os.path.join(PREPROCESSORS_DIR, f"{disease}_preprocessor.joblib"))
        self.bg_sample = joblib.load(os.path.join(EXPLAINERS_DIR, f"{disease}_background.joblib"))
        
        # Get feature names
        try:
            self.feature_names = self.preprocessor.get_feature_names_out().tolist()
        except Exception:
            self.feature_names = [f"f_{i}" for i in range(self.bg_sample.shape[1])]
            
        # Initialize appropriate SHAP Explainer
        model_name = type(self.model).__name__
        if "Forest" in model_name or "Tree" in model_name or "GB" in model_name or "XGB" in model_name or "LGBM" in model_name:
            try:
                self.explainer = shap.TreeExplainer(self.model)
            except Exception:
                self.explainer = shap.Explainer(self.model, self.bg_sample)
        elif "Logistic" in model_name or "Linear" in model_name:
            try:
                self.explainer = shap.LinearExplainer(self.model, self.bg_sample)
            except Exception:
                self.explainer = shap.Explainer(self.model, self.bg_sample)
        else:
            self.explainer = shap.Explainer(self.model, self.bg_sample)

    def _clean_feature_name(self, raw_name: str) -> str:
        clean = raw_name.replace("num__", "").replace("cat__", "")
        return clean

    def explain_instance(self, input_df: pd.DataFrame) -> Dict[str, Any]:
        X_trans = self.preprocessor.transform(input_df)
        shap_vals = self.explainer(X_trans)
        
        values = shap_vals.values[0]
        base_val = shap_vals.base_values[0]
        
        if len(values.shape) > 1 and values.shape[-1] == 2:
            values = values[:, 1]
            if isinstance(base_val, np.ndarray) and len(base_val) == 2:
                base_val = float(base_val[1])
        elif len(values.shape) > 1 and values.shape[0] == 2:
            values = values[1, :]
            if isinstance(base_val, np.ndarray) and len(base_val) == 2:
                base_val = float(base_val[1])
                
        base_value = float(base_val) if np.isscalar(base_val) else float(base_val[0])
        
        contributions = []
        for i, raw_fn in enumerate(self.feature_names):
            val = float(values[i])
            clean_name = self._clean_feature_name(raw_fn)
            
            orig_val = None
            for col in input_df.columns:
                if col in raw_fn:
                    orig_val = input_df[col].iloc[0]
                    break
                    
            label = clean_name.replace("_", " ").title()
            label_ta = label
            if clean_name in self.schema.get("features", {}):
                f_meta = self.schema["features"][clean_name]
                label = f_meta.get("label", label)
                label_ta = f_meta.get("label_ta", label)
                
            contributions.append({
                "feature": clean_name,
                "label": label,
                "label_ta": label_ta,
                "shap_value": round(val, 4),
                "original_value": orig_val,
                "abs_importance": round(abs(val), 4)
            })
            
        contributions_sorted = sorted(contributions, key=lambda x: x["abs_importance"], reverse=True)
        
        why_factors = [c for c in contributions_sorted if c["shap_value"] > 0.001]
        why_not_factors = [c for c in contributions_sorted if c["shap_value"] < -0.001]
        
        top_positive = why_factors[:3]
        top_negative = why_not_factors[:2]
        
        summary_sentences = []
        if top_positive:
            pos_names = [f"{p['label']} (impact: +{p['shap_value']:.2f})" for p in top_positive]
            summary_sentences.append(
                f"The model's estimate was most strongly elevated by: {', '.join(pos_names)}."
            )
        if top_negative:
            neg_names = [f"{n['label']} (impact: {n['shap_value']:.2f})" for n in top_negative]
            summary_sentences.append(
                f"Factors exerting a lower or protective influence on this estimate include: {', '.join(neg_names)}."
            )
            
        summary_text = " ".join(summary_sentences) if summary_sentences else "Feature attributions evaluated."
        
        summary_ta = (
            f"மாதிரி மதிப்பீட்டை உயர்த்திய முக்கிய காரணிகள்: {', '.join([p['label_ta'] for p in top_positive])}."
        ) if top_positive else "காரணிகள் பகுப்பாய்வு செய்யப்பட்டது."
        
        return {
            "disease": self.disease,
            "base_value": round(base_value, 4),
            "summary_explanation": summary_text,
            "summary_explanation_ta": summary_ta,
            "all_contributions": contributions_sorted,
            "why_factors_increasing_risk": why_factors[:6],
            "why_not_factors_decreasing_risk": why_not_factors[:6],
            "top_positive_features": [p["feature"] for p in top_positive],
            "top_negative_features": [n["feature"] for n in top_negative]
        }

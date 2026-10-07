"""
LIME Tabular Explainability Module for ExplainHealth AI
"""

import os
import joblib
import numpy as np
import pandas as pd
from lime import lime_tabular
from typing import Dict, Any, List

from backend.app.config import MODELS_DIR, PREPROCESSORS_DIR, EXPLAINERS_DIR

class DiseaseLIMEExplainer:
    def __init__(self, disease: str):
        self.disease = disease
        self.model = joblib.load(os.path.join(MODELS_DIR, f"{disease}_production_model.joblib"))
        self.preprocessor = joblib.load(os.path.join(PREPROCESSORS_DIR, f"{disease}_preprocessor.joblib"))
        self.bg_sample = joblib.load(os.path.join(EXPLAINERS_DIR, f"{disease}_background.joblib"))
        
        try:
            self.feature_names = self.preprocessor.get_feature_names_out().tolist()
        except Exception:
            self.feature_names = [f"f_{i}" for i in range(self.bg_sample.shape[1])]
            
        self.explainer = lime_tabular.LimeTabularExplainer(
            training_data=self.bg_sample,
            feature_names=self.feature_names,
            class_names=["Lower Risk", "Elevated Risk"],
            mode="classification"
        )

    def explain_instance(self, input_df: pd.DataFrame, num_features: int = 6) -> Dict[str, Any]:
        X_trans = self.preprocessor.transform(input_df)
        instance = X_trans[0]
        
        exp = self.explainer.explain_instance(
            data_row=instance,
            predict_fn=self.model.predict_proba,
            num_features=num_features
        )
        
        weights = exp.as_list()
        items = []
        for feature_rule, weight in weights:
            items.append({
                "rule": feature_rule,
                "weight": round(float(weight), 4),
                "direction": "increases_risk" if weight > 0 else "decreases_risk"
            })
            
        return {
            "disease": self.disease,
            "method": "LIME (Local Interpretable Model-agnostic Explanations)",
            "local_weights": items
        }

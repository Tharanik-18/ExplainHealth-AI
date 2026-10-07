"""
Unified Disease Risk Assessment and Explainability Orchestrator
Coordinates:
- Input Reliability / OOD Validation
- Calibrated ML Prediction
- Prediction Uncertainty
- SHAP Feature Attributions ("Why & Why Not")
- Multi-Model Disagreement
- Actionable Counterfactual Scenarios
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

from backend.app.config import MODELS_DIR, PREPROCESSORS_DIR
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS
from backend.app.uncertainty.detector import UncertaintyAndOODDetector
from backend.app.explainability.shap_explainer import DiseaseSHAPExplainer
from backend.app.counterfactual.engine import CounterfactualEngine
from backend.app.ml.prediction.disagreement import ModelDisagreementEngine
from backend.app.utils.sanitizer import sanitize_json_payload

class DiseaseRiskService:
    def __init__(self, disease: str):
        if disease not in DISEASE_SCHEMAS:
            raise ValueError(f"Unknown disease: {disease}. Supported: {list(DISEASE_SCHEMAS.keys())}")
        self.disease = disease
        self.schema = DISEASE_SCHEMAS[disease]
        
        # Load artifacts using central config paths
        self.calibrated_model = joblib.load(os.path.join(MODELS_DIR, f"{disease}_calibrated_model.joblib"))
        self.preprocessor = joblib.load(os.path.join(PREPROCESSORS_DIR, f"{disease}_preprocessor.joblib"))
        
        # Initialize sub-engines
        self.ood_detector = UncertaintyAndOODDetector(disease)
        self.shap_explainer = DiseaseSHAPExplainer(disease)
        self.counterfactual_engine = CounterfactualEngine(disease)
        self.disagreement_engine = ModelDisagreementEngine(disease)

    def _prepare_full_input_dataframe(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        features_meta = self.schema.get("features", {})
        training_dists = self.ood_detector.training_dists
        
        processed_input = {}
        expected_cols = getattr(self.preprocessor, "feature_names_in_", list(features_meta.keys()))
        
        for col in expected_cols:
            if col in input_data and input_data[col] is not None:
                processed_input[col] = input_data[col]
            elif col in features_meta and "default" in features_meta[col]:
                processed_input[col] = features_meta[col]["default"]
            elif col in training_dists and "median" in training_dists[col]:
                processed_input[col] = training_dists[col]["median"]
            elif col in training_dists and "categories" in training_dists[col] and training_dists[col]["categories"]:
                processed_input[col] = training_dists[col]["categories"][0]
            else:
                processed_input[col] = 0.0
                
        return pd.DataFrame([processed_input]), processed_input

    def analyze_risk(
        self,
        input_data: Dict[str, Any],
        include_counterfactuals: bool = True,
        include_disagreement: bool = True
    ) -> Dict[str, Any]:
        """
        Executes end-to-end interpretable ML pipeline with sanitized JSON output.
        """
        input_df, processed_input = self._prepare_full_input_dataframe(input_data)
        
        # 1. Input Reliability & OOD Check
        reliability_check = self.ood_detector.check_input_reliability(input_data)
        if not reliability_check["is_valid"]:
            return sanitize_json_payload({
                "success": False,
                "disease": self.disease,
                "display_name": self.schema["display_name"],
                "error_type": "OUT_OF_DISTRIBUTION_REJECTION",
                "message": "The supplied input values fall outside plausible clinical boundaries or the training distribution. The system cannot reliably generate an estimate.",
                "reliability_report": reliability_check
            })
            
        # 2. Model Prediction with Probability Calibration
        X_trans = self.preprocessor.transform(input_df)
        raw_prob = float(self.calibrated_model.predict_proba(X_trans)[0, 1])
        prediction = 1 if raw_prob >= 0.50 else 0
        
        # Clinical Risk Level Classification
        if raw_prob < 0.25:
            risk_tier = "Lower Model-Estimated Risk"
            risk_tier_ta = "குறைந்த ஆபத்து மதிப்பீடு"
            severity = "low"
        elif raw_prob < 0.60:
            risk_tier = "Moderate Model-Estimated Risk"
            risk_tier_ta = "நடுத்தர ஆபத்து மதிப்பீடு"
            severity = "moderate"
        else:
            risk_tier = "Elevated Model-Estimated Risk"
            risk_tier_ta = "அதிகரித்த ஆபத்து மதிப்பீடு"
            severity = "elevated"
            
        # 3. Uncertainty Estimation
        uncertainty = self.ood_detector.estimate_uncertainty(input_df, raw_prob)
        
        # 4. SHAP Attributions ("Why & Why Not")
        shap_explanation = self.shap_explainer.explain_instance(input_df)
        
        # 5. Model Disagreement
        disagreement_report = None
        if include_disagreement:
            disagreement_report = self.disagreement_engine.compare_models(input_df)
            
        # 6. Counterfactual Analysis
        counterfactual_report = None
        if include_counterfactuals:
            counterfactual_report = self.counterfactual_engine.generate_counterfactuals(processed_input)
            
        disclaimer = (
            "EDUCATIONAL NOTICE: This estimate is generated purely by a machine learning model "
            "based on the supplied structured inputs. It does NOT constitute a clinical diagnosis, "
            "medical opinion, or treatment guidance. Always consult a qualified healthcare provider."
        )
        
        raw_result = {
            "success": True,
            "disease": self.disease,
            "display_name": self.schema["display_name"],
            "prediction": prediction,
            "probability": round(raw_prob, 4),
            "percentage": f"{raw_prob * 100:.1f}%",
            "risk_tier": risk_tier,
            "risk_tier_ta": risk_tier_ta,
            "severity": severity,
            "reliability_report": reliability_check,
            "uncertainty": uncertainty,
            "shap_explanation": shap_explanation,
            "model_disagreement": disagreement_report,
            "counterfactuals": counterfactual_report,
            "input_data": processed_input,
            "disclaimer": disclaimer
        }
        
        return sanitize_json_payload(raw_result)

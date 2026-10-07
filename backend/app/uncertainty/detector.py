"""
Uncertainty and Out-Of-Distribution (OOD) Input Reliability Detector
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple

from backend.app.config import MODELS_DIR, PREPROCESSORS_DIR, MODEL_CARDS_DIR
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

class UncertaintyAndOODDetector:
    def __init__(self, disease: str):
        self.disease = disease
        self.schema = DISEASE_SCHEMAS.get(disease, {})
        
        # Load training distributions from Model Card
        card_path = os.path.join(MODEL_CARDS_DIR, f"{disease}_model_card.json")
        self.training_dists = {}
        if os.path.exists(card_path):
            with open(card_path, "r") as f:
                card = json.load(f)
                self.training_dists = card.get("training_distribution_summary", {})
                
        # Load production model & preprocessor for ensemble variance inspection
        self.model = joblib.load(os.path.join(MODELS_DIR, f"{disease}_production_model.joblib"))
        self.preprocessor = joblib.load(os.path.join(PREPROCESSORS_DIR, f"{disease}_preprocessor.joblib"))

    def check_input_reliability(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        hard_rejections = []
        warnings = []
        features_meta = self.schema.get("features", {})
        
        for feat_name, val in input_dict.items():
            if val is None or val == "":
                continue
                
            if feat_name in features_meta:
                meta = features_meta[feat_name]
                if meta["type"] == "numerical":
                    try:
                        num_val = float(val)
                        if "min" in meta and num_val < meta["min"]:
                            hard_rejections.append(
                                f"The supplied value for '{meta['label']}' ({num_val} {meta.get('unit', '')}) is below the plausible clinical limit ({meta['min']})."
                            )
                        if "max" in meta and num_val > meta["max"]:
                            hard_rejections.append(
                                f"The supplied value for '{meta['label']}' ({num_val} {meta.get('unit', '')}) exceeds the plausible clinical limit ({meta['max']})."
                            )
                    except (ValueError, TypeError):
                        hard_rejections.append(f"Invalid non-numerical input provided for '{meta['label']}': {val}")
                        
            if feat_name in self.training_dists:
                dist = self.training_dists[feat_name]
                if dist["type"] == "numerical":
                    try:
                        num_val = float(val)
                        t_min = dist["min"]
                        t_max = dist["max"]
                        q25 = dist.get("q25", t_min)
                        q75 = dist.get("q75", t_max)
                        iqr = dist.get("iqr", (q75 - q25))
                        
                        if num_val < (t_min - 0.25 * (t_max - t_min)) or num_val > (t_max + 0.25 * (t_max - t_min)):
                            hard_rejections.append(
                                f"The supplied value for '{feat_name}' ({num_val}) is outside the distribution represented in the training dataset ({t_min:.1f} to {t_max:.1f}). The model cannot reliably generate an estimate."
                            )
                        elif iqr > 0 and (num_val < q25 - 3 * iqr or num_val > q75 + 3 * iqr):
                            warnings.append(
                                f"'{feat_name}' value ({num_val}) is an extreme statistical outlier compared to the training cohort."
                            )
                    except Exception:
                        pass
                elif dist["type"] == "categorical":
                    allowed_cats = dist.get("categories", [])
                    if allowed_cats and str(val) not in allowed_cats:
                        warnings.append(f"Category '{val}' for '{feat_name}' was not encountered in the training dataset.")
                        
        is_valid = len(hard_rejections) == 0
        is_ood = len(hard_rejections) > 0 or len(warnings) >= 2
        
        reliability_score = 1.0
        if not is_valid:
            reliability_score = 0.0
        else:
            reliability_score = max(0.2, 1.0 - (len(warnings) * 0.2))
            
        return {
            "is_valid": is_valid,
            "is_ood": is_ood,
            "reliability_score": round(reliability_score, 2),
            "rejection_reasons": hard_rejections,
            "warnings": warnings,
            "safety_verdict": "Reliable In-Distribution Input" if is_valid and not is_ood else (
                "Rejected: Out-of-Distribution Input" if not is_valid else "Caution: Statistical Outlier Detected"
            )
        }

    def estimate_uncertainty(self, input_df: pd.DataFrame, probability: float) -> Dict[str, Any]:
        X_trans = self.preprocessor.transform(input_df)
        
        ensemble_std = 0.0
        if hasattr(self.model, "estimators_"):
            try:
                tree_preds = [tree.predict_proba(X_trans)[0, 1] for tree in self.model.estimators_]
                ensemble_std = float(np.std(tree_preds))
            except Exception:
                ensemble_std = 0.05
        else:
            ensemble_std = 0.04
            
        prob_margin = abs(probability - 0.5)
        
        if prob_margin < 0.12 or ensemble_std > 0.18:
            confidence_level = "Lower model confidence"
            confidence_desc = "The model's probability estimate falls close to the classification threshold, indicating higher epistemic uncertainty."
        elif prob_margin > 0.28 and ensemble_std < 0.10:
            confidence_level = "Higher model confidence"
            confidence_desc = "The model demonstrates high agreement and substantial margin away from the decision boundary."
        else:
            confidence_level = "Moderate model confidence"
            confidence_desc = "The model demonstrates moderate certainty with consistent feature alignments."
            
        return {
            "confidence_level": confidence_level,
            "confidence_description": confidence_desc,
            "probability_margin": round(prob_margin, 4),
            "ensemble_variance": round(ensemble_std, 4)
        }

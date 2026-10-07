"""
Probability Calibration Engine for Healthcare Risk Models
Supports:
- Platt Scaling (Sigmoidal calibration)
- Isotonic Regression (Non-parametric isotonic calibration)
- Automatic selection based on Brier Score on validation split
"""

from typing import Tuple, Any
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss

def calibrate_model(
    model: Any,
    X_val: np.ndarray,
    y_val: np.ndarray
) -> Tuple[Any, str, float]:
    """
    Fits and compares Platt Scaling vs Isotonic Regression vs Raw model on the validation fold.
    Returns the best calibrated wrapper, the method used, and the improvement in Brier Score.
    """
    # 1. Raw model brier score
    raw_probs = model.predict_proba(X_val)[:, 1]
    raw_brier = brier_score_loss(y_val, raw_probs)
    
    best_calibrator = model
    best_method = "raw"
    best_brier = raw_brier
    
    # 2. Platt Scaling (Sigmoidal)
    try:
        platt = CalibratedClassifierCV(estimator=model, method="sigmoid", cv="prefit")
        platt.fit(X_val, y_val)
        platt_probs = platt.predict_proba(X_val)[:, 1]
        platt_brier = brier_score_loss(y_val, platt_probs)
        if platt_brier < best_brier:
            best_calibrator = platt
            best_method = "platt_scaling"
            best_brier = platt_brier
    except Exception:
        pass
        
    # 3. Isotonic Regression (suitable when validation samples > 100)
    if len(y_val) >= 80:
        try:
            iso = CalibratedClassifierCV(estimator=model, method="isotonic", cv="prefit")
            iso.fit(X_val, y_val)
            iso_probs = iso.predict_proba(X_val)[:, 1]
            iso_brier = brier_score_loss(y_val, iso_probs)
            if iso_brier < best_brier:
                best_calibrator = iso
                best_method = "isotonic_regression"
                best_brier = iso_brier
        except Exception:
            pass
            
    brier_improvement = round(float(raw_brier - best_brier), 4)
    return best_calibrator, best_method, brier_improvement

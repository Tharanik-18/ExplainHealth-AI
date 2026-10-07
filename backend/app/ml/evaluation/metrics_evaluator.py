"""
Evaluation and Probability Calibration Metrics Engine for Healthcare ML
Calculates:
- Accuracy, Precision, Recall/Sensitivity, Specificity, F1-Score
- ROC-AUC, PR-AUC (Average Precision)
- Confusion Matrix (TN, FP, FN, TP)
- Brier Score for probability error
- Calibration curve deciles
"""

from typing import Dict, Any, Tuple
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    brier_score_loss
)
from sklearn.calibration import calibration_curve

def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray
) -> Dict[str, Any]:
    """
    Computes a comprehensive suite of clinical and statistical classification metrics.
    """
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    y_prob = np.asarray(y_prob).astype(float)
    
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    
    try:
        roc_auc = float(roc_auc_score(y_true, y_prob))
    except Exception:
        roc_auc = 0.5
        
    try:
        pr_auc = float(average_precision_score(y_true, y_prob))
    except Exception:
        pr_auc = float(np.mean(y_true))
        
    brier = float(brier_score_loss(y_true, y_prob))
    
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
    else:
        tn, fp, fn, tp = 0, 0, 0, 0
        specificity = 0.0
        
    # Calibration curve (5-10 bins)
    try:
        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=8, strategy='uniform')
        calibration_points = [
            {"expected": float(p_pred), "observed": float(p_true)}
            for p_pred, p_true in zip(prob_pred, prob_true)
        ]
    except Exception:
        calibration_points = []
        
    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "sensitivity": round(rec, 4),
        "specificity": round(specificity, 4),
        "f1": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "brier_score": round(brier, 4),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp)
        },
        "calibration_curve": calibration_points
    }

def calculate_selection_score(
    metrics: Dict[str, Any],
    w_recall: float = 0.35,
    w_roc_auc: float = 0.35,
    w_f1: float = 0.20,
    w_brier: float = 0.10
) -> float:
    """
    Configurable healthcare scoring function.
    Prioritizes Recall (minimizing missed diseases) and ROC-AUC while penalizing poor calibration.
    """
    recall = metrics.get("recall", 0.0)
    roc_auc = metrics.get("roc_auc", 0.0)
    f1 = metrics.get("f1", 0.0)
    brier = metrics.get("brier_score", 0.25)
    
    # Invert brier score (lower brier is better, max is 1.0, perfect is 0.0)
    brier_component = max(0.0, 1.0 - brier)
    
    score = (
        w_recall * recall +
        w_roc_auc * roc_auc +
        w_f1 * f1 +
        w_brier * brier_component
    )
    return round(float(score), 4)

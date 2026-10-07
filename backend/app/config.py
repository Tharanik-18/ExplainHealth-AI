"""
Central Configuration and Path Registry for ExplainHealth AI
"""

import os

# Root directory resolution
APP_DIR = os.path.dirname(os.path.abspath(__file__))             # .../backend/app
BACKEND_DIR = os.path.dirname(APP_DIR)                           # .../backend
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)                       # ... (c:/Healthcaremachine)

# Artifact Directories
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "artifacts")
MODELS_DIR = os.path.join(ARTIFACTS_DIR, "models")
PREPROCESSORS_DIR = os.path.join(ARTIFACTS_DIR, "preprocessors")
METRICS_DIR = os.path.join(ARTIFACTS_DIR, "metrics")
MODEL_CARDS_DIR = os.path.join(ARTIFACTS_DIR, "model_cards")
EXPLAINERS_DIR = os.path.join(ARTIFACTS_DIR, "explainers")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def ensure_all_dirs():
    for d in [ARTIFACTS_DIR, MODELS_DIR, PREPROCESSORS_DIR, METRICS_DIR, MODEL_CARDS_DIR, EXPLAINERS_DIR, DATA_DIR]:
        os.makedirs(d, exist_ok=True)

ensure_all_dirs()

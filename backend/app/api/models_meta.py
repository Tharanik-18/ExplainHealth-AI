"""
Model Cards & Metadata Endpoints
"""

import os
import json
from fastapi import APIRouter, HTTPException

from backend.app.config import METRICS_DIR, MODEL_CARDS_DIR
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

router = APIRouter(tags=["Models & Metadata"])

def normalize_disease_name(disease: str) -> str:
    norm = disease.lower().replace("-", "_").replace(" ", "_")
    if norm == "heart":
        return "heart_disease"
    if norm in DISEASE_SCHEMAS:
        return norm
    raise HTTPException(status_code=404, detail=f"Disease module '{disease}' not found.")

@router.get("/models")
def list_models():
    models_summary = []
    for d_key, schema in DISEASE_SCHEMAS.items():
        card_path = os.path.join(MODEL_CARDS_DIR, f"{d_key}_model_card.json")
        metrics_path = os.path.join(METRICS_DIR, f"{d_key}_metrics.json")
        
        info = {
            "disease_id": d_key,
            "display_name": schema["display_name"],
            "description": schema["description"],
            "target": schema["target_name"],
            "features_count": len(schema["features"])
        }
        
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                m_data = json.load(f)
                info["selected_architecture"] = m_data.get("selected_model")
                info["roc_auc"] = m_data.get("test_metrics_calibrated", {}).get("roc_auc")
                info["recall"] = m_data.get("test_metrics_calibrated", {}).get("recall")
                
        models_summary.append(info)
    return {"models": models_summary}

@router.get("/models/{disease}")
def get_model_details(disease: str):
    disease_key = normalize_disease_name(disease)
    schema = DISEASE_SCHEMAS[disease_key]
    metrics_path = os.path.join(METRICS_DIR, f"{disease_key}_metrics.json")
    
    metrics = {}
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
    return {
        "disease": disease_key,
        "schema": schema,
        "evaluation_summary": metrics
    }

@router.get("/models/{disease}/metrics")
def get_model_metrics(disease: str):
    disease_key = normalize_disease_name(disease)
    metrics_path = os.path.join(METRICS_DIR, f"{disease_key}_metrics.json")
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail=f"Metrics for '{disease_key}' not found.")
    with open(metrics_path, "r") as f:
        return json.load(f)

@router.get("/models/{disease}/model-card")
def get_model_card(disease: str):
    disease_key = normalize_disease_name(disease)
    card_path = os.path.join(MODEL_CARDS_DIR, f"{disease_key}_model_card.json")
    if not os.path.exists(card_path):
        raise HTTPException(status_code=404, detail=f"Model card for '{disease_key}' not found.")
    with open(card_path, "r") as f:
        return json.load(f)

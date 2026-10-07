"""
Disease Risk Prediction & XAI Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.app.database.connection import get_db
from backend.app.schemas.prediction import RiskPredictionRequest
from backend.app.services.risk_service import DiseaseRiskService
from backend.app.explainability.shap_explainer import DiseaseSHAPExplainer
from backend.app.counterfactual.engine import CounterfactualEngine
from backend.app.ml.prediction.disagreement import ModelDisagreementEngine
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

router = APIRouter(tags=["Prediction & XAI"])

def normalize_disease_name(disease: str) -> str:
    norm = disease.lower().replace("-", "_").replace(" ", "_")
    if norm == "breast_cancer":
        return "breast_cancer"
    if norm == "lung_cancer":
        return "lung_cancer"
    if norm == "heart":
        return "heart_disease"
    if norm in DISEASE_SCHEMAS:
        return norm
    raise HTTPException(status_code=404, detail=f"Disease module '{disease}' not found. Supported: {list(DISEASE_SCHEMAS.keys())}")

@router.post("/predict/{disease}")
def predict_disease_risk(disease: str, payload: RiskPredictionRequest, db: Session = Depends(get_db)):
    disease_key = normalize_disease_name(disease)
    svc = DiseaseRiskService(disease_key)
    result = svc.analyze_risk(
        input_data=payload.patient_data,
        include_counterfactuals=payload.include_counterfactuals,
        include_disagreement=payload.include_disagreement
    )
    return result

@router.post("/explain/{disease}")
def explain_prediction(disease: str, payload: RiskPredictionRequest):
    disease_key = normalize_disease_name(disease)
    explainer = DiseaseSHAPExplainer(disease_key)
    import pandas as pd
    input_df = pd.DataFrame([payload.patient_data])
    explanation = explainer.explain_instance(input_df)
    return explanation

@router.post("/counterfactual/{disease}")
def get_counterfactuals(disease: str, payload: RiskPredictionRequest):
    disease_key = normalize_disease_name(disease)
    engine = CounterfactualEngine(disease_key)
    scenarios = engine.generate_counterfactuals(payload.patient_data)
    return scenarios

@router.post("/compare-models/{disease}")
def compare_disease_models(disease: str, payload: RiskPredictionRequest):
    disease_key = normalize_disease_name(disease)
    engine = ModelDisagreementEngine(disease_key)
    import pandas as pd
    input_df = pd.DataFrame([payload.patient_data])
    comparison = engine.compare_models(input_df)
    return comparison

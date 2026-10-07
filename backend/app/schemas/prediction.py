"""
Pydantic Request and Response Schemas for Prediction & XAI Endpoints
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class RiskPredictionRequest(BaseModel):
    patient_data: Dict[str, Any] = Field(..., json_schema_extra={"example": {"age": 45, "glucose": 165, "bmi": 31.0, "blood_pressure": 85}})
    anonymized_id: Optional[str] = "guest_user"
    include_counterfactuals: Optional[bool] = True
    include_disagreement: Optional[bool] = True

class ChatMessageRequest(BaseModel):
    user_message: str = Field(..., json_schema_extra={"example": "I am 45 years old, glucose 165, BMI 31. What is my diabetes risk?"})
    session_id: Optional[str] = None
    disease_override: Optional[str] = None
    anonymized_id: Optional[str] = "guest_user"

class MultiDiseaseProfileRequest(BaseModel):
    patient_data: Dict[str, Any] = Field(..., json_schema_extra={"example": {"age": 55, "glucose": 150, "bmi": 28.5, "blood_pressure": 130, "smoking": 2}})
    anonymized_id: Optional[str] = "guest_user"

class ReportGenerationRequest(BaseModel):
    anonymized_id: Optional[str] = "guest_user"
    patient_data: Optional[Dict[str, Any]] = None

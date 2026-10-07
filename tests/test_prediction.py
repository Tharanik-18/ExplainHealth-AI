"""
End-to-End API Integration Tests for ExplainHealth AI
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "diabetes" in data["supported_diseases"]

def test_models_list():
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) == 5

def test_diabetes_prediction():
    payload = {
        "patient_data": {
            "age": 45,
            "glucose": 165,
            "bmi": 31.0,
            "blood_pressure": 85
        }
    }
    response = client.post("/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "probability" in data
    assert "percentage" in data
    assert "shap_explanation" in data
    assert "counterfactuals" in data
    assert "model_disagreement" in data

def test_ood_input_rejection():
    payload = {
        "patient_data": {
            "age": 150,  # Invalid Age > 100
            "glucose": 120,
            "bmi": 25.0
        }
    }
    response = client.post("/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error_type"] == "OUT_OF_DISTRIBUTION_REJECTION"

def test_chat_slot_extraction():
    payload = {
        "user_message": "I am 55 years old and my glucose is 170. My BMI is 32."
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["intent"] in ["disease_risk_analysis", "input_collection"]

def test_multi_disease_profile():
    payload = {
        "patient_data": {
            "age": 55,
            "glucose": 150,
            "bmi": 29.0,
            "blood_pressure": 135,
            "smoking": 2
        }
    }
    response = client.post("/health-profile", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "disease_modules" in data
    assert len(data["disease_modules"]) == 5

"""
Multi-Disease Health Profile & Personal Health Timeline Service
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.app.database.models import User, PatientMeasurement
from backend.app.services.risk_service import DiseaseRiskService
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

class HealthProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_user(self, anonymized_id: str) -> User:
        user = self.db.query(User).filter(User.anonymized_id == anonymized_id).first()
        if not user:
            user = User(anonymized_id=anonymized_id)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def record_measurement(
        self,
        anonymized_id: str,
        disease: str,
        assessment_result: Dict[str, Any]
    ) -> PatientMeasurement:
        user = self.get_or_create_user(anonymized_id)
        
        record = PatientMeasurement(
            user_id=user.id,
            disease=disease,
            measurement_date=datetime.utcnow(),
            input_values=assessment_result.get("input_data", {}),
            predicted_risk=assessment_result.get("probability", 0.0),
            risk_tier=assessment_result.get("risk_tier", "Unknown"),
            severity=assessment_result.get("severity", "low"),
            full_assessment_payload=assessment_result
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_personal_health_timeline(self, anonymized_id: str) -> Dict[str, Any]:
        """
        Retrieves user's historical measurements over time, grouped by disease module.
        Labeled explicitly as 'Model-Estimate Trends'.
        """
        user = self.get_or_create_user(anonymized_id)
        records = (
            self.db.query(PatientMeasurement)
            .filter(PatientMeasurement.user_id == user.id)
            .order_by(PatientMeasurement.measurement_date.asc())
            .all()
        )
        
        timeline_by_disease: Dict[str, List[Dict[str, Any]]] = {d: [] for d in DISEASE_SCHEMAS.keys()}
        
        for r in records:
            if r.disease in timeline_by_disease:
                timeline_by_disease[r.disease].append({
                    "id": r.id,
                    "date": r.measurement_date.strftime("%Y-%m-%d %H:%M"),
                    "predicted_risk": r.predicted_risk,
                    "percentage": f"{r.predicted_risk * 100:.1f}%",
                    "risk_tier": r.risk_tier,
                    "severity": r.severity,
                    "inputs": r.input_values
                })
                
        return {
            "anonymized_id": anonymized_id,
            "title": "Personal Model-Estimate Health Trends",
            "disclaimer": "These trends reflect model-estimated risk variations across historical patient-entered measurements, not direct diagnostic progression.",
            "disease_timelines": timeline_by_disease
        }

    def generate_multi_disease_profile(
        self,
        unified_patient_data: Dict[str, Any],
        anonymized_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Runs all five disease models independently on a unified patient profile.
        Does NOT combine probabilities into an unscientific single overall score.
        """
        results = {}
        for disease in DISEASE_SCHEMAS.keys():
            svc = DiseaseRiskService(disease)
            res = svc.analyze_risk(unified_patient_data, include_counterfactuals=False, include_disagreement=False)
            results[disease] = res
            
            if anonymized_id and res.get("success"):
                self.record_measurement(anonymized_id, disease, res)
                
        return {
            "title": "Multi-Disease Risk Assessment Profile",
            "evaluated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "disease_modules": results,
            "methodology_note": "Each disease risk module evaluates independent clinical feature spaces with specialized machine learning architectures."
        }

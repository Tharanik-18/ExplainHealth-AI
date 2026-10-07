"""
Health Profile & Timeline Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.prediction import MultiDiseaseProfileRequest
from backend.app.services.profile_service import HealthProfileService

router = APIRouter(tags=["Health Profile & Timeline"])

@router.post("/health-profile")
def generate_multi_disease_profile(payload: MultiDiseaseProfileRequest, db: Session = Depends(get_db)):
    svc = HealthProfileService(db)
    profile = svc.generate_multi_disease_profile(
        unified_patient_data=payload.patient_data,
        anonymized_id=payload.anonymized_id
    )
    return profile

@router.get("/health-profile/{user_id}")
def get_user_health_timeline(user_id: str, db: Session = Depends(get_db)):
    svc = HealthProfileService(db)
    timeline = svc.get_personal_health_timeline(user_id)
    return timeline

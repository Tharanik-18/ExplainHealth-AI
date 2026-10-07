"""
Report Generation Endpoints
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.prediction import ReportGenerationRequest
from backend.app.services.report_service import ClinicalReportService
from backend.app.services.profile_service import HealthProfileService
from backend.app.services.risk_service import DiseaseRiskService

router = APIRouter(tags=["Reports"])

@router.post("/report")
def generate_clinical_report(payload: ReportGenerationRequest, db: Session = Depends(get_db)):
    anonymized_id = payload.anonymized_id or "guest_user"
    
    # If patient data is supplied, run risk service for all diseases
    assessments = []
    if payload.patient_data:
        profile_svc = HealthProfileService(db)
        profile = profile_svc.generate_multi_disease_profile(payload.patient_data, anonymized_id)
        assessments = list(profile.get("disease_modules", {}).values())
    else:
        # Load latest from timeline
        profile_svc = HealthProfileService(db)
        timeline = profile_svc.get_personal_health_timeline(anonymized_id)
        # Reconstruct assessments from latest measurements
        for disease, records in timeline.get("disease_timelines", {}).items():
            if records:
                latest = records[-1]
                svc = DiseaseRiskService(disease)
                res = svc.analyze_risk(latest.get("inputs", {}))
                assessments.append(res)
                
    report_svc = ClinicalReportService()
    html_report = report_svc.generate_html_report(anonymized_id, assessments)
    return Response(content=html_report, media_type="text/html")

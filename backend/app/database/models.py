"""
SQLAlchemy Models for ExplainHealth AI Database
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    anonymized_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    measurements = relationship("PatientMeasurement", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")

class PatientMeasurement(Base):
    __tablename__ = "patient_measurements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    disease = Column(String, index=True)
    measurement_date = Column(DateTime, default=datetime.utcnow, index=True)
    
    input_values = Column(JSON)
    predicted_risk = Column(Float)
    risk_tier = Column(String)
    severity = Column(String)
    full_assessment_payload = Column(JSON)
    
    user = relationship("User", back_populates="measurements")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    current_disease = Column(String, nullable=True)
    extracted_slots = Column(JSON, default=dict)
    conversation_history = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="chat_sessions")

class AssessmentReport(Base):
    __tablename__ = "assessment_reports"
    
    report_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    disease_assessments = Column(JSON)
    summary = Column(Text)

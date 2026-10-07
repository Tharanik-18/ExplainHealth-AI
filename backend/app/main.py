"""
ExplainHealth AI - Main FastAPI Application Server
Conversational Multi-Disease Interpretable Machine Learning System
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure project root is in python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.database.connection import engine, Base
from backend.app.api import chat, prediction, models_meta, health_profile, reports

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ExplainHealth AI API",
    description="Conversational Multi-Disease Interpretable Machine Learning System with SHAP, Counterfactuals, and Uncertainty Detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(chat.router)
app.include_router(prediction.router)
app.include_router(models_meta.router)
app.include_router(health_profile.router)
app.include_router(reports.router)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "system": "ExplainHealth AI",
        "supported_diseases": ["diabetes", "heart_disease", "breast_cancer", "lung_cancer", "stroke"],
        "xai_engines": ["SHAP", "LIME", "Counterfactual Optimization", "Model Disagreement"],
        "version": "1.0.0"
    }

@app.get("/", tags=["System"])
def root_endpoint():
    return {
        "message": "Welcome to ExplainHealth AI Conversational Interpretability System.",
        "documentation": "/docs",
        "health": "/health"
    }

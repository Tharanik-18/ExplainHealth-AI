"""
Chat API Endpoint
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.prediction import ChatMessageRequest
from backend.app.services.chat_service import ChatDialogueService

router = APIRouter(tags=["Chat"])

@router.post("/chat")
def chat_interaction(payload: ChatMessageRequest, db: Session = Depends(get_db)):
    svc = ChatDialogueService(db)
    response = svc.process_chat_message(
        user_message=payload.user_message,
        session_id=payload.session_id,
        disease_override=payload.disease_override,
        anonymized_id=payload.anonymized_id or "guest_user"
    )
    return response

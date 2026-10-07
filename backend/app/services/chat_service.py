"""
Conversational Dialogue & Intent Management Service for ExplainHealth AI
Coordinates:
- Session context and slot accumulation
- Emergency triage
- Disease routing
- Natural language slot extraction
- Input collection prompting
- Risk Assessment invocation
- Multi-lingual response formatting
"""

import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.app.database.models import ChatSession
from backend.app.llm.multilingual import detect_disease, detect_intent
from backend.app.llm.extraction import ClinicalSlotExtractor
from backend.app.llm.response_generator import ConversationalResponseGenerator
from backend.app.services.risk_service import DiseaseRiskService
from backend.app.services.profile_service import HealthProfileService
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

class ChatDialogueService:
    def __init__(self, db: Session):
        self.db = db
        self.extractor = ClinicalSlotExtractor()
        self.generator = ConversationalResponseGenerator()
        self.profile_service = HealthProfileService(db)

    def get_or_create_session(self, session_id: Optional[str], anonymized_id: str = "guest_user") -> ChatSession:
        user = self.profile_service.get_or_create_user(anonymized_id)
        if session_id:
            session = self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
            if session:
                return session
                
        new_session = ChatSession(
            session_id=str(uuid.uuid4()),
            user_id=user.id,
            extracted_slots={},
            conversation_history=[]
        )
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)
        return new_session

    def process_chat_message(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        disease_override: Optional[str] = None,
        anonymized_id: str = "guest_user"
    ) -> Dict[str, Any]:
        """
        Main conversational entrypoint.
        """
        # 1. Emergency Triage Check
        emergency_notice = self.generator.check_emergency_triage(user_message)
        if emergency_notice:
            return {
                "session_id": session_id or str(uuid.uuid4()),
                "intent": "emergency_triage",
                "message": emergency_notice,
                "is_emergency": True
            }
            
        session = self.get_or_create_session(session_id, anonymized_id)
        
        # 2. Disease Routing
        detected_dis = detect_disease(user_message)
        target_disease = disease_override or detected_dis or session.current_disease or "diabetes"
        session.current_disease = target_disease
        
        # 3. Intent Detection
        intent = detect_intent(user_message)
        
        # 4. Extract slots from user message and merge with session slots
        new_slots = self.extractor.extract_slots(user_message, target_disease)
        current_slots = dict(session.extracted_slots or {})
        current_slots.update(new_slots)
        session.extracted_slots = current_slots
        
        # 5. Intent-specific handlers
        # Case A: General Educational Question (e.g. "What is diabetes?")
        if "what is" in user_message.lower() and not new_slots and intent != "disease_risk_analysis":
            schema = DISEASE_SCHEMAS.get(target_disease, {})
            educational_text = (
                f"### Educational Information: {schema.get('display_name')}\n"
                f"{schema.get('description')}\n\n"
                f"I can analyze your personal risk estimate using our specialized machine-learning models "
                f"if you provide your measurements (e.g., age, glucose, BMI)."
            )
            return {
                "session_id": session.session_id,
                "intent": "educational_info",
                "disease": target_disease,
                "message": educational_text,
                "slots": current_slots
            }
            
        # Case B: Check for Missing Required Inputs
        missing_names, missing_meta = self.extractor.get_missing_inputs(target_disease, current_slots)
        
        if missing_names and intent == "disease_risk_analysis":
            prompt_text = self.generator.format_missing_inputs_prompt(target_disease, current_slots, missing_meta)
            self.db.commit()
            return {
                "session_id": session.session_id,
                "intent": "input_collection",
                "disease": target_disease,
                "message": prompt_text,
                "missing_fields": missing_names,
                "collected_slots": current_slots,
                "is_complete": False
            }
            
        # Case C: Sufficient Data Available -> Run ML Risk Assessment
        risk_service = DiseaseRiskService(target_disease)
        assessment = risk_service.analyze_risk(current_slots)
        
        if assessment.get("success"):
            self.profile_service.record_measurement(anonymized_id, target_disease, assessment)
            
        formatted_response = self.generator.format_risk_result_response(assessment)
        
        # Update history
        history = list(session.conversation_history or [])
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": formatted_response})
        session.conversation_history = history[-10:] # Keep last 10 turns
        self.db.commit()
        
        return {
            "session_id": session.session_id,
            "intent": intent,
            "disease": target_disease,
            "message": formatted_response,
            "collected_slots": current_slots,
            "is_complete": True,
            "assessment_result": assessment
        }

"""
Conversational Response Generator & Safety Triage Layer
Translates structured ML results into human-understandable natural language responses.
Strict Anti-Hallucination: Uses ONLY provided ML outputs.
"""

from typing import Dict, Any, List, Optional
from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

EMERGENCY_KEYWORDS = [
    "crushing chest pain", "severe chest pain", "sudden numbness",
    "slurred speech", "face drooping", "difficulty breathing",
    "நெஞ்சு வலி அதிகமா இருக்கு", "மூச்சு திணறல்"
]

class ConversationalResponseGenerator:
    def check_emergency_triage(self, user_message: str) -> Optional[str]:
        """Checks for acute emergency medical symptoms requiring immediate ER care."""
        msg_lower = user_message.lower()
        for kw in EMERGENCY_KEYWORDS:
            if kw in msg_lower:
                return (
                    "⚠️ **URGENT MEDICAL NOTICE**: You have mentioned potentially severe or acute symptoms "
                    "(such as severe chest pain, sudden numbness, or difficulty breathing). "
                    "This system is an educational decision-support tool and CANNOT handle emergency medical conditions. "
                    "Please seek immediate emergency medical care or call your local emergency services (e.g., 108/911) right now."
                )
        return None

    def format_missing_inputs_prompt(
        self,
        disease: str,
        collected_slots: Dict[str, Any],
        missing_meta: List[Dict[str, Any]]
    ) -> str:
        schema = DISEASE_SCHEMAS[disease]
        dis_name = schema["display_name"]
        
        collected_str = ", ".join([f"{k} ({v})" for k, v in collected_slots.items()]) if collected_slots else "None yet"
        missing_str = ", ".join([f"**{m.get('label', m.get('name'))}**" for m in missing_meta])
        
        msg = (
            f"I will use the **{dis_name}** prediction model.\n\n"
            f"✅ **Information received so far**: {collected_str}\n"
            f"❓ **Still needed to calculate an accurate estimate**: {missing_str}.\n\n"
            f"Please enter these details or use the form fields below to proceed."
        )
        return msg

    def format_risk_result_response(self, assessment: Dict[str, Any], language: str = "en") -> str:
        if not assessment.get("success"):
            return (
                f"❌ **Input Reliability Notice**: {assessment.get('message')}\n\n"
                f"**Reasons**: {'; '.join(assessment.get('reliability_report', {}).get('rejection_reasons', []))}"
            )
            
        dis_display = assessment["display_name"]
        risk_pct = assessment["percentage"]
        risk_tier = assessment["risk_tier"]
        unc = assessment["uncertainty"]
        shap_exp = assessment["shap_explanation"]
        disagreement = assessment.get("model_disagreement")
        counterfactuals = assessment.get("counterfactuals")
        
        # Build Natural Language Output
        response_lines = [
            f"### 📊 {dis_display} Machine Learning Analysis",
            f"**Model-Estimated Risk**: `{risk_pct}` ({risk_tier})",
            f"**Prediction Confidence**: {unc['confidence_level']} — *{unc['confidence_description']}*\n",
            "---",
            "### 🔍 Why did the model output this result? (Feature Attributions)"
        ]
        
        if shap_exp.get("summary_explanation"):
            response_lines.append(f"> {shap_exp['summary_explanation']}\n")
            
        # Positive factors
        if shap_exp.get("why_factors_increasing_risk"):
            response_lines.append("**Top factors elevating the estimated risk:**")
            for f in shap_exp["why_factors_increasing_risk"][:4]:
                response_lines.append(f"• **{f['label']}**: {f['original_value']} *(Impact: +{f['shap_value']:.2f})*")
            response_lines.append("")
            
        # Negative factors
        if shap_exp.get("why_not_factors_decreasing_risk"):
            response_lines.append("**Top factors lowering or protecting the estimated risk:**")
            for f in shap_exp["why_not_factors_decreasing_risk"][:3]:
                response_lines.append(f"• **{f['label']}**: {f['original_value']} *(Impact: {f['shap_value']:.2f})*")
            response_lines.append("")
            
        # Disagreement notice
        if disagreement and disagreement.get("disagreement_detected"):
            response_lines.append(f"⚠️ **{disagreement['interpretation']}**\n")
            
        # Counterfactuals
        if counterfactuals and counterfactuals.get("scenarios"):
            response_lines.append("---")
            response_lines.append("### 💡 What Would Change the Prediction? (Mathematical Simulation)")
            scen = counterfactuals["scenarios"][0]
            response_lines.append(f"Under a **{scen['scenario_name']}**, the model estimate changes from `{risk_pct}` to `{scen['estimated_probability']*100:.1f}%`:")
            for ch in scen["modified_features"]:
                response_lines.append(f"• Change **{ch['label']}** from {ch['current_value']} {ch['unit']} to **{ch['scenario_value']} {ch['unit']}**")
            response_lines.append(f"\n*{counterfactuals['disclaimer']}*\n")
            
        response_lines.append("---")
        response_lines.append(f"ℹ️ *{assessment['disclaimer']}*")
        
        return "\n".join(response_lines)

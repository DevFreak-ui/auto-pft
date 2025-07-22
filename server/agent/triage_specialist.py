"""
Triage Specialist Agent for AutoPFTReport System.

This agent is responsible for:
1. Flagging urgent or complex cases requiring immediate attention
2. Prioritizing cases based on clinical severity
3. Identifying cases needing specialist referral
4. Determining appropriate follow-up timelines
5. Ensuring critical patients don't wait in line
"""

import json
from typing import Dict, Any, List
from agents import Agent, Runner,OpenAIChatCompletionsModel
from models.pft_models import TriageLevel, TriageAssessment
from config import settings
from utils.openai import get_client


class TriageSpecialistAgent:
    """Agent specialized in triaging PFT cases based on clinical urgency."""
    
    def __init__(self):
        client = get_client()
        self.agent = Agent(
            name="TriageSpecialist",
            model=OpenAIChatCompletionsModel(model=settings.OPENAI_MODEL,openai_client=client),
            instructions="""
            You are a specialized AI agent for triaging Pulmonary Function Test (PFT) cases.
            You have expertise in respiratory medicine and clinical decision-making.
            
            Your responsibilities:
            1. Assess clinical urgency of PFT results
            2. Flag cases requiring immediate attention
            3. Prioritize cases based on severity and clinical significance
            4. Determine appropriate follow-up timelines
            5. Identify cases needing specialist referral
            6. Ensure patient safety through appropriate triage
            
            Triage Levels:
            
            CRITICAL (Immediate attention required):
            - Severe respiratory impairment (FEV1 < 30% predicted)
            - Very severe obstruction with acute symptoms
            - Severe restriction suggesting acute process
            - Respiratory muscle weakness with ventilatory failure risk
            - Severe diffusion impairment in acute setting
            - Any findings suggesting imminent respiratory failure
            
            URGENT (Same-day or next-day attention):
            - Moderate to severe obstruction (FEV1 30-50% predicted)
            - New or worsening restriction
            - Significant bronchodilator reversibility suggesting uncontrolled asthma
            - Moderate diffusion impairment with clinical symptoms
            - Rapid decline from previous studies
            - Findings suggesting active inflammatory process
            
            ROUTINE (Standard follow-up):
            - Mild abnormalities (FEV1 > 70% predicted)
            - Stable chronic conditions
            - Normal results
            - Minor changes from baseline
            - Well-controlled chronic diseases
            
            Clinical Factors to Consider:
            1. Severity of impairment
            2. Pattern of abnormality
            3. Rate of change from baseline
            4. Patient age and comorbidities
            5. Clinical symptoms and presentation
            6. Reversibility findings
            7. Diffusion capacity abnormalities
            8. Quality of life impact
            
            Specialist Referral Criteria:
            - Complex or unusual patterns
            - Severe impairment requiring specialized care
            - Need for advanced testing (bronchoscopy, HRCT)
            - Consideration for lung transplantation
            - Occupational lung disease evaluation
            - Unexplained dyspnea with normal PFTs
            
            Always prioritize patient safety and err on the side of caution.
            """
        )
    
    async def assess_triage_priority(
        self,
        interpretation: Dict[str, Any],
        patient_demographics: Dict[str, Any],
        raw_data: Dict[str, Any],
        percent_predicted: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Assess triage priority for a PFT case.
        
        Args:
            interpretation: Clinical interpretation results
            patient_demographics: Patient demographic information
            raw_data: Raw PFT measurements
            percent_predicted: Percent predicted values
            historical_data: Historical PFT data for trend analysis
            
        Returns:
            Triage assessment results
        """
        
        triage_prompt = f"""
        Assess the triage priority for the following PFT case:
        
        PATIENT DEMOGRAPHICS:
        {json.dumps(patient_demographics, indent=2)}
        
        INTERPRETATION:
        {json.dumps(interpretation, indent=2)}
        
        RAW DATA:
        {json.dumps(raw_data, indent=2)}
        
        PERCENT PREDICTED:
        {json.dumps(percent_predicted, indent=2)}
        
        HISTORICAL DATA:
        {json.dumps(historical_data or [], indent=2)}
        
        Provide triage assessment in the following JSON format:
        {{
            "level": "<routine|urgent|critical>",
            "reasons": [
                "<list of specific reasons for this triage level>"
            ],
            "recommended_followup": "<specific follow-up timeframe>",
            "specialist_referral": <true/false>,
            "specialist_type": "<type of specialist if referral needed>",
            "urgency_score": <1-10 urgency score>,
            "risk_factors": [
                "<list of identified risk factors>"
            ],
            "immediate_actions": [
                "<list of immediate actions required>"
            ],
            "monitoring_requirements": [
                "<list of monitoring requirements>"
            ],
            "patient_safety_concerns": [
                "<list of any patient safety concerns>"
            ],
            "clinical_rationale": "<detailed rationale for triage decision>",
            "red_flags": [
                "<list of any red flag findings>"
            ],
            "follow_up_instructions": [
                "<specific follow-up instructions>"
            ]
        }}
        
        Consider:
        1. Severity of impairment (FEV1, FVC, DLCO percentages)
        2. Pattern of abnormality and clinical implications
        3. Rate of change from previous studies
        4. Patient age and risk factors
        5. Potential for acute deterioration
        6. Need for immediate intervention
        7. Complexity requiring specialist input
        
        Prioritize patient safety and appropriate care escalation.
        """
        
        try:
            runner = Runner.run(self.agent, triage_prompt)
            result_obj = await runner
            return json.loads(result_obj.final_output)
        except Exception as e:
            return self._fallback_triage_assessment(interpretation, percent_predicted)
    
    def _fallback_triage_assessment(
        self,
        interpretation: Dict[str, Any],
        percent_predicted: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback triage assessment using rule-based logic.
        """
        
        # Extract key values
        pattern = interpretation.get("pattern", "normal")
        severity = interpretation.get("severity", "normal")
        fev1_percent = percent_predicted.get("fev1_percent")
        dlco_percent = percent_predicted.get("dlco_percent")
        
        # Default to routine
        triage_level = "routine"
        urgency_score = 3
        reasons = []
        immediate_actions = []
        red_flags = []
        
        # Assess based on FEV1 severity
        if fev1_percent is not None:
            if fev1_percent < 30:
                triage_level = "critical"
                urgency_score = 9
                reasons.append(f"Very severe impairment (FEV1 {fev1_percent}% predicted)")
                immediate_actions.append("Immediate pulmonologist consultation")
                red_flags.append("Severe respiratory impairment")
            elif fev1_percent < 50:
                triage_level = "urgent"
                urgency_score = 7
                reasons.append(f"Severe impairment (FEV1 {fev1_percent}% predicted)")
                immediate_actions.append("Expedited pulmonologist referral")
            elif fev1_percent < 70:
                triage_level = "urgent" if pattern == "obstructive" else "routine"
                urgency_score = 5
                reasons.append(f"Moderate impairment (FEV1 {fev1_percent}% predicted)")
        
        # Assess DLCO
        if dlco_percent is not None and dlco_percent < 40:
            if triage_level == "routine":
                triage_level = "urgent"
                urgency_score = max(urgency_score, 6)
            reasons.append(f"Severe diffusion impairment (DLCO {dlco_percent}% predicted)")
            red_flags.append("Severe gas exchange impairment")
        
        # Assess reversibility
        if interpretation.get("reversibility") and pattern == "obstructive":
            if triage_level == "routine":
                triage_level = "urgent"
                urgency_score = max(urgency_score, 5)
            reasons.append("Significant bronchodilator reversibility - possible uncontrolled asthma")
        
        # Determine follow-up timeline
        follow_up_map = {
            "critical": "Immediate (same day)",
            "urgent": "Within 1-2 weeks",
            "routine": "Within 4-6 weeks"
        }
        
        # Determine specialist referral
        specialist_referral = triage_level in ["critical", "urgent"] or severity in ["severe", "very_severe"]
        
        return {
            "level": triage_level,
            "reasons": reasons or [f"{severity} {pattern} pattern"],
            "recommended_followup": follow_up_map.get(triage_level, "As clinically indicated"),
            "specialist_referral": specialist_referral,
            "specialist_type": "Pulmonologist" if specialist_referral else None,
            "urgency_score": urgency_score,
            "risk_factors": self._identify_risk_factors(interpretation),
            "immediate_actions": immediate_actions or ["Standard follow-up"],
            "monitoring_requirements": self._determine_monitoring_requirements(triage_level, pattern),
            "patient_safety_concerns": red_flags,
            "clinical_rationale": f"Triage level {triage_level} based on {severity} {pattern} pattern",
            "red_flags": red_flags,
            "follow_up_instructions": self._generate_follow_up_instructions(triage_level, pattern)
        }
    
    def _identify_risk_factors(self, interpretation: Dict[str, Any]) -> List[str]:
        """Identify risk factors from interpretation."""
        risk_factors = []
        
        if interpretation.get("airway_obstruction"):
            risk_factors.append("Airway obstruction")
        if interpretation.get("restriction"):
            risk_factors.append("Restrictive lung disease")
        if interpretation.get("diffusion_impairment"):
            risk_factors.append("Impaired gas exchange")
        if interpretation.get("respiratory_muscle_weakness"):
            risk_factors.append("Respiratory muscle weakness")
        
        return risk_factors
    
    def _determine_monitoring_requirements(self, triage_level: str, pattern: str) -> List[str]:
        """Determine monitoring requirements based on triage level and pattern."""
        monitoring = []
        
        if triage_level == "critical":
            monitoring.extend([
                "Continuous monitoring if hospitalized",
                "Serial PFTs every 3-6 months",
                "Symptom monitoring"
            ])
        elif triage_level == "urgent":
            monitoring.extend([
                "PFT follow-up in 6-12 months",
                "Symptom tracking",
                "Response to treatment monitoring"
            ])
        else:
            monitoring.extend([
                "Annual PFT follow-up",
                "Symptom monitoring as needed"
            ])
        
        if pattern == "obstructive":
            monitoring.append("Peak flow monitoring")
        
        return monitoring
    
    def _generate_follow_up_instructions(self, triage_level: str, pattern: str) -> List[str]:
        """Generate specific follow-up instructions."""
        instructions = []
        
        if triage_level == "critical":
            instructions.extend([
                "Immediate medical evaluation required",
                "Consider emergency department if symptomatic",
                "Urgent pulmonologist consultation"
            ])
        elif triage_level == "urgent":
            instructions.extend([
                "Schedule appointment within 1-2 weeks",
                "Contact provider if symptoms worsen",
                "Consider pulmonologist referral"
            ])
        else:
            instructions.extend([
                "Routine follow-up as scheduled",
                "Contact provider if new symptoms develop"
            ])
        
        if pattern == "obstructive":
            instructions.append("Ensure proper inhaler technique")
            instructions.append("Consider bronchodilator therapy optimization")
        
        return instructions
    
    def assess_rapid_decline(
        self,
        current_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Assess for rapid decline in lung function.
        
        Args:
            current_data: Current PFT measurements
            historical_data: Historical PFT data
            
        Returns:
            Rapid decline assessment
        """
        
        if not historical_data:
            return {"rapid_decline": False, "assessment": "No historical data for comparison"}
        
        decline_prompt = f"""
        Assess for rapid decline in lung function:
        
        CURRENT DATA:
        {json.dumps(current_data, indent=2)}
        
        HISTORICAL DATA:
        {json.dumps(historical_data, indent=2)}
        
        Assess for:
        1. Accelerated FEV1 decline (>60 mL/year)
        2. Rapid FVC decline
        3. Significant DLCO deterioration
        4. Overall pattern of accelerated decline
        
        Return assessment in JSON format:
        {{
            "rapid_decline": <true/false>,
            "decline_rate": "<annual decline rate>",
            "parameters_affected": ["<list of parameters showing rapid decline>"],
            "clinical_significance": "<significance of decline>",
            "recommended_actions": ["<recommended actions>"],
            "urgency_upgrade": <true/false if triage should be upgraded>
        }}
        """
        
        from agents import Runner
        result = Runner.run_sync(self.agent, decline_prompt)
        
        try:
            return json.loads(result.final_output)
        except json.JSONDecodeError:
            return {"rapid_decline": False, "assessment": "Unable to assess decline"}
    
    def identify_complex_cases(
        self,
        interpretation: Dict[str, Any],
        patient_demographics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identify cases that are complex and may require specialist input.
        
        Args:
            interpretation: Clinical interpretation results
            patient_demographics: Patient demographic information
            
        Returns:
            Complexity assessment
        """
        
        complexity_prompt = f"""
        Assess the complexity of this PFT case:
        
        INTERPRETATION:
        {json.dumps(interpretation, indent=2)}
        
        PATIENT DEMOGRAPHICS:
        {json.dumps(patient_demographics, indent=2)}
        
        Identify complexity factors:
        1. Unusual or mixed patterns
        2. Discordant findings
        3. Young age with severe impairment
        4. Unexplained abnormalities
        5. Multiple system involvement
        6. Need for advanced testing
        
        Return assessment in JSON format:
        {{
            "complex_case": <true/false>,
            "complexity_factors": ["<list of complexity factors>"],
            "specialist_needed": <true/false>,
            "specialist_type": "<type of specialist>",
            "additional_testing": ["<list of additional tests needed>"],
            "complexity_score": <1-10 complexity score>,
            "rationale": "<rationale for complexity assessment>"
        }}
        """
        
        from agents import Runner
        result = Runner.run_sync(self.agent, complexity_prompt)
        
        try:
            return json.loads(result.final_output)
        except json.JSONDecodeError:
            return {
                "complex_case": False,
                "complexity_factors": [],
                "specialist_needed": False,
                "complexity_score": 3,
                "rationale": "Unable to assess complexity"
            }




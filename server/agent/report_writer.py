"""
Report Writer Agent for AutoPFTReport System.

This agent is responsible for:
1. Creating clear, professional medical reports
2. Using appropriate medical terminology and language
3. Structuring reports in standard medical format
4. Generating patient-friendly summaries
5. Ensuring compliance with medical documentation standards
"""

import json
from typing import Dict, Any, List
from datetime import datetime
from agents import Agent, Runner,OpenAIChatCompletionsModel
from config import settings
from utils.openai import get_client
import re


class ReportWriterAgent:
    """Agent specialized in generating professional medical reports."""
    
    def __init__(self):
        client = get_client()
        self.agent = Agent(
            name="ReportWriter",
            model=OpenAIChatCompletionsModel(model=settings.OPENAI_MODEL,openai_client=client),
            instructions="""
            You are a specialized AI agent for writing professional medical reports for Pulmonary Function Tests (PFTs).
            You have expertise in medical writing, terminology, and documentation standards.
            
            Your responsibilities:
            1. Generate clear, professional medical reports
            2. Use appropriate medical terminology and language
            3. Structure reports in standard medical format
            4. Ensure accuracy and completeness
            5. Provide both technical and patient-friendly explanations
            6. Follow medical documentation best practices
            
            Report Structure Standards:
            1. PATIENT DEMOGRAPHICS
            2. TEST INFORMATION
            3. RESULTS SUMMARY
            4. INTERPRETATION
            5. CLINICAL SIGNIFICANCE
            6. RECOMMENDATIONS
            7. TECHNICAL DETAILS (if requested)
            
            Writing Guidelines:
            - Use clear, professional medical language
            - Avoid jargon when possible, explain technical terms
            - Be concise but comprehensive
            - Use standard medical abbreviations appropriately
            - Maintain objective, clinical tone
            - Include relevant normal ranges and reference values
            - Provide context for abnormal findings
            - Make recommendations specific and actionable
            
            Quality Standards:
            - Ensure all critical findings are highlighted
            - Verify consistency between data and interpretation
            - Include appropriate disclaimers and limitations
            - Follow institutional formatting guidelines
            - Maintain patient confidentiality standards
            """
        )
    
    async def generate_full_report(
        self,
        patient_demographics: Dict[str, Any],
        raw_data: Dict[str, Any],
        predicted_values: Dict[str, Any],
        percent_predicted: Dict[str, Any],
        interpretation: Dict[str, Any],
        triage: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None,
        test_date: str = None
    ) -> Dict[str, Any]:
        """
        Generate a complete professional medical report.
        
        Args:
            patient_demographics: Patient demographic information
            raw_data: Raw PFT measurements
            predicted_values: Predicted normal values
            percent_predicted: Percent predicted values
            interpretation: Clinical interpretation
            triage: Triage assessment
            historical_data: Historical PFT data
            test_date: Date of test
            
        Returns:
            Dictionary containing the complete report
        """
        
        report_prompt = f"""
        Generate a comprehensive, professional medical report for the following PFT results:
        
        PATIENT DEMOGRAPHICS:
        {json.dumps(patient_demographics, indent=2)}
        
        TEST DATE: {test_date or datetime.now().strftime("%Y-%m-%d")}
        
        RAW PFT DATA:
        {json.dumps(raw_data, indent=2)}
        
        PREDICTED VALUES:
        {json.dumps(predicted_values, indent=2)}
        
        PERCENT PREDICTED:
        {json.dumps(percent_predicted, indent=2)}
        
        INTERPRETATION:
        {json.dumps(interpretation, indent=2)}
        
        TRIAGE ASSESSMENT:
        {json.dumps(triage, indent=2)}
        
        HISTORICAL DATA:
        {json.dumps(historical_data or [], indent=2)}
        
        Generate a professional medical report in the following JSON format:
        {{
            "clinical_summary": "<concise clinical summary paragraph>",
            "detailed_interpretation": "<detailed interpretation section>",
            "recommendations_text": "<detailed recommendations section>",
            "technical_summary": "<technical data summary>",
            "patient_summary": "<patient-friendly summary>",
            "report_sections": {{
                "demographics": "<formatted demographics section>",
                "test_information": "<test information section>",
                "results_table": "<formatted results table>",
                "interpretation_section": "<detailed interpretation>",
                "clinical_significance": "<clinical significance section>",
                "recommendations": "<recommendations section>",
                "technical_notes": "<technical notes and quality metrics>",
                "historical_comparison": "<comparison with historical data if available>"
            }},
            "key_findings": [
                "<list of key findings for quick reference>"
            ],
            "critical_values": [
                "<list of any critical or urgent findings>"
            ],
            "follow_up_timeline": "<recommended follow-up timeline>",
            "report_quality_score": <1-10 quality assessment>,
            "completeness_score": <1-10 completeness assessment>
        }}
        
        Ensure the report is:
        1. Professionally written with appropriate medical terminology
        2. Clear and easy to understand for healthcare providers
        3. Comprehensive but concise
        4. Properly formatted with clear sections
        5. Includes all relevant clinical information
        6. Provides actionable recommendations
        7. Highlights any urgent or critical findings
        """
        
        try:
            from agents import Runner
            result = Runner.run(self.agent, report_prompt)
            result_obj = await result
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            report_data = json.loads(raw_output)
            return report_data

        except Exception as e:
            return self._generate_fallback_report(
                patient_demographics, raw_data, interpretation, triage
            )
    
    def _generate_fallback_report(
        self,
        patient_demographics: Dict[str, Any],
        raw_data: Dict[str, Any],
        interpretation: Dict[str, Any],
        triage: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a basic report using template-based approach.
        """
        
        # Extract key values
        age = patient_demographics.get("age", "Unknown")
        gender = patient_demographics.get("gender", "Unknown")
        fvc = raw_data.get("fvc", "Not measured")
        fev1 = raw_data.get("fev1", "Not measured")
        fev1_fvc_ratio = raw_data.get("fev1_fvc_ratio", "Not calculated")
        pattern = interpretation.get("pattern", "inconclusive")
        severity = interpretation.get("severity", "unknown")
        
        clinical_summary = f"""
        {age}-year-old {gender} patient underwent pulmonary function testing. 
        Results demonstrate {pattern} pattern with {severity} severity. 
        FVC: {fvc} L, FEV1: {fev1} L, FEV1/FVC: {fev1_fvc_ratio}%.
        """
        
        detailed_interpretation = f"""
        SPIROMETRY RESULTS:
        - FVC (Forced Vital Capacity): {fvc} L
        - FEV1 (Forced Expiratory Volume in 1 second): {fev1} L
        - FEV1/FVC Ratio: {fev1_fvc_ratio}%
        
        INTERPRETATION:
        The pulmonary function test demonstrates a {pattern} pattern. 
        {interpretation.get("interpretation_rationale", "No detailed rationale available.")}
        
        SEVERITY: {severity.replace("_", " ").title()}
        """
        
        recommendations = "\n".join([
            f"- {rec}" for rec in interpretation.get("recommendations", ["Follow-up as clinically indicated"])
        ])
        
        return {
            "clinical_summary": clinical_summary.strip(),
            "detailed_interpretation": detailed_interpretation.strip(),
            "recommendations_text": recommendations,
            "technical_summary": f"PFT performed with {pattern} pattern identified",
            "patient_summary": f"Your breathing test shows {pattern} pattern. Please discuss results with your doctor.",
            "report_sections": {
                "demographics": f"Age: {age}, Gender: {gender}",
                "test_information": f"Pulmonary Function Test performed on {datetime.now().strftime('%Y-%m-%d')}",
                "results_table": f"FVC: {fvc} L\nFEV1: {fev1} L\nFEV1/FVC: {fev1_fvc_ratio}%",
                "interpretation_section": detailed_interpretation,
                "clinical_significance": f"Results indicate {pattern} pattern with {severity} severity",
                "recommendations": recommendations,
                "technical_notes": "Automated report generation",
                "historical_comparison": "No historical data available"
            },
            "key_findings": interpretation.get("key_findings", [f"{pattern} pattern"]),
            "critical_values": [],
            "follow_up_timeline": triage.get("recommended_followup", "As clinically indicated"),
            "report_quality_score": 6,
            "completeness_score": 7
        }
    
    async def validate_report_quality(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the quality and completeness of a generated report.
        
        Args:
            report_data: Generated report data
            
        Returns:
            Quality assessment results
        """
        
        validation_prompt = f"""
        Assess the quality and completeness of the following medical report:
        
        {json.dumps(report_data, indent=2)}
        
        Evaluate:
        1. Completeness of information
        2. Clarity and readability
        3. Medical accuracy
        4. Professional formatting
        5. Appropriate use of terminology
        6. Actionable recommendations
        7. Patient safety considerations
        
        Return assessment in JSON format:
        {{
            "overall_quality": <1-10 score>,
            "completeness": <1-10 score>,
            "clarity": <1-10 score>,
            "medical_accuracy": <1-10 score>,
            "formatting": <1-10 score>,
            "recommendations_quality": <1-10 score>,
            "areas_for_improvement": ["<list of areas to improve>"],
            "strengths": ["<list of report strengths>"],
            "critical_issues": ["<list of any critical issues>"],
            "approval_status": "<approved|needs_revision|requires_review>"
        }}
        """
        
        try:
            
            from agents import Runner
            result = Runner.run(self.agent, validation_prompt)
            result_obj = await result
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
            
        except Exception:
            return {
                "overall_quality": 7,
                "completeness": 7,
                "clarity": 7,
                "medical_accuracy": 7,
                "formatting": 7,
                "recommendations_quality": 7,
                "areas_for_improvement": ["Unable to assess"],
                "strengths": ["Report generated successfully"],
                "critical_issues": [],
                "approval_status": "requires_review"
            }


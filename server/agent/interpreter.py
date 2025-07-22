"""
Interpreter Agent for AutoPFTReport System.

This agent is responsible for:
1. Analyzing PFT results using medical guidelines
2. Identifying obstructive, restrictive, and mixed patterns
3. Determining severity levels
4. Assessing bronchodilator reversibility
5. Providing clinical correlations and likely diagnoses
"""

import json
import logging
from typing import Dict, Any, List, Optional
from agents import Agent, Runner,OpenAIChatCompletionsModel
from config import settings
from utils.openai import get_client
import re


class InterpreterAgent:
    """Agent specialized in interpreting PFT results using medical guidelines."""

    def __init__(self):
        client = get_client()
        self.agent = Agent(
            name="Interpreter",
            model=OpenAIChatCompletionsModel(model=settings.OPENAI_MODEL,openai_client=client),
            instructions="""
            You are a specialized AI agent for interpreting Pulmonary Function Test (PFT) results.
            You have expert knowledge of respiratory medicine and PFT interpretation guidelines.
            
            Your responsibilities:
            1. Analyze PFT data using established medical guidelines (ATS/ERS, GOLD, AAFP)
            2. Identify interpretation patterns (Normal, Obstructive, Restrictive, Mixed)
            3. Determine severity levels (Normal, Mild, Moderate, Severe, Very Severe)
            4. Assess bronchodilator reversibility
            5. Identify specific abnormalities (airway obstruction, restriction, diffusion impairment)
            6. Provide likely clinical diagnoses
            7. Generate clinical recommendations
            
            Key Interpretation Guidelines:
            
            OBSTRUCTIVE PATTERN:
            - FEV1/FVC ratio < 70% (GOLD criteria for age 65+)
            - FEV1/FVC ratio < Lower Limit of Normal (ATS criteria for younger patients)
            - FEV1/FVC ratio < 85% (pediatric 5-18 years with symptoms)
            
            RESTRICTIVE PATTERN:
            - Normal FEV1/FVC ratio (≥70% or ≥LLN)
            - Reduced FVC (< 80% predicted or < LLN)
            - Reduced TLC (< 80% predicted) - gold standard for restriction
            
            MIXED PATTERN:
            - Reduced FEV1/FVC ratio (obstructive component)
            - Reduced FVC and TLC (restrictive component)
            
            SEVERITY GRADING (based on FEV1 % predicted):
            - Normal: ≥80%
            - Mild: 70-79%
            - Moderate: 50-69%
            - Severe: 30-49%
            - Very Severe: <30%
            
            REVERSIBILITY CRITERIA:
            - Adults: >12% AND >200 mL increase in FEV1 or FVC
            - Pediatric (5-18 years): >12% increase in FEV1 or FVC
            
            DIFFUSION IMPAIRMENT:
            - DLCO < 75% predicted indicates impairment
            - Consider pulmonary vascular disease, early ILD, emphysema
            
            Always provide evidence-based interpretations with clear reasoning.
            Consider patient demographics, clinical context, and historical trends.
            """
        )
    
    async def interpret_pft_results(
        self, 
        raw_data: Dict[str, Any],
        predicted_values: Dict[str, Any],
        percent_predicted: Dict[str, Any],
        patient_demographics: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Interpret PFT results and provide clinical analysis.
        
        Args:
            raw_data: Raw PFT measurements
            predicted_values: Predicted normal values
            percent_predicted: Percent predicted values
            patient_demographics: Patient demographic information
            historical_data: Historical PFT data for trend analysis
            
        Returns:
            Dictionary containing interpretation results
        """
        
        logger = logging.getLogger(__name__)
        logger.info(f"interpret_pft_results called with raw_data keys: {list(raw_data.keys())}")
        interpretation_prompt = f"""
        Interpret the following PFT results using established medical guidelines:
        
        PATIENT DEMOGRAPHICS:
        {json.dumps(patient_demographics, indent=2)}
        
        RAW PFT DATA:
        {json.dumps(raw_data, indent=2)}
        
        PREDICTED VALUES:
        {json.dumps(predicted_values, indent=2)}
        
        PERCENT PREDICTED:
        {json.dumps(percent_predicted, indent=2)}
        
        HISTORICAL DATA:
        {json.dumps(historical_data or [], indent=2)}
        
        Please provide a comprehensive interpretation in the following JSON format:
        {{
            "pattern": "<normal|obstructive|restrictive|mixed|inconclusive>",
            "severity": "<normal|mild|moderate|severe|very_severe>",
            "reversibility": <true/false/null>,
            "reversibility_percent": <percentage improvement if applicable>,
            "airway_obstruction": <true/false>,
            "restriction": <true/false>,
            "diffusion_impairment": <true/false>,
            "respiratory_muscle_weakness": <true/false>,
            "likely_diagnoses": [
                "<list of likely clinical diagnoses>"
            ],
            "recommendations": [
                "<list of clinical recommendations>"
            ],
            "interpretation_rationale": "<detailed explanation of interpretation>",
            "key_findings": [
                "<list of key abnormal findings>"
            ],
            "trend_analysis": "<analysis of trends if historical data available>",
            "clinical_significance": "<clinical significance of findings>",
            "follow_up_recommendations": [
                "<specific follow-up recommendations>"
            ]
        }}
        
        Base your interpretation on:
        1. ATS/ERS guidelines for PFT interpretation
        2. GOLD criteria for COPD diagnosis
        3. AAFP stepwise approach
        4. Patient age and demographics
        5. Historical trends if available
        
        Provide clear reasoning for your interpretation and specific evidence from the data.
        """
        
        try:
            runner = Runner.run(self.agent, interpretation_prompt)
            result_obj = await runner
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            logger.info(raw_output)
            return json.loads(raw_output)
        except Exception as e:
            logger.error(e)
            return self._fallback_interpretation(raw_data, predicted_values, percent_predicted)
    
    def _fallback_interpretation(
        self, 
        raw_data: Dict[str, Any],
        predicted_values: Dict[str, Any],
        percent_predicted: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback interpretation using rule-based logic.
        """
        interpretation = {
            "pattern": "inconclusive",
            "severity": "normal",
            "reversibility": None,
            "reversibility_percent": None,
            "airway_obstruction": False,
            "restriction": False,
            "diffusion_impairment": False,
            "respiratory_muscle_weakness": False,
            "likely_diagnoses": [],
            "recommendations": [],
            "interpretation_rationale": "Automated rule-based interpretation",
            "key_findings": [],
            "trend_analysis": "No historical data available",
            "clinical_significance": "Unable to determine clinical significance",
            "follow_up_recommendations": ["Manual review recommended"]
        }
        
        # Basic pattern recognition
        fev1_fvc_ratio = raw_data.get("fev1_fvc_ratio")
        fvc_percent = percent_predicted.get("fvc_percent")
        fev1_percent = percent_predicted.get("fev1_percent")
        tlc_percent = percent_predicted.get("tlc_percent")
        dlco_percent = percent_predicted.get("dlco_percent")
        
        # Check for obstruction
        if fev1_fvc_ratio is not None and fev1_fvc_ratio < 70:
            interpretation["airway_obstruction"] = True
            interpretation["pattern"] = "obstructive"
            interpretation["key_findings"].append(f"FEV1/FVC ratio {fev1_fvc_ratio}% indicates airway obstruction")
        
        # Check for restriction
        if fvc_percent is not None and fvc_percent < 80:
            interpretation["restriction"] = True
            if interpretation["pattern"] == "obstructive":
                interpretation["pattern"] = "mixed"
            else:
                interpretation["pattern"] = "restrictive"
            interpretation["key_findings"].append(f"FVC {fvc_percent}% predicted suggests restriction")
        
        # Determine severity based on FEV1
        if fev1_percent is not None:
            if fev1_percent >= 80:
                interpretation["severity"] = "normal"
            elif fev1_percent >= 70:
                interpretation["severity"] = "mild"
            elif fev1_percent >= 50:
                interpretation["severity"] = "moderate"
            elif fev1_percent >= 30:
                interpretation["severity"] = "severe"
            else:
                interpretation["severity"] = "very_severe"
        
        # Check for diffusion impairment
        if dlco_percent is not None and dlco_percent < 75:
            interpretation["diffusion_impairment"] = True
            interpretation["key_findings"].append(f"DLCO {dlco_percent}% predicted indicates diffusion impairment")
        
        # Set pattern to normal if no abnormalities found
        if not any([
            interpretation["airway_obstruction"],
            interpretation["restriction"],
            interpretation["diffusion_impairment"]
        ]):
            interpretation["pattern"] = "normal"
        
        return interpretation
    
    async def assess_reversibility(
        self, 
        pre_bd_data: Dict[str, Any], 
        post_bd_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess bronchodilator reversibility.
        
        Args:
            pre_bd_data: Pre-bronchodilator measurements
            post_bd_data: Post-bronchodilator measurements
            
        Returns:
            Reversibility assessment
        """
        reversibility_prompt = f"""
        Assess bronchodilator reversibility based on the following data:
        
        PRE-BRONCHODILATOR:
        FVC: {pre_bd_data.get("fvc")} L
        FEV1: {pre_bd_data.get("fev1")} L
        
        POST-BRONCHODILATOR:
        FVC: {post_bd_data.get("post_bd_fvc")} L
        FEV1: {post_bd_data.get("post_bd_fev1")} L
        
        Criteria for reversibility:
        - Adults: >12% AND >200 mL increase in FEV1 or FVC
        - Pediatric: >12% increase in FEV1 or FVC
        
        Return JSON with:
        {{
            "reversible": <true/false>,
            "fev1_improvement_percent": <percentage>,
            "fev1_improvement_ml": <absolute change in mL>,
            "fvc_improvement_percent": <percentage>,
            "fvc_improvement_ml": <absolute change in mL>,
            "meets_criteria": <true/false>,
            "interpretation": "<clinical interpretation>"
        }}
        """
        
        try:
            runner = Runner.run(self.agent, reversibility_prompt)
            result_obj = await runner
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return self._calculate_reversibility(pre_bd_data, post_bd_data)
        except Exception:
            return {"error": "Unable to assess reversibility"}
    
    def _calculate_reversibility(
        self, 
        pre_bd_data: Dict[str, Any], 
        post_bd_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate reversibility using direct computation.
        """
        pre_fev1 = pre_bd_data.get("fev1")
        post_fev1 = post_bd_data.get("post_bd_fev1")
        pre_fvc = pre_bd_data.get("fvc")
        post_fvc = post_bd_data.get("post_bd_fvc")
        
        result = {
            "reversible": False,
            "fev1_improvement_percent": None,
            "fev1_improvement_ml": None,
            "fvc_improvement_percent": None,
            "fvc_improvement_ml": None,
            "meets_criteria": False,
            "interpretation": "Unable to assess reversibility"
        }
        
        if pre_fev1 and post_fev1:
            fev1_change_ml = (post_fev1 - pre_fev1) * 1000  # Convert to mL
            fev1_change_percent = (fev1_change_ml / (pre_fev1 * 1000)) * 100
            
            result["fev1_improvement_ml"] = fev1_change_ml
            result["fev1_improvement_percent"] = fev1_change_percent
            
            # Check reversibility criteria for FEV1
            if fev1_change_percent > 12 and fev1_change_ml > 200:
                result["reversible"] = True
                result["meets_criteria"] = True
                result["interpretation"] = "Significant bronchodilator reversibility demonstrated"
        
        if pre_fvc and post_fvc:
            fvc_change_ml = (post_fvc - pre_fvc) * 1000
            fvc_change_percent = (fvc_change_ml / (pre_fvc * 1000)) * 100
            
            result["fvc_improvement_ml"] = fvc_change_ml
            result["fvc_improvement_percent"] = fvc_change_percent
            
            # Check reversibility criteria for FVC
            if fvc_change_percent > 12 and fvc_change_ml > 200:
                result["reversible"] = True
                result["meets_criteria"] = True
                result["interpretation"] = "Significant bronchodilator reversibility demonstrated"
        
        return result


"""
Data Specialist Agent for AutoPFTReport System.

This agent is responsible for:
1. Extracting PFT data from unstructured files
2. Standardizing the data format
3. Extracting patient historical data
4. Validating data quality and completeness
"""

import re
import json
from typing import Dict, Any, Optional, List
from agents import Agent, Runner,OpenAIChatCompletionsModel
from models.pft_models import (
    PFTRawData, PatientDemographics, PFTPredictedValues, 
    PFTPercentPredicted, HistoricalPFTData, PFTQualityMetrics
)
from datetime import datetime
from config import settings
import logging
# from main import client
from utils.openai import get_client
import re

logger = logging.getLogger(__name__)


class DataSpecialistAgent:
    
    """Agent specialized in extracting and standardizing PFT data."""
    
    def __init__(self):
        client = get_client()
        self.agent = Agent(
            name="DataSpecialist",
            model=OpenAIChatCompletionsModel(model=settings.OPENAI_MODEL,openai_client=client),
            instructions="""
            You are a specialized AI agent for extracting and standardizing Pulmonary Function Test (PFT) data.
            You have expertise in respiratory medicine and PFT data formats.
            
            Your responsibilities:
            1. Extract PFT measurements from various file formats
            2. Standardize data into consistent format
            3. Validate data quality and completeness
            4. Calculate predicted values when possible
            5. Identify and flag data quality issues
            
            Key PFT Parameters to Extract:
            - FVC (Forced Vital Capacity) in Liters
            - FEV1 (Forced Expiratory Volume in 1 second) in Liters
            - FEV1/FVC ratio as percentage
            - PEF (Peak Expiratory Flow) in L/s
            - FEF25-75 (Forced Expiratory Flow 25-75%) in L/s
            - TLC (Total Lung Capacity) in Liters
            - RV (Residual Volume) in Liters
            - DLCO (Diffusion Capacity) in mL/min/mmHg
            - Post-bronchodilator values when available
            
            Data Quality Checks:
            - Verify values are within physiological ranges
            - Check for missing critical parameters
            - Validate measurement units
            - Identify potential data entry errors
            
            Always provide structured, validated output with quality metrics.
            """
        )
    
    async def process_file(self, file_content: str, file_type: str) -> Dict[str, Any]:
        """
        Process PFT file and extract standardized data.
        
        Args:
            file_content: Raw file content as string
            file_type: Type of file (txt, pdf, csv, etc.)
            
        Returns:
            Dictionary containing extracted and standardized PFT data
        """
        
        logger.info(f"process_file: file_type={file_type}, content_length={len(file_content)}")
        extraction_prompt = f"""
        Extract and standardize PFT data from the following file content:
        
        FILE TYPE: {file_type}
        FILE CONTENT:
        {file_content}
        
        Please extract all available PFT measurements and return them in the following JSON format:
        {{
            "raw_data": {{
                "fvc": <value in liters>,
                "fev1": <value in liters>,
                "fev1_fvc_ratio": <percentage>,
                "pef": <value in L/s>,
                "fef25_75": <value in L/s>,
                "tlc": <value in liters>,
                "rv": <value in liters>,
                "dlco": <value in mL/min/mmHg>,
                "post_bd_fvc": <post-bronchodilator FVC if available>,
                "post_bd_fev1": <post-bronchodilator FEV1 if available>
            }},
            "predicted_values": {{
                "fvc": <predicted FVC>,
                "fev1": <predicted FEV1>,
                "tlc": <predicted TLC>,
                "dlco": <predicted DLCO>
            }},
            "percent_predicted": {{
                "fvc_percent": <FVC as % of predicted>,
                "fev1_percent": <FEV1 as % of predicted>,
                "tlc_percent": <TLC as % of predicted>,
                "dlco_percent": <DLCO as % of predicted>
            }},
            "quality_metrics": {{
                "data_completeness": <percentage 0-100>,
                "measurement_quality": "<excellent|good|fair|poor>",
                "missing_parameters": [<list of missing key parameters>],
                "data_quality_issues": [<list of any quality concerns>]
            }},
            "test_metadata": {{
                "test_date": "<date if available>",
                "technician": "<technician name if available>",
                "equipment": "<equipment info if available>",
                "test_quality": "<quality grade if available>"
            }}
        }}
        
        If a value is not available, use null. Ensure all numeric values are properly extracted and converted to appropriate units.
        """
        
        logger.info(f"DataSpecialistAgent.process_file called: type={file_type}, len={len(file_content)}")
        try:
            runner = Runner.run(self.agent, extraction_prompt)
            result_obj = await runner
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            logger.info(result_obj.final_output)
            return json.loads(raw_output)
        except Exception as e:
            logger.warning(e)
            return self._fallback_extraction(file_content)
    
    def _fallback_extraction(self, file_content: str) -> Dict[str, Any]:
        """
        Fallback extraction using regex patterns when AI extraction fails.
        """
        
        logger.info("DataSpecialistAgent._fallback_extraction called")
        # First, try CSV-style parsing if possible
        try:
            import csv
            from io import StringIO

            reader = csv.DictReader(StringIO(file_content))
            raw_data = {}
            for row in reader:
                for key in ['fvc','fev1','fev1_fvc_ratio','pef','fef25_75','tlc','rv','dlco']:
                    val = row.get(key.upper()) or row.get(key)
                    if val:
                        try:
                            raw_data[key] = float(val)
                        except ValueError:
                            pass
            if raw_data:
                completeness = len(raw_data) / 8 * 100
                missing = [k for k in ['fvc','fev1','fev1_fvc_ratio','pef','fef25_75','tlc','rv','dlco'] if k not in raw_data]
                return {
                    'raw_data': raw_data,
                    'predicted_values': {},
                    'percent_predicted': {},
                    'quality_metrics': {
                        'data_completeness': completeness,
                        'measurement_quality': 'good',
                        'missing_parameters': missing,
                        'data_quality_issues': []
                    },
                    'test_metadata': {
                        'test_date': None,
                        'technician': None,
                        'equipment': None,
                        'test_quality': None
                    }
                }
        except Exception:
            pass

        # Generic regex fallback for other formats
        patterns = {
            'fvc': r'FVC[:\s]*(\d+\.?\d*)',
            'fev1': r'FEV1[:\s]*(\d+\.?\d*)',
            'fev1_fvc_ratio': r'FEV1/FVC[:\s]*(\d+\.?\d*)',
            'pef': r'PEF[:\s]*(\d+\.?\d*)',
            'fef25_75': r'FEF25-75[:\s]*(\d+\.?\d*)',
            'tlc': r'TLC[:\s]*(\d+\.?\d*)',
            'rv': r'RV[:\s]*(\d+\.?\d*)',
            'dlco': r'DLCO[:\s]*(\d+\.?\d*)'
        }
        raw_data = {}
        for param, pattern in patterns.items():
            match = re.search(pattern, file_content, re.IGNORECASE)
            if match:
                try:
                    raw_data[param] = float(match.group(1))
                except ValueError:
                    pass
        completeness = len(raw_data) / len(patterns) * 100
        missing = [k for k in patterns if k not in raw_data]
        quality = 'excellent' if completeness >= 80 else 'good' if completeness >= 60 else 'fair' if completeness >= 40 else 'poor'
        return {
            'raw_data': raw_data,
            'predicted_values': {},
            'percent_predicted': {},
            'quality_metrics': {
                'data_completeness': completeness,
                'measurement_quality': quality,
                'missing_parameters': missing,
                'data_quality_issues': [] if completeness > 50 else ['low_data_completeness']
            },
            'test_metadata': {
                'test_date': None,
                'technician': None,
                'equipment': None,
                'test_quality': None
            }
        }
    
    def extract_numeric_value(self, text: str, pattern: str) -> Optional[float]:
        """
        Extract a numeric value using a regex pattern.
        
        Args:
            text: Text to search in
            pattern: Regex pattern to use
            
        Returns:
            Extracted numeric value or None
        """
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                return None
        return None
    
    async def validate_pft_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate PFT data for physiological ranges and consistency.
        
        Args:
            raw_data: Raw PFT measurements
            
        Returns:
            Validation results with issues and recommendations
        """
        
        logger.info("DataSpecialistAgent.validate_pft_data called")
        validation_prompt = f"""
        Validate the following PFT data for physiological ranges and consistency:
        
        PFT DATA:
        {json.dumps(raw_data, indent=2)}
        
        Check for:
        1. Values within normal physiological ranges
        2. Internal consistency (e.g., FEV1 should be ≤ FVC)
        3. Reasonable relationships between parameters
        4. Potential data entry errors
        
        Return validation results in JSON format:
        {{
            "is_valid": <true/false>,
            "validation_issues": [
                {{
                    "parameter": "<parameter name>",
                    "issue": "<description of issue>",
                    "severity": "<low|medium|high>",
                    "recommendation": "<suggested action>"
                }}
            ],
            "overall_quality": "<excellent|good|fair|poor>",
            "confidence_score": <0.0-1.0>
        }}
        """
        
        try:
            runner = Runner.run(self.agent, validation_prompt)
            result_obj = await runner
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
        except Exception:
            issues = []
            
            # Check FEV1 ≤ FVC
            if raw_data.get('fev1') and raw_data.get('fvc'):
                if raw_data['fev1'] > raw_data['fvc']:
                    issues.append({
                        "parameter": "fev1_fvc_consistency",
                        "issue": "FEV1 cannot be greater than FVC",
                        "severity": "high",
                        "recommendation": "Verify measurements"
                    })
            
            return {
                "is_valid": len(issues) == 0,
                "validation_issues": issues,
                "overall_quality": "fair",
                "confidence_score": 0.7
            }


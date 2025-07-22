"""
Medical Chatbot Agent for AutoPFTReport System.

This agent is responsible for:
1. Answering doctors' questions about PFT reports
2. Explaining rationale behind interpretations and recommendations
3. Providing educational information about PFT interpretation
4. Clarifying medical terminology and concepts
5. Offering clinical guidance and best practices
"""

import json
from typing import Dict, Any, List, Optional
from agents import Agent, Runner,OpenAIChatCompletionsModel
from models.pft_models import ChatMessage, ChatResponse
from config import settings
from utils.openai import get_client
import logging
import re

logger = logging.getLogger(__name__)

class MedicalChatbotAgent:
    """Agent specialized in answering medical questions about PFT reports."""
    
    def __init__(self):
        client = get_client()
        self.agent = Agent(
            name="MedicalChatbot",
            model=OpenAIChatCompletionsModel(model=settings.OPENAI_MODEL,openai_client=client),
            instructions="""
            You are a specialized AI medical chatbot for the AutoPFTReport system.
            You have expert knowledge in respiratory medicine, PFT interpretation, and clinical practice.
            
            Your responsibilities:
            1. Answer questions about PFT reports and interpretations
            2. Explain medical rationale behind recommendations
            3. Provide educational information about PFT concepts
            4. Clarify medical terminology and abbreviations
            5. Offer clinical guidance and best practices
            6. Help with differential diagnosis considerations
            7. Explain treatment implications of PFT findings
            
            Knowledge Areas:
            - Pulmonary function test interpretation
            - Respiratory physiology and pathophysiology
            - Obstructive and restrictive lung diseases
            - COPD, asthma, interstitial lung disease
            - Bronchodilator reversibility testing
            - Diffusion capacity interpretation
            - Respiratory muscle strength assessment
            - PFT quality control and technical aspects
            - Clinical guidelines (ATS/ERS, GOLD, AAFP)
            - Treatment implications and monitoring
            
            Communication Style:
            - Professional and knowledgeable
            - Clear and educational
            - Evidence-based responses
            - Appropriate medical terminology with explanations
            - Helpful and supportive
            - Acknowledge limitations when appropriate
            - Encourage clinical judgment and patient-specific considerations
            
            Safety Guidelines:
            - Always emphasize clinical correlation
            - Remind users to consider patient-specific factors
            - Encourage direct patient evaluation when appropriate
            - Acknowledge when specialist consultation may be needed
            - Never provide specific treatment recommendations without clinical context
            - Emphasize the importance of clinical judgment
            
            Response Format:
            - Provide clear, structured answers
            - Include relevant medical evidence or guidelines
            - Offer additional context when helpful
            - Suggest follow-up questions or considerations
            - Provide confidence level for responses
            """
        )
    
    async def answer_question(
        self,
        question: str,
        report_context: Optional[Dict[str, Any]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Answer a medical question about PFT reports.
        
        Args:
            question: The medical question to answer
            report_context: Related PFT report data for context
            user_context: Information about the user asking the question
            
        Returns:
            Structured response with answer and metadata
        """
        
        context_info = ""
        if report_context:
            context_info = f"""
            RELATED PFT REPORT CONTEXT:
            {json.dumps(report_context, indent=2)}
            """
        
        user_info = ""
        if user_context:
            user_info = f"""
            USER CONTEXT:
            {json.dumps(user_context, indent=2)}
            """
        
        question_prompt = f"""
        Please answer the following medical question about PFT interpretation:
        
        QUESTION: {question}
        
        {context_info}
        
        {user_info}
        
        Provide a comprehensive, evidence-based response in the following JSON format:
        {{
            "answer": "<detailed answer to the question>",
            "confidence": <0.0-1.0 confidence score>,
            "sources": ["<list of relevant guidelines, studies, or sources>"],
            "key_points": ["<list of key points from the answer>"],
            "clinical_pearls": ["<relevant clinical pearls or tips>"],
            "related_concepts": ["<related medical concepts to explore>"],
            "follow_up_questions": ["<suggested follow-up questions>"],
            "limitations": ["<any limitations or caveats to the answer>"],
            "recommendations": ["<clinical recommendations if appropriate>"],
            "educational_content": "<additional educational information>",
            "complexity_level": "<basic|intermediate|advanced>",
            "specialty_consultation": <true/false if specialist input recommended>
        }}
        
        Ensure your response is:
        1. Medically accurate and evidence-based
        2. Appropriate for the user's level of expertise
        3. Clinically relevant and practical
        4. Clear and well-structured
        5. Acknowledges limitations when appropriate
        """
        
        
        try:
            runner = Runner.run(self.agent, question_prompt)
            result_obj = await runner
            raw_output = result_obj.final_output.strip()

            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            data = json.loads(raw_output)
            logger.info(data)
            return data
        except Exception as e:
            logger.info(e)
            return self._generate_fallback_response(question)
    
    def _generate_fallback_response(self, question: str) -> Dict[str, Any]:
        """
        Generate a basic fallback response when JSON parsing fails.
        """
        return {
            "answer": f"I understand you're asking about: {question}. This is a complex medical question that would benefit from detailed analysis. Please consult current medical literature and consider specialist input for comprehensive guidance.",
            "confidence": 0.5,
            "sources": ["General medical knowledge"],
            "key_points": ["Complex medical question requiring detailed analysis"],
            "clinical_pearls": ["Always correlate PFT findings with clinical presentation"],
            "related_concepts": ["PFT interpretation", "Respiratory medicine"],
            "follow_up_questions": ["Could you provide more specific details about the case?"],
            "limitations": ["Limited context for comprehensive response"],
            "recommendations": ["Consult current medical literature", "Consider specialist input"],
            "educational_content": "PFT interpretation requires consideration of multiple factors including patient demographics, clinical presentation, and quality of testing.",
            "complexity_level": "intermediate",
            "specialty_consultation": True
        }
    
    async def explain_interpretation_rationale(
        self,
        interpretation: Dict[str, Any],
        raw_data: Dict[str, Any]
    ) -> str:
        """
        Explain the rationale behind a PFT interpretation.
        
        Args:
            interpretation: The PFT interpretation to explain
            raw_data: Raw PFT data used for interpretation
            
        Returns:
            Detailed explanation of the interpretation rationale
        """
        
        rationale_prompt = f"""
        Explain the medical rationale behind the following PFT interpretation:
        
        INTERPRETATION:
        {json.dumps(interpretation, indent=2)}
        
        RAW DATA:
        {json.dumps(raw_data, indent=2)}
        
        Provide a detailed explanation that covers:
        1. How the interpretation was derived from the data
        2. Which specific values led to the conclusions
        3. What medical guidelines were applied
        4. Why certain patterns were identified
        5. How severity was determined
        6. Rationale for recommendations
        
        Make the explanation educational and clear for medical professionals.
        """
        
        runner = Runner.run(self.agent, rationale_prompt)
        result_obj = await runner
        raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
        if raw_output.startswith("```") and raw_output.endswith("```"):
            # Remove language hint (e.g., ```json)
            raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
            raw_output = re.sub(r"\n```$", "", raw_output)
        return raw_output
    
    async def provide_differential_diagnosis_guidance(
        self,
        interpretation: Dict[str, Any],
        patient_demographics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Provide guidance on differential diagnosis considerations.
        
        Args:
            interpretation: PFT interpretation results
            patient_demographics: Patient demographic information
            
        Returns:
            Differential diagnosis guidance
        """
        
        differential_prompt = f"""
        Provide differential diagnosis guidance for the following case:
        
        PFT INTERPRETATION:
        {json.dumps(interpretation, indent=2)}
        
        PATIENT DEMOGRAPHICS:
        {json.dumps(patient_demographics, indent=2)}
        
        Provide guidance in JSON format:
        {{
            "primary_considerations": ["<most likely diagnoses>"],
            "secondary_considerations": ["<less likely but possible diagnoses>"],
            "distinguishing_features": {{
                "<diagnosis>": ["<features that support this diagnosis>"]
            }},
            "additional_testing": ["<tests that could help differentiate>"],
            "clinical_clues": ["<clinical features to look for>"],
            "red_flags": ["<concerning features requiring immediate attention>"],
            "monitoring_strategy": "<how to monitor and follow up>",
            "treatment_implications": ["<how diagnosis affects treatment>"]
        }}
        """
        
        from agents import Runner
        result = Runner.run(self.agent, differential_prompt)
        result_obj = await result
        try:

            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {"error": "Unable to generate differential diagnosis guidance"}
    
    async def explain_medical_terminology(self, term: str) -> Dict[str, Any]:
        """
        Explain medical terminology related to PFTs.
        
        Args:
            term: Medical term to explain
            
        Returns:
            Explanation of the medical term
        """
        
        terminology_prompt = f"""
        Explain the medical term "{term}" in the context of pulmonary function testing:
        
        Provide explanation in JSON format:
        {{
            "term": "{term}",
            "definition": "<clear definition>",
            "clinical_significance": "<why this term is important>",
            "normal_values": "<normal ranges if applicable>",
            "abnormal_implications": "<what abnormal values suggest>",
            "related_terms": ["<related medical terms>"],
            "measurement_method": "<how it's measured if applicable>",
            "clinical_examples": ["<examples of when this term is relevant>"],
            "common_misconceptions": ["<common misunderstandings>"]
        }}
        """
        
        from agents import Runner
        result = Runner.run(self.agent, terminology_prompt)
        result_obj = await result
        
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {
                "term": term,
                "definition": f"Medical term: {term}",
                "clinical_significance": "Consult medical literature for detailed information",
                "error": "Unable to generate detailed explanation"
            }
    
    async def provide_treatment_guidance(
        self,
        interpretation: Dict[str, Any],
        patient_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Provide general treatment guidance based on PFT findings.
        
        Args:
            interpretation: PFT interpretation results
            patient_context: Patient context information
            
        Returns:
            Treatment guidance information
        """
        
        treatment_prompt = f"""
        Provide general treatment guidance based on the following PFT findings:
        
        INTERPRETATION:
        {json.dumps(interpretation, indent=2)}
        
        PATIENT CONTEXT:
        {json.dumps(patient_context, indent=2)}
        
        Provide guidance in JSON format:
        {{
            "general_approach": "<overall treatment approach>",
            "pharmacological_considerations": ["<medication considerations>"],
            "non_pharmacological_interventions": ["<lifestyle and other interventions>"],
            "monitoring_parameters": ["<what to monitor during treatment>"],
            "treatment_goals": ["<specific treatment goals>"],
            "specialist_referral_indications": ["<when to refer to specialist>"],
            "patient_education_points": ["<key points for patient education>"],
            "follow_up_schedule": "<recommended follow-up timeline>",
            "contraindications": ["<important contraindications to consider>"],
            "special_considerations": ["<special factors to consider>"]
        }}
        
        Note: This is general guidance only. All treatment decisions should be individualized based on complete clinical assessment.
        """
        
        from agents import Runner
        result = Runner.run(self.agent, treatment_prompt)
        result_obj = await result
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {"error": "Unable to generate treatment guidance"}
    
    async def answer_technical_question(self, question: str) -> Dict[str, Any]:
        """
        Answer technical questions about PFT procedures and quality control.
        
        Args:
            question: Technical question about PFTs
            
        Returns:
            Technical answer and guidance
        """
        
        technical_prompt = f"""
        Answer the following technical question about pulmonary function testing:
        
        QUESTION: {question}
        
        Provide a technical response in JSON format:
        {{
            "answer": "<detailed technical answer>",
            "technical_details": ["<specific technical points>"],
            "quality_control_aspects": ["<quality control considerations>"],
            "troubleshooting_tips": ["<troubleshooting guidance>"],
            "best_practices": ["<best practice recommendations>"],
            "common_errors": ["<common technical errors to avoid>"],
            "equipment_considerations": ["<equipment-related factors>"],
            "standardization_guidelines": ["<relevant standardization guidelines>"],
            "interpretation_impact": "<how technical factors affect interpretation>"
        }}
        """
        
        from agents import Runner
        result = Runner.run(self.agent, technical_prompt)
        result_obj = await result
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {"error": "Unable to generate technical response"}
    
    def generate_educational_content(self, topic: str) -> str:
        """
        Generate educational content about PFT-related topics.
        
        Args:
            topic: Educational topic to cover
            
        Returns:
            Educational content
        """
        
        education_prompt = f"""
        Generate educational content about the following PFT-related topic:
        
        TOPIC: {topic}
        
        Create comprehensive educational content that includes:
        1. Overview of the topic
        2. Key concepts and principles
        3. Clinical relevance
        4. Practical applications
        5. Common pitfalls or misconceptions
        6. Current guidelines or recommendations
        7. Future directions or considerations
        
        Make the content suitable for medical professionals seeking to enhance their understanding.
        """
        
        from agents import Runner
        result = Runner.run_sync(self.agent, education_prompt)
        return result.final_output




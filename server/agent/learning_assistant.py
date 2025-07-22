"""
Learning Assistant Agent for AutoPFTReport System.

This agent is responsible for:
1. Analyzing doctor feedback and corrections
2. Identifying patterns in AI performance
3. Learning from expert edits and modifications
4. Improving system accuracy over time
5. Generating insights for system enhancement
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from agents import Agent, Runner,OpenAIChatCompletionsModel
from models.pft_models import DoctorFeedback
from config import settings
from utils.openai import get_client
import re


class LearningAssistantAgent:
    """
    Agent specialized in learning from feedback and improving system performance.
    """
    
    def __init__(self):
        client = get_client()
        self.agent = Agent(
            name="LearningAssistant",
            model=OpenAIChatCompletionsModel(model=settings.OPENAI_MODEL,openai_client=client),
            instructions="""
            You are a specialized AI agent for analyzing feedback and improving the AutoPFTReport system.
            You have expertise in machine learning, medical AI, and continuous improvement processes.
            
            Your responsibilities:
            1. Analyze doctor feedback and corrections
            2. Identify patterns in AI performance issues
            3. Learn from expert edits and modifications
            4. Generate insights for system improvement
            5. Track performance metrics over time
            6. Recommend system enhancements
            7. Identify training data needs
            8. Monitor quality trends
            
            Analysis Areas:
            
            FEEDBACK ANALYSIS:
            - Accuracy of interpretations
            - Quality of reports
            - Appropriateness of triage decisions
            - Common error patterns
            - Physician satisfaction metrics
            
            PERFORMANCE TRACKING:
            - Interpretation accuracy trends
            - Report quality scores
            - Triage appropriateness
            - Processing time metrics
            - User satisfaction ratings
            
            IMPROVEMENT IDENTIFICATION:
            - Systematic errors requiring correction
            - Knowledge gaps in medical guidelines
            - Pattern recognition improvements needed
            - Report template enhancements
            - Workflow optimization opportunities
            
            LEARNING STRATEGIES:
            - Identify high-quality feedback for training
            - Recognize expert consensus patterns
            - Detect edge cases requiring special handling
            - Monitor for guideline updates or changes
            - Track emerging medical knowledge
            
            Always focus on evidence-based improvements and maintain high standards for medical accuracy.
            Prioritize patient safety and clinical utility in all recommendations.
            """
        )
    
    async def analyze_feedback_batch(
        self,
        feedback_list: List[Dict[str, Any]],
        time_period: str = "last_month"
    ) -> Dict[str, Any]:
        """
        Analyze a batch of doctor feedback to identify improvement opportunities.
        
        Args:
            feedback_list: List of doctor feedback entries
            time_period: Time period for analysis
            
        Returns:
            Comprehensive feedback analysis
        """
        
        analysis_prompt = f"""
        Analyze the following batch of doctor feedback from {time_period}:
        
        FEEDBACK DATA:
        {json.dumps(feedback_list, indent=2)}
        
        Provide comprehensive analysis in JSON format:
        {{
            "summary_statistics": {{
                "total_feedback_entries": <number>,
                "average_interpretation_accuracy": <1-5 score>,
                "average_report_quality": <1-5 score>,
                "average_triage_appropriateness": <1-5 score>,
                "overall_satisfaction": <1-5 score>
            }},
            "performance_trends": {{
                "interpretation_accuracy_trend": "<improving|stable|declining>",
                "report_quality_trend": "<improving|stable|declining>",
                "triage_accuracy_trend": "<improving|stable|declining>",
                "trend_analysis": "<detailed trend analysis>"
            }},
            "common_issues": [
                {{
                    "issue": "<description of issue>",
                    "frequency": <number of occurrences>,
                    "severity": "<low|medium|high>",
                    "examples": ["<specific examples>"],
                    "suggested_fix": "<suggested improvement>"
                }}
            ],
            "accuracy_patterns": {{
                "most_accurate_areas": ["<areas where AI performs well>"],
                "least_accurate_areas": ["<areas needing improvement>"],
                "pattern_analysis": "<detailed pattern analysis>"
            }},
            "physician_insights": [
                "<key insights from physician feedback>"
            ],
            "improvement_recommendations": [
                {{
                    "recommendation": "<specific recommendation>",
                    "priority": "<high|medium|low>",
                    "implementation_effort": "<low|medium|high>",
                    "expected_impact": "<description of expected impact>",
                    "success_metrics": ["<how to measure success>"]
                }}
            ],
            "training_data_needs": [
                "<types of cases needed for training>"
            ],
            "knowledge_gaps": [
                "<identified knowledge gaps>"
            ],
            "quality_metrics": {{
                "error_rate": <percentage>,
                "false_positive_rate": <percentage>,
                "false_negative_rate": <percentage>,
                "clinical_agreement_rate": <percentage>
            }}
        }}
        
        Focus on actionable insights that can improve patient care and physician satisfaction.
        """
        
        runner = Runner.run(self.agent, analysis_prompt)
        result_obj = await runner
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(result_obj.final_output)
        except json.JSONDecodeError:
            return self._generate_fallback_analysis(feedback_list)
    
    def _generate_fallback_analysis(self, feedback_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate basic analysis when AI analysis fails.
        """
        
        if not feedback_list:
            return {"error": "No feedback data available for analysis"}
        
        # Calculate basic statistics
        total_entries = len(feedback_list)
        avg_interpretation = sum(f.get("interpretation_accuracy", 3) for f in feedback_list) / total_entries
        avg_quality = sum(f.get("report_quality", 3) for f in feedback_list) / total_entries
        avg_triage = sum(f.get("triage_appropriateness", 3) for f in feedback_list) / total_entries
        
        return {
            "summary_statistics": {
                "total_feedback_entries": total_entries,
                "average_interpretation_accuracy": round(avg_interpretation, 2),
                "average_report_quality": round(avg_quality, 2),
                "average_triage_appropriateness": round(avg_triage, 2),
                "overall_satisfaction": round((avg_interpretation + avg_quality + avg_triage) / 3, 2)
            },
            "performance_trends": {
                "interpretation_accuracy_trend": "stable",
                "report_quality_trend": "stable",
                "triage_accuracy_trend": "stable",
                "trend_analysis": "Insufficient data for trend analysis"
            },
            "common_issues": [],
            "improvement_recommendations": [
                {
                    "recommendation": "Collect more feedback data for detailed analysis",
                    "priority": "high",
                    "implementation_effort": "low",
                    "expected_impact": "Better understanding of system performance"
                }
            ],
            "analysis_method": "fallback_basic_statistics"
        }
    
    async def identify_learning_opportunities(
        self,
        original_interpretation: Dict[str, Any],
        corrected_interpretation: Dict[str, Any],
        case_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identify specific learning opportunities from expert corrections.
        
        Args:
            original_interpretation: AI's original interpretation
            corrected_interpretation: Expert's corrected interpretation
            case_context: Context about the case
            
        Returns:
            Learning opportunity analysis
        """
        
        learning_prompt = f"""
        Analyze the differences between AI interpretation and expert correction to identify learning opportunities:
        
        ORIGINAL AI INTERPRETATION:
        {json.dumps(original_interpretation, indent=2)}
        
        EXPERT CORRECTED INTERPRETATION:
        {json.dumps(corrected_interpretation, indent=2)}
        
        CASE CONTEXT:
        {json.dumps(case_context, indent=2)}
        
        Identify learning opportunities in JSON format:
        {{
            "interpretation_differences": [
                {{
                    "parameter": "<parameter that differed>",
                    "ai_value": "<AI's interpretation>",
                    "expert_value": "<expert's interpretation>",
                    "significance": "<clinical significance of difference>",
                    "learning_point": "<what the AI should learn>"
                }}
            ],
            "error_classification": {{
                "error_type": "<systematic|random|knowledge_gap|guideline_interpretation>",
                "severity": "<minor|moderate|major|critical>",
                "clinical_impact": "<potential clinical impact>",
                "root_cause": "<likely root cause of error>"
            }},
            "knowledge_gaps": [
                "<specific knowledge gaps identified>"
            ],
            "pattern_recognition_issues": [
                "<pattern recognition problems identified>"
            ],
            "guideline_application_issues": [
                "<issues with guideline application>"
            ],
            "training_recommendations": [
                {{
                    "training_type": "<type of training needed>",
                    "focus_area": "<specific focus area>",
                    "priority": "<high|medium|low>",
                    "expected_improvement": "<expected improvement>"
                }}
            ],
            "case_complexity_factors": [
                "<factors that made this case complex>"
            ],
            "improvement_strategies": [
                "<specific strategies to prevent similar errors>"
            ]
        }}
        """
        
        runner = Runner.run(self.agent, learning_prompt)
        result_obj = await runner
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(result_obj.final_output)
        except json.JSONDecodeError:
            return {"error": "Unable to analyze learning opportunities"}
    
    async def track_performance_metrics(
        self,
        metrics_data: List[Dict[str, Any]],
        time_window: str = "30_days"
    ) -> Dict[str, Any]:
        """
        Track and analyze performance metrics over time.
        
        Args:
            metrics_data: Performance metrics data
            time_window: Time window for analysis
            
        Returns:
            Performance tracking analysis
        """
        
        metrics_prompt = f"""
        Analyze performance metrics over the {time_window} time window:
        
        METRICS DATA:
        {json.dumps(metrics_data, indent=2)}
        
        Provide performance tracking analysis in JSON format:
        {{
            "metric_trends": {{
                "accuracy_trend": {{
                    "direction": "<improving|stable|declining>",
                    "rate_of_change": <percentage change>,
                    "statistical_significance": <true/false>
                }},
                "quality_trend": {{
                    "direction": "<improving|stable|declining>",
                    "rate_of_change": <percentage change>,
                    "statistical_significance": <true/false>
                }},
                "efficiency_trend": {{
                    "direction": "<improving|stable|declining>",
                    "rate_of_change": <percentage change>,
                    "statistical_significance": <true/false>
                }}
            }},
            "performance_benchmarks": {{
                "current_accuracy": <percentage>,
                "target_accuracy": <percentage>,
                "gap_analysis": "<analysis of performance gap>",
                "benchmark_comparison": "<comparison to benchmarks>"
            }},
            "outlier_analysis": [
                {{
                    "outlier_type": "<type of outlier>",
                    "frequency": <number>,
                    "impact": "<impact description>",
                    "investigation_needed": <true/false>
                }}
            ],
            "improvement_trajectory": {{
                "projected_improvement": "<projection of future improvement>",
                "time_to_target": "<estimated time to reach targets>",
                "confidence_interval": "<confidence in projections>"
            }},
            "actionable_insights": [
                "<specific actionable insights from metrics>"
            ]
        }}
        """
        
        runner = Runner.run(self.agent, metrics_prompt)
        result_obj = await runner
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(result_obj.final_output)
        except json.JSONDecodeError:
            return {"error": "Unable to analyze performance metrics"}
    
    async def generate_improvement_plan(
        self,
        analysis_results: Dict[str, Any],
        priority_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive improvement plan based on analysis results.
        
        Args:
            analysis_results: Results from feedback and performance analysis
            priority_areas: Specific areas to prioritize for improvement
            
        Returns:
            Detailed improvement plan
        """
        
        plan_prompt = f"""
        Generate a comprehensive improvement plan based on the following analysis:
        
        ANALYSIS RESULTS:
        {json.dumps(analysis_results, indent=2)}
        
        PRIORITY AREAS:
        {json.dumps(priority_areas or [], indent=2)}
        
        Create an improvement plan in JSON format:
        {{
            "executive_summary": "<high-level summary of improvement plan>",
            "improvement_initiatives": [
                {{
                    "initiative_name": "<name of initiative>",
                    "description": "<detailed description>",
                    "priority": "<high|medium|low>",
                    "timeline": "<implementation timeline>",
                    "resources_required": ["<required resources>"],
                    "success_metrics": ["<how to measure success>"],
                    "risk_assessment": "<potential risks and mitigation>",
                    "expected_outcomes": ["<expected outcomes>"]
                }}
            ],
            "quick_wins": [
                {{
                    "action": "<quick win action>",
                    "effort": "<low|medium|high>",
                    "impact": "<low|medium|high>",
                    "timeline": "<implementation timeline>"
                }}
            ],
            "long_term_goals": [
                {{
                    "goal": "<long-term goal>",
                    "target_date": "<target completion date>",
                    "milestones": ["<key milestones>"],
                    "success_criteria": ["<success criteria>"]
                }}
            ],
            "resource_requirements": {{
                "technical_resources": ["<technical resources needed>"],
                "human_resources": ["<human resources needed>"],
                "training_requirements": ["<training requirements>"],
                "infrastructure_needs": ["<infrastructure needs>"]
            }},
            "implementation_roadmap": [
                {{
                    "phase": "<phase number>",
                    "duration": "<phase duration>",
                    "activities": ["<activities in this phase>"],
                    "deliverables": ["<expected deliverables>"],
                    "dependencies": ["<dependencies>"]
                }}
            ],
            "monitoring_strategy": {{
                "key_metrics": ["<metrics to monitor>"],
                "review_frequency": "<how often to review>",
                "reporting_structure": "<how to report progress>",
                "adjustment_triggers": ["<when to adjust the plan>"]
            }}
        }}
        """
        
        runner = Runner.run(self.agent, plan_prompt)
        result_obj = await runner
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(result_obj.final_output)
        except json.JSONDecodeError:
            return {"error": "Unable to generate improvement plan"}
    
    async def analyze_edge_cases(
        self,
        edge_case_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze edge cases to improve system robustness.
        
        Args:
            edge_case_data: Data about edge cases encountered
            
        Returns:
            Edge case analysis and recommendations
        """
        
        edge_case_prompt = f"""
        Analyze the following edge cases to improve system robustness:
        
        EDGE CASE DATA:
        {json.dumps(edge_case_data, indent=2)}
        
        Provide edge case analysis in JSON format:
        {{
            "edge_case_categories": [
                {{
                    "category": "<category of edge case>",
                    "frequency": <number of occurrences>,
                    "complexity": "<low|medium|high>",
                    "current_handling": "<how system currently handles>",
                    "improvement_needed": <true/false>
                }}
            ],
            "common_patterns": [
                "<common patterns in edge cases>"
            ],
            "system_limitations": [
                "<identified system limitations>"
            ],
            "robustness_improvements": [
                {{
                    "improvement": "<specific improvement>",
                    "target_edge_cases": ["<edge cases this addresses>"],
                    "implementation_complexity": "<low|medium|high>",
                    "expected_benefit": "<expected benefit>"
                }}
            ],
            "special_handling_rules": [
                {{
                    "rule": "<special handling rule>",
                    "trigger_conditions": ["<when to apply this rule>"],
                    "actions": ["<actions to take>"],
                    "validation_criteria": ["<how to validate effectiveness>"]
                }}
            ],
            "testing_recommendations": [
                "<recommendations for testing edge cases>"
            ]
        }}
        """
        
        runner = Runner.run(self.agent, edge_case_prompt)
        result_obj = await runner
        try:
            raw_output = result_obj.final_output.strip()
            # Remove markdown-style triple backticks if present
            if raw_output.startswith("```") and raw_output.endswith("```"):
                # Remove language hint (e.g., ```json)
                raw_output = re.sub(r"^```[a-zA-Z]*\n", "", raw_output)
                raw_output = re.sub(r"\n```$", "", raw_output)
            return json.loads(result_obj.final_output)
        except json.JSONDecodeError:
            return {"error": "Unable to analyze edge cases"}
    
    async def generate_learning_report(
        self,
        time_period: str,
        feedback_data: List[Dict[str, Any]],
        performance_data: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a comprehensive learning and improvement report.
        
        Args:
            time_period: Time period for the report
            feedback_data: Feedback data for the period
            performance_data: Performance data for the period
            
        Returns:
            Comprehensive learning report
        """
        
        report_prompt = f"""
        Generate a comprehensive learning and improvement report for {time_period}:
        
        FEEDBACK DATA:
        {json.dumps(feedback_data, indent=2)}
        
        PERFORMANCE DATA:
        {json.dumps(performance_data, indent=2)}
        
        Create a detailed report covering:
        1. Executive Summary
        2. Performance Overview
        3. Key Learning Points
        4. Improvement Achievements
        5. Ongoing Challenges
        6. Future Recommendations
        7. Action Items
        
        Format as a professional report suitable for stakeholders.
        """
        
        runner = Runner.run(self.agent, report_prompt)
        result_obj = await runner
        return result_obj.final_output




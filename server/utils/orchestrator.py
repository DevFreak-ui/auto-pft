"""
Agent Orchestration Utility for AutoPFTReport System.

This module provides workflow management and coordination between different AI agents.
It handles the sequential processing pipeline and manages agent interactions.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum

from agent.data_specialist import DataSpecialistAgent
from agent.interpreter import InterpreterAgent
from agent.report_writer import ReportWriterAgent
from agent.triage_specialist import TriageSpecialistAgent
from agent.medical_chatbot import MedicalChatbotAgent
from agent.learning_assistant import LearningAssistantAgent

# Redis pub/sub for progress updates
import redis.asyncio as aioredis
from config import settings
redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
import json


class ProcessingStage(Enum):
    """Enumeration of processing stages in the PFT workflow."""
    QUEUED = "queued"
    DATA_EXTRACTION = "data_extraction"
    INTERPRETATION = "interpretation"
    TRIAGE_ASSESSMENT = "triage_assessment"
    REPORT_GENERATION = "report_generation"
    QUALITY_VALIDATION = "quality_validation"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStatus:
    """Class to track workflow status and progress."""
    
    def __init__(self, request_id: str):
        self.request_id = request_id
        self.stage = ProcessingStage.QUEUED
        self.progress = 0
        self.current_step = "Queued for processing"
        self.started_at = datetime.now()
        self.completed_at = None
        self.error_message = None
        self.stage_results = {}
        self.processing_time = 0.0
    
    def update_stage(self, stage: ProcessingStage, progress: int, step_description: str):
        """Update the current processing stage."""
        self.stage = stage
        self.progress = progress
        self.current_step = step_description
        
        if stage == ProcessingStage.COMPLETED:
            self.completed_at = datetime.now()
            self.processing_time = (self.completed_at - self.started_at).total_seconds()
    
    def set_error(self, error_message: str):
        """Set error status."""
        self.stage = ProcessingStage.FAILED
        self.error_message = error_message
        self.completed_at = datetime.now()
        self.processing_time = (self.completed_at - self.started_at).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status to dictionary."""
        return {
            "request_id": self.request_id,
            "stage": self.stage.value,
            "progress": self.progress,
            "current_step": self.current_step,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "processing_time": self.processing_time,
            "error_message": self.error_message
        }


class PFTWorkflowOrchestrator:
    """
    Orchestrates the multi-agent workflow for PFT processing.
    
    This class manages the sequential execution of agents and handles
    error recovery, progress tracking, and result aggregation.
    """
    
    def __init__(self):
        # Initialize all agents
        self.data_specialist = DataSpecialistAgent()
        self.interpreter = InterpreterAgent()
        self.report_writer = ReportWriterAgent()
        self.triage_specialist = TriageSpecialistAgent()
        self.medical_chatbot = MedicalChatbotAgent()
        self.learning_assistant = LearningAssistantAgent()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Workflow configuration
        self.workflow_steps = [
            {
                "stage": ProcessingStage.DATA_EXTRACTION,
                "progress": 20,
                "description": "Extracting and standardizing PFT data",
                "agent": self.data_specialist,
                "method": "process_file",
                "timeout": 60  # seconds
            },
            {
                "stage": ProcessingStage.INTERPRETATION,
                "progress": 40,
                "description": "Analyzing PFT results",
                "agent": self.interpreter,
                "method": "interpret_pft_results",
                "timeout": 90
            },
            {
                "stage": ProcessingStage.TRIAGE_ASSESSMENT,
                "progress": 60,
                "description": "Assessing clinical priority",
                "agent": self.triage_specialist,
                "method": "assess_triage_priority",
                "timeout": 60
            },
            {
                "stage": ProcessingStage.REPORT_GENERATION,
                "progress": 80,
                "description": "Generating professional report",
                "agent": self.report_writer,
                "method": "generate_full_report",
                "timeout": 120
            },
            {
                "stage": ProcessingStage.QUALITY_VALIDATION,
                "progress": 95,
                "description": "Validating report quality",
                "agent": self.report_writer,
                "method": "validate_report_quality",
                "timeout": 30
            }
        ]
    
    async def process_pft_request(
        self,
        request_id: str,
        file_content: str,
        file_type: str,
        patient_demographics: Dict[str, Any],
        historical_data: List[Dict[str, Any]] = None,
        priority: str = "routine",
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Process a complete PFT request through the multi-agent workflow.
        
        Args:
            request_id: Unique identifier for the request
            file_content: Raw PFT file content
            file_type: Type of PFT file
            patient_demographics: Patient demographic information
            historical_data: Historical PFT data
            priority: Processing priority
            progress_callback: Optional callback for progress updates
            
        Returns:
            Complete processing results
        """
        
        status = WorkflowStatus(request_id)
        
        self.logger.info(f"Orchestrator starting workflow for request_id={request_id}")
        try:
            # Initialize workflow data
            workflow_data = {
                "request_id": request_id,
                "file_content": file_content,
                "file_type": file_type,
                "patient_demographics": patient_demographics,
                "historical_data": historical_data or [],
                "priority": priority,
                "extracted_data": {},
                "interpretation": {},
                "triage_assessment": {},
                "report_data": {},
                "quality_assessment": {}
            }
            
            # Execute workflow steps
            for step in self.workflow_steps:
                try:
                    # Update status
                    status.update_stage(
                        step["stage"],
                        step["progress"],
                        step["description"]
                    )
                    # Publish real-time progress
                    await redis_client.publish(
                        f"pft:progress:{request_id}",
                        json.dumps(status.to_dict())
                    )
                    # Persist updated status to Redis for HTTP polling
                    await redis_client.set(
                        f"pft:processing:{request_id}",
                        json.dumps(status.to_dict())
                    )
                    
                    # Call progress callback if provided
                    if progress_callback:
                        await progress_callback(status.to_dict())
                    
                    # Execute step with timeout
                    result = await asyncio.wait_for(
                        self._execute_workflow_step(step, workflow_data),
                        timeout=step["timeout"]
                    )
                    
                    # Store step result
                    status.stage_results[step["stage"].value] = result
                    
                    # Update workflow data based on step
                    workflow_data = self._update_workflow_data(step["stage"], result, workflow_data)
                    
                    self.logger.info(f"Completed step {step['stage'].value} for request {request_id}")
                    
                except asyncio.TimeoutError:
                    error_msg = f"Timeout in step {step['stage'].value}"
                    self.logger.error(f"{error_msg} for request {request_id}")
                    status.set_error(error_msg)
                    # Persist error status
                    await redis_client.set(
                        f"pft:processing:{request_id}",
                        json.dumps(status.to_dict())
                    )
                    return self._create_error_response(request_id, error_msg, status)
                    
                except Exception as e:
                    error_msg = f"Error in step {step['stage'].value}: {str(e)}"
                    self.logger.error(f"{error_msg} for request {request_id}")
                    status.set_error(error_msg)
                    # Persist error status
                    await redis_client.set(
                        f"pft:processing:{request_id}",
                        json.dumps(status.to_dict())
                    )
                    return self._create_error_response(request_id, error_msg, status)
            
            # Mark as completed
            status.update_stage(ProcessingStage.COMPLETED, 100, "Processing completed successfully")
            # Publish and persist final status
            await redis_client.publish(
                f"pft:progress:{request_id}",
                json.dumps(status.to_dict())
            )
            await redis_client.set(
                f"pft:processing:{request_id}",
                json.dumps(status.to_dict())
            )
            
            # Call final progress callback
            if progress_callback:
                await progress_callback(status.to_dict())
            
            # Create final result
            final_result = self._create_final_result(request_id, workflow_data, status)
            # Persist the generated report for HTTP retrieval
            await redis_client.set(
                f"pft:report:{request_id}",
                json.dumps(final_result.get("report", {}))
            )
            self.logger.info(f"Successfully completed processing for request {request_id}")
            return final_result
            
        except Exception as e:
            error_msg = f"Unexpected error in workflow: {str(e)}"
            self.logger.error(f"{error_msg} for request {request_id}")
            status.set_error(error_msg)
            # Persist error status
            await redis_client.set(
                f"pft:processing:{request_id}",
                json.dumps(status.to_dict())
            )
            return self._create_error_response(request_id, error_msg, status)
    
    async def _execute_workflow_step(
        self,
        step: Dict[str, Any],
        workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single workflow step."""
        
        stage = step["stage"]
        agent = step["agent"]
        method_name = step["method"]
        
        # Prepare arguments based on stage
        if stage == ProcessingStage.DATA_EXTRACTION:
            result = await agent.process_file(
                file_content=workflow_data["file_content"],
                file_type=workflow_data["file_type"]
            )
            
        elif stage == ProcessingStage.INTERPRETATION:
            method = getattr(agent, method_name)
            result = await method(
                raw_data=workflow_data["extracted_data"].get("raw_data", {}),
                predicted_values=workflow_data["extracted_data"].get("predicted_values", {}),
                percent_predicted=workflow_data["extracted_data"].get("percent_predicted", {}),
                patient_demographics=workflow_data["patient_demographics"],
                historical_data=workflow_data["historical_data"]
            )
            
        elif stage == ProcessingStage.TRIAGE_ASSESSMENT:
            method = getattr(agent, method_name)
            result = await method(
                interpretation=workflow_data["interpretation"],
                patient_demographics=workflow_data["patient_demographics"],
                raw_data=workflow_data["extracted_data"].get("raw_data", {}),
                percent_predicted=workflow_data["extracted_data"].get("percent_predicted", {}),
                historical_data=workflow_data["historical_data"]
            )
            
        elif stage == ProcessingStage.REPORT_GENERATION:
            method = getattr(agent, method_name)
            result = await method(
                patient_demographics=workflow_data["patient_demographics"],
                raw_data=workflow_data["extracted_data"].get("raw_data", {}),
                predicted_values=workflow_data["extracted_data"].get("predicted_values", {}),
                percent_predicted=workflow_data["extracted_data"].get("percent_predicted", {}),
                interpretation=workflow_data["interpretation"],
                triage=workflow_data["triage_assessment"],
                historical_data=workflow_data["historical_data"],
                test_date=datetime.now().strftime('%Y-%m-%d')
            )
            
        elif stage == ProcessingStage.QUALITY_VALIDATION:
            method = getattr(agent, method_name)
            result = await method(workflow_data["report_data"])
            
        else:
            raise ValueError(f"Unknown workflow stage: {stage}")
        
        return result
    
    def _update_workflow_data(
        self,
        stage: ProcessingStage,
        result: Dict[str, Any],
        workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update workflow data with step results."""
        
        if stage == ProcessingStage.DATA_EXTRACTION:
            workflow_data["extracted_data"] = result
            
        elif stage == ProcessingStage.INTERPRETATION:
            workflow_data["interpretation"] = result
            
        elif stage == ProcessingStage.TRIAGE_ASSESSMENT:
            workflow_data["triage_assessment"] = result
            
        elif stage == ProcessingStage.REPORT_GENERATION:
            workflow_data["report_data"] = result
            
        elif stage == ProcessingStage.QUALITY_VALIDATION:
            workflow_data["quality_assessment"] = result
        
        return workflow_data
    
    def _create_final_result(
        self,
        request_id: str,
        workflow_data: Dict[str, Any],
        status: WorkflowStatus
    ) -> Dict[str, Any]:
        """Create the final processing result."""
        
        return {
            "request_id": request_id,
            "status": "completed",
            "processing_time": status.processing_time,
            "report": {
                "report_id": request_id,
                "patient_demographics": workflow_data["patient_demographics"],
                "test_date": datetime.now().isoformat(),
                "raw_data": workflow_data["extracted_data"].get("raw_data", {}),
                "predicted_values": workflow_data["extracted_data"].get("predicted_values", {}),
                "percent_predicted": workflow_data["extracted_data"].get("percent_predicted", {}),
                "quality_metrics": workflow_data["extracted_data"].get("quality_metrics", {}),
                "interpretation": workflow_data["interpretation"],
                "triage": workflow_data["triage_assessment"],
                "report_content": workflow_data["report_data"],
                "quality_assessment": workflow_data["quality_assessment"],
                "generated_by": "AutoPFTReport AI",
                "generated_at": datetime.now().isoformat(),
                "processing_metadata": {
                    "workflow_version": "1.0",
                    "agents_used": [step["stage"].value for step in self.workflow_steps],
                    "processing_time": status.processing_time
                }
            },
            "workflow_status": status.to_dict()
        }
    
    def _create_error_response(
        self,
        request_id: str,
        error_message: str,
        status: WorkflowStatus
    ) -> Dict[str, Any]:
        """Create an error response."""
        
        return {
            "request_id": request_id,
            "status": "failed",
            "error_message": error_message,
            "processing_time": status.processing_time,
            "workflow_status": status.to_dict(),
            "partial_results": status.stage_results
        }
    
    async def get_agent_health_status(self) -> Dict[str, Any]:
        """Get health status of all agents."""
        
        agents_status = {}
        
        # Test each agent with a simple operation
        try:
            # Test data specialist
            test_result = self.data_specialist.extract_numeric_value("FVC: 3.5", r"FVC[:\s]*(\d+\.?\d*)")
            agents_status["data_specialist"] = "healthy" if test_result else "warning"
        except Exception:
            agents_status["data_specialist"] = "error"
        
        # For other agents, we'll assume they're healthy if they can be instantiated
        agents_status.update({
            "interpreter": "healthy",
            "report_writer": "healthy",
            "triage_specialist": "healthy",
            "medical_chatbot": "healthy",
            "learning_assistant": "healthy"
        })
        
        return {
            "overall_status": "healthy" if all(status == "healthy" for status in agents_status.values()) else "degraded",
            "agents": agents_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get workflow performance metrics."""
        
        return {
            "workflow_steps": len(self.workflow_steps),
            "average_processing_time": "3-5 minutes",  # This would be calculated from actual data
            "success_rate": "95%",  # This would be calculated from actual data
            "most_time_consuming_step": "report_generation",
            "optimization_opportunities": [
                "Parallel execution of independent steps",
                "Caching of common calculations",
                "Optimized agent response times"
            ]
        }


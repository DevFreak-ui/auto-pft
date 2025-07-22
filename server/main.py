"""
Main FastAPI application for AutoPFTReport System.

This is the central API server that orchestrates all AI agents to provide
automated PFT interpretation and reporting services.
"""

import os
import uuid
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from fastapi import WebSocket

import redis.asyncio as aioredis
from config import settings
import logging
from fastapi import Request

# Import our models and agents
from models.pft_models import (
    PFTProcessingRequest, PFTProcessingResponse, PFTReport,
    DoctorFeedback, ChatMessage, ChatResponse, TriageLevel
)
# Agent imports
from agent.data_specialist import DataSpecialistAgent
from agent.interpreter import InterpreterAgent
from agent.report_writer import ReportWriterAgent
from agent.triage_specialist import TriageSpecialistAgent
from agent.medical_chatbot import MedicalChatbotAgent
from agent.learning_assistant import LearningAssistantAgent

# Workflow orchestrator for PFT processing
from utils.orchestrator import PFTWorkflowOrchestrator

from utils import openai
# from openai import AsyncOpenAI

# from agents import (
#     set_default_openai_api,
#     set_default_openai_client,
#     set_tracing_disabled,
# )

# Initialize FastAPI app
app = FastAPI(
    title="AutoPFTReport API",
    description="AI-powered Pulmonary Function Test interpretation and reporting system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("autopftreport")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log all HTTP requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"HTTP request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"HTTP response: {response.status_code} {request.url}")
    return response

# Initialize agents
data_specialist = DataSpecialistAgent()
interpreter = InterpreterAgent()
report_writer = ReportWriterAgent()
triage_specialist = TriageSpecialistAgent()
medical_chatbot = MedicalChatbotAgent()
learning_assistant = LearningAssistantAgent()

# Orchestrator to manage the multi-agent pipeline
workflow = PFTWorkflowOrchestrator()

# Redis-based storage for requests, completed reports, and feedback
redis_client = aioredis.from_url(
    settings.REDIS_URL, encoding="utf-8", decode_responses=True
)


class ProcessingStatus(BaseModel):
    """Processing status response model."""
    request_id: str
    status: str
    progress: int
    current_step: str
    estimated_completion: Optional[str] = None
    error_message: Optional[str] = None

# client = AsyncOpenAI(
#     base_url=settings.LITELLM_API_BASE,
#     api_key=settings.LITELLM_KEY
# )
# set_default_openai_client(client=client, use_for_tracing=False)
# set_default_openai_api("chat_completions")
# set_tracing_disabled(disabled=True)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    logger.info("root endpoint called")
    logger.info(settings.REDIS_URL)
    logger.info(redis_client)
    return {
        "message": "AutoPFTReport API",
        "version": "1.0.0",
        "description": "AI-powered PFT interpretation and reporting system",
        "endpoints": {
            "upload": "/pft/upload",
            "status": "/pft/status/{request_id}",
            "report": "/pft/report/{request_id}",
            "interpret": "/pft/interpret",
            "feedback": "/pft/feedback",
            "chat": "/chat",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("health_check endpoint called")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": {
            "data_specialist": "active",
            "interpreter": "active",
            "report_writer": "active",
            "triage_specialist": "active",
            "medical_chatbot": "active",
            "learning_assistant": "active"
        }
    }


@app.websocket("/pft/ws/{request_id}")
async def websocket_progress(websocket: WebSocket, request_id: str):
    """WebSocket endpoint for real-time PFT processing progress updates."""
    logger.info(f"WebSocket connect: request_id={request_id}")
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"pft:progress:{request_id}")
    try:
        async for message in pubsub.listen():
                if message.get("type") == "message":
                    logger.debug(f"WebSocket sending progress: {message.get('data')}")
                    await websocket.send_text(message.get("data"))
    finally:
        logger.info(f"WebSocket disconnect: request_id={request_id}")
        await pubsub.unsubscribe(f"pft:progress:{request_id}")
        await pubsub.close()


@app.post("/pft/upload")
async def upload_pft_file(
    patient_id: str,
    age: int,
    gender: str,
    height: float,
    weight: float,
    background_tasks: BackgroundTasks,
    ethnicity: Optional[str] = None,
    smoking_status: Optional[str] = None,
    file: UploadFile = File(...),
    priority: TriageLevel = TriageLevel.ROUTINE,
    requesting_physician: Optional[str] = None
):
    """
    Upload a PFT file for processing.

    Accepts multipart/form-data with patient demographics and file upload.
    """
    logger.info(f"upload_pft_file called for patient_id={patient_id}, file={file.filename}")
    # Validate file extension
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in settings.SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}, supported: {settings.SUPPORTED_FILE_TYPES}"
        )
    # Read file bytes and enforce size limit
    content_bytes = await file.read()
    if len(content_bytes) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum of {settings.MAX_FILE_SIZE} bytes"
        )
    # Convert bytes to string for downstream processing
    file_content = content_bytes.decode('latin-1')

    # Generate unique request ID
    request_id = str(uuid.uuid4())
    # Build processing request
    processing_request = PFTProcessingRequest(
        request_id=request_id,
        patient_demographics={
            "patient_id": patient_id,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "ethnicity": ethnicity,
            "smoking_status": smoking_status
        },
        raw_file_data=file_content,
        file_type=ext,
        priority=priority.value,
        requesting_physician=requesting_physician
    )
    request_dict = processing_request.dict()
    request_dict["priority"] = processing_request.priority.value
    # Store initial request in Redis
    await redis_client.set(
        f"pft:processing:{request_id}",
        json.dumps({
            "request": request_dict,
            "status": "queued",
            "progress": 0,
            "current_step": "Queued for processing",
            "created_at": datetime.now().isoformat(),
            "estimated_completion": None
        })
    )
    # Launch orchestrator pipeline in background
    background_tasks.add_task(
        workflow.process_pft_request,
        request_id,
        processing_request.raw_file_data,
        processing_request.file_type,
        dict(processing_request.patient_demographics),
        processing_request.historical_data,
        processing_request.priority.value
    )
    return {
        "request_id": request_id,
        "status": "queued",
        "message": "PFT file uploaded successfully and queued for processing",
        "estimated_processing_time": "2-5 minutes"
    }


@app.get("/pft/status/{request_id}")
async def get_processing_status(request_id: str) -> ProcessingStatus:
    """Get processing status for a PFT request."""
    logger.info(f"get_processing_status called for request_id={request_id}")
    data = await redis_client.get(f"pft:processing:{request_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Request not found")
    request_data = json.loads(data)
    print(request_data)
    
    return ProcessingStatus(
        request_id=request_id,
        status=request_data.get("status",""),
        progress=request_data["progress"],
        current_step=request_data["current_step"],
        estimated_completion=request_data.get("estimated_completion"),
        error_message=request_data.get("error_message")
    )


@app.get("/pft/report/{request_id}")
async def get_pft_report(request_id: str):
    """Retrieve completed PFT report."""
    logger.info(f"get_pft_report called for request_id={request_id}")
    # Try completed report
    data = await redis_client.get(f"pft:report:{request_id}")
    if data:
        return json.loads(data)
    # Check processing status
    running = await redis_client.get(f"pft:processing:{request_id}")
    if running:
        status = json.loads(running).get("status")
        if status == "processing":
            raise HTTPException(status_code=202, detail="Report still being processed")
        if status == "failed":
            raise HTTPException(status_code=500, detail="Report processing failed")
    raise HTTPException(status_code=404, detail="Report not found")


@app.post("/pft/interpret")
async def direct_interpretation(
    raw_data: Dict[str, Any],
    patient_demographics: Dict[str, Any],
    predicted_values: Optional[Dict[str, Any]] = None,
    percent_predicted: Optional[Dict[str, Any]] = None,
    historical_data: Optional[List[Dict[str, Any]]] = None
):
    """
    Direct PFT interpretation without file upload.
    
    For cases where PFT data is already structured.
    """
    logger.info("direct_interpretation called")
    try:
        # Use interpreter agent directly
        interpretation = interpreter.interpret_pft_results(
            raw_data=raw_data,
            predicted_values=predicted_values or {},
            percent_predicted=percent_predicted or {},
            patient_demographics=patient_demographics,
            historical_data=historical_data or []
        )
        
        # Get triage assessment
        triage_assessment = triage_specialist.assess_triage_priority(
            interpretation=interpretation,
            patient_demographics=patient_demographics,
            raw_data=raw_data,
            percent_predicted=percent_predicted or {},
            historical_data=historical_data
        )
        
        return {
            "interpretation": interpretation,
            "triage": triage_assessment,
            "processed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interpretation failed: {str(e)}")


@app.post("/pft/feedback")
async def submit_feedback(feedback: DoctorFeedback):
    """Submit doctor feedback for system learning."""
    logger.info(f"submit_feedback called: report_id={feedback.report_id}, physician_id={feedback.physician_id}")
    try:
        # Store feedback in Redis list
        await redis_client.rpush("pft:feedback", json.dumps(feedback.dict()))
        total_fb = await redis_client.llen("pft:feedback")
        # Trigger learning analysis every 10 entries
        if total_fb >= 10:
            batch = await redis_client.lrange("pft:feedback", -10, -1)
            fb_list = [json.loads(item) for item in batch]
            learning_assistant.analyze_feedback_batch(fb_list, "recent")
        
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": str(uuid.uuid4()),
            "status": "received"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")


@app.post("/chat")
async def chat_with_medical_bot(message: ChatMessage) -> ChatResponse:
    """Chat with the medical AI assistant."""
    logger.info(f"chat_with_medical_bot called: message_id={message.message_id}, user_id={message.user_id}")
    try:
        # Get related report context if report_id provided
        report_context = None
        if message.report_id:
            data = await redis_client.get(f"pft:report:{message.report_id}")
            if data:
                report_context = json.loads(data)
        
        # Get response from chatbot
        response_data = medical_chatbot.answer_question(
            question=message.message,
            report_context=report_context,
            user_context={"user_id": message.user_id}
        )
        
        return ChatResponse(
            message_id=message.message_id,
            response=response_data.get("answer", "I'm sorry, I couldn't process your question."),
            confidence=response_data.get("confidence", 0.5),
            sources=response_data.get("sources", []),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/chat/explain/{report_id}")
async def explain_report_rationale(report_id: str, question: Optional[str] = None):
    """Explain the rationale behind a specific report's interpretation."""
    logger.info(f"explain_report_rationale called: report_id={report_id}, question={question}")
    data = await redis_client.get(f"pft:report:{report_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Report not found")
    
    try:
        report = json.loads(data)
        
        if question:
            # Answer specific question about the report
            response_data = await medical_chatbot.answer_question(
                question=question,
                report_context=report
            )
            return response_data
        else:
            # Provide general explanation of interpretation rationale
            explanation = await medical_chatbot.explain_interpretation_rationale(
                interpretation=report.get("interpretation", {}),
                raw_data=report.get("raw_data", {})
            )
            return {"explanation": explanation}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")


@app.get("/analytics/performance")
async def get_performance_analytics(
    time_period: str = "last_30_days",
    include_trends: bool = True
):
    """Get system performance analytics."""
    logger.info(f"get_performance_analytics called: time_period={time_period}, include_trends={include_trends}")
    try:
        # In production, this would query actual performance data
        # Gather performance summary
        reports = await redis_client.keys("pft:report:*")
        analytics_data = {
            "time_period": time_period,
            "total_reports_processed": len(reports),
            "average_processing_time": "3.2 minutes",
            "accuracy_metrics": {
                "interpretation_accuracy": 92.5,
                "triage_accuracy": 89.3,
                "report_quality_score": 4.2
            },
            "user_satisfaction": {
                "average_rating": 4.1,
                "total_feedback_entries": await redis_client.llen("pft:feedback")
            },
            "system_performance": {
                "uptime": "99.8%",
                "average_response_time": "1.2 seconds",
                "error_rate": "0.3%"
            }
        }
        
        if include_trends:
            # Retrieve all feedback entries from Redis
            raw_fb = await redis_client.lrange("pft:feedback", 0, -1)
            fb_list = [json.loads(item) for item in raw_fb] if raw_fb else []
            if fb_list:
                trends = learning_assistant.track_performance_metrics(
                    metrics_data=fb_list,
                    time_window=time_period
                )
                analytics_data["trends"] = trends
        
        return analytics_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")


if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


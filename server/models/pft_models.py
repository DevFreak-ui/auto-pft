"""
Pydantic models for PFT (Pulmonary Function Test) data structures.
These models define the data schemas used throughout the AutoPFTReport system.
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class PatientDemographics(BaseModel):
    """Patient demographic information."""
    patient_id: str = Field(..., description="Unique patient identifier")
    age: int = Field(..., ge=0, le=150, description="Patient age in years")
    gender: str = Field(..., description="Patient gender (M/F/Other)")
    height: float = Field(..., gt=0, description="Patient height in cm")
    weight: float = Field(..., gt=0, description="Patient weight in kg")
    ethnicity: Optional[str] = Field(None, description="Patient ethnicity")
    smoking_status: Optional[str] = Field(None, description="Current/Former/Never smoker")


class PFTRawData(BaseModel):
    """Raw PFT measurement data."""
    # Spirometry measurements
    fvc: Optional[float] = Field(None, description="Forced Vital Capacity (L)")
    fev1: Optional[float] = Field(None, description="Forced Expiratory Volume in 1 second (L)")
    fev1_fvc_ratio: Optional[float] = Field(None, description="FEV1/FVC ratio (%)")
    pef: Optional[float] = Field(None, description="Peak Expiratory Flow (L/s)")
    fef25_75: Optional[float] = Field(None, description="Forced Expiratory Flow 25-75% (L/s)")
    
    # Lung volumes
    tlc: Optional[float] = Field(None, description="Total Lung Capacity (L)")
    frc: Optional[float] = Field(None, description="Functional Residual Capacity (L)")
    rv: Optional[float] = Field(None, description="Residual Volume (L)")
    erv: Optional[float] = Field(None, description="Expiratory Reserve Volume (L)")
    irv: Optional[float] = Field(None, description="Inspiratory Reserve Volume (L)")
    svc: Optional[float] = Field(None, description="Slow Vital Capacity (L)")
    
    # Diffusion capacity
    dlco: Optional[float] = Field(None, description="Diffusing Capacity for CO (mL/min/mmHg)")
    dlco_va: Optional[float] = Field(None, description="DLCO corrected for alveolar volume")
    va: Optional[float] = Field(None, description="Alveolar Volume (L)")
    
    # Respiratory muscle strength
    mip: Optional[float] = Field(None, description="Maximal Inspiratory Pressure (cmH2O)")
    mep: Optional[float] = Field(None, description="Maximal Expiratory Pressure (cmH2O)")
    
    # Post-bronchodilator values (if applicable)
    post_bd_fvc: Optional[float] = Field(None, description="Post-bronchodilator FVC (L)")
    post_bd_fev1: Optional[float] = Field(None, description="Post-bronchodilator FEV1 (L)")
    post_bd_fev1_fvc_ratio: Optional[float] = Field(None, description="Post-BD FEV1/FVC ratio (%)")


class PFTPredictedValues(BaseModel):
    """Predicted normal values based on patient demographics."""
    fvc_predicted: Optional[float] = Field(None, description="Predicted FVC (L)")
    fev1_predicted: Optional[float] = Field(None, description="Predicted FEV1 (L)")
    fev1_fvc_predicted: Optional[float] = Field(None, description="Predicted FEV1/FVC ratio (%)")
    tlc_predicted: Optional[float] = Field(None, description="Predicted TLC (L)")
    dlco_predicted: Optional[float] = Field(None, description="Predicted DLCO (mL/min/mmHg)")
    
    # Lower limits of normal (LLN)
    fvc_lln: Optional[float] = Field(None, description="FVC Lower Limit of Normal")
    fev1_lln: Optional[float] = Field(None, description="FEV1 Lower Limit of Normal")
    fev1_fvc_lln: Optional[float] = Field(None, description="FEV1/FVC LLN")
    tlc_lln: Optional[float] = Field(None, description="TLC Lower Limit of Normal")
    dlco_lln: Optional[float] = Field(None, description="DLCO Lower Limit of Normal")


class PFTPercentPredicted(BaseModel):
    """Percent predicted values for PFT measurements."""
    fvc_percent: Optional[float] = Field(None, description="FVC % predicted")
    fev1_percent: Optional[float] = Field(None, description="FEV1 % predicted")
    tlc_percent: Optional[float] = Field(None, description="TLC % predicted")
    dlco_percent: Optional[float] = Field(None, description="DLCO % predicted")


class HistoricalPFTData(BaseModel):
    """Historical PFT data for trend analysis."""
    test_date: datetime = Field(..., description="Date of historical test")
    fvc: Optional[float] = Field(None, description="Historical FVC (L)")
    fev1: Optional[float] = Field(None, description="Historical FEV1 (L)")
    fev1_fvc_ratio: Optional[float] = Field(None, description="Historical FEV1/FVC ratio (%)")
    dlco: Optional[float] = Field(None, description="Historical DLCO (mL/min/mmHg)")


class PFTQualityMetrics(BaseModel):
    """Quality control metrics for PFT test."""
    acceptable_curves: int = Field(..., ge=0, description="Number of acceptable curves")
    reproducible: bool = Field(..., description="Test meets reproducibility criteria")
    effort_quality: str = Field(..., description="Patient effort quality (Good/Fair/Poor)")
    technician_notes: Optional[str] = Field(None, description="Technician quality notes")


class PFTInterpretationPattern(Enum):
    """PFT interpretation patterns."""
    NORMAL = "normal"
    OBSTRUCTIVE = "obstructive"
    RESTRICTIVE = "restrictive"
    MIXED = "mixed"
    INCONCLUSIVE = "inconclusive"


class PFTSeverity(Enum):
    """PFT abnormality severity levels."""
    NORMAL = "normal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    VERY_SEVERE = "very_severe"


class PFTInterpretation(BaseModel):
    """PFT interpretation results."""
    pattern: PFTInterpretationPattern = Field(..., description="Primary interpretation pattern")
    severity: PFTSeverity = Field(..., description="Severity of abnormality")
    reversibility: Optional[bool] = Field(None, description="Bronchodilator reversibility")
    reversibility_percent: Optional[float] = Field(None, description="% improvement with bronchodilator")
    
    # Specific findings
    airway_obstruction: bool = Field(False, description="Airway obstruction present")
    restriction: bool = Field(False, description="Restriction present")
    diffusion_impairment: bool = Field(False, description="Diffusion impairment present")
    respiratory_muscle_weakness: bool = Field(False, description="Respiratory muscle weakness")
    
    # Clinical correlations
    likely_diagnoses: List[str] = Field(default_factory=list, description="Likely clinical diagnoses")
    recommendations: List[str] = Field(default_factory=list, description="Clinical recommendations")


class TriageLevel(Enum):
    """Triage priority levels."""
    ROUTINE = "routine"
    URGENT = "urgent"
    CRITICAL = "critical"


class TriageAssessment(BaseModel):
    """Triage assessment for PFT results."""
    level: TriageLevel = Field(..., description="Triage priority level")
    reasons: List[str] = Field(..., description="Reasons for triage level")
    recommended_followup: str = Field(..., description="Recommended follow-up timeframe")
    specialist_referral: bool = Field(False, description="Specialist referral recommended")


class PFTReport(BaseModel):
    """Complete PFT report."""
    report_id: str = Field(..., description="Unique report identifier")
    patient_demographics: PatientDemographics
    test_date: datetime = Field(..., description="Date of PFT test")
    raw_data: PFTRawData
    predicted_values: PFTPredictedValues
    percent_predicted: PFTPercentPredicted
    quality_metrics: PFTQualityMetrics
    interpretation: PFTInterpretation
    triage: TriageAssessment
    
    # Historical data for comparison
    historical_data: List[HistoricalPFTData] = Field(default_factory=list)
    
    # Report metadata
    generated_by: str = Field("AutoPFTReport AI", description="Report generator")
    generated_at: datetime = Field(default_factory=datetime.now)
    reviewed_by: Optional[str] = Field(None, description="Reviewing physician")
    review_date: Optional[datetime] = Field(None, description="Review date")
    
    # Free text sections
    clinical_summary: str = Field(..., description="Clinical summary")
    detailed_interpretation: str = Field(..., description="Detailed interpretation")
    recommendations_text: str = Field(..., description="Detailed recommendations")


class PFTProcessingRequest(BaseModel):
    """Request for PFT processing."""
    request_id: str = Field(..., description="Unique request identifier")
    patient_demographics: PatientDemographics
    raw_file_data: str = Field(..., description="Raw PFT file content or data")
    file_type: str = Field(..., description="Type of PFT file (PDF, TXT, XML, etc.)")
    historical_data: List[HistoricalPFTData] = Field(default_factory=list)
    priority: TriageLevel = Field(TriageLevel.ROUTINE, description="Processing priority")
    requesting_physician: Optional[str] = Field(None, description="Requesting physician")


class PFTProcessingResponse(BaseModel):
    """Response from PFT processing."""
    request_id: str = Field(..., description="Original request identifier")
    status: str = Field(..., description="Processing status")
    report: Optional[PFTReport] = Field(None, description="Generated report if completed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    processing_time: float = Field(..., description="Processing time in seconds")


class DoctorFeedback(BaseModel):
    """Feedback from doctors for system learning."""
    report_id: str = Field(..., description="Report identifier")
    physician_id: str = Field(..., description="Physician identifier")
    feedback_date: datetime = Field(default_factory=datetime.now)
    
    # Accuracy ratings (1-5 scale)
    interpretation_accuracy: int = Field(..., ge=1, le=5, description="Interpretation accuracy rating")
    report_quality: int = Field(..., ge=1, le=5, description="Report quality rating")
    triage_appropriateness: int = Field(..., ge=1, le=5, description="Triage appropriateness rating")
    
    # Specific corrections
    corrected_pattern: Optional[PFTInterpretationPattern] = Field(None)
    corrected_severity: Optional[PFTSeverity] = Field(None)
    corrected_triage: Optional[TriageLevel] = Field(None)
    
    # Free text feedback
    comments: Optional[str] = Field(None, description="Additional comments")
    suggestions: Optional[str] = Field(None, description="Suggestions for improvement")


class ChatMessage(BaseModel):
    """Chat message for medical chatbot."""
    message_id: str = Field(..., description="Unique message identifier")
    session_id: str = Field(..., description="Chat session identifier")
    user_id: str = Field(..., description="User identifier")
    message: str = Field(..., description="User message")
    timestamp: datetime = Field(default_factory=datetime.now)
    report_id: Optional[str] = Field(None, description="Related report ID if applicable")


class ChatResponse(BaseModel):
    """Response from medical chatbot."""
    message_id: str = Field(..., description="Original message identifier")
    response: str = Field(..., description="Chatbot response")
    confidence: float = Field(..., ge=0, le=1, description="Response confidence score")
    sources: List[str] = Field(default_factory=list, description="Information sources")
    timestamp: datetime = Field(default_factory=datetime.now)


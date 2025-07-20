"""
Configuration settings for AutoPFTReport System.
"""

import os
from typing import Dict, Any
from typing import Any
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_TITLE: str = "AutoPFTReport API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered Pulmonary Function Test interpretation and reporting system"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    RELOAD: bool = False
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL: str = "openai/gpt-4o"
    OPENAI_TEMPERATURE: float = 0.1
    OPENAI_MAX_TOKENS: int = 2000

    # Litellm configuration
    LITELLM_MODEL: str = os.getenv("LITELLM_MODEL","openai/gpt-4o")
    LITELLM_KEY: str = os.getenv("LITELLM_KEY","sk-S")
    LITELLM_API_BASE: str = os.getenv("LITELLM_API_BASE","http://91.108.112.45:4000")
    
    # Processing Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FILE_TYPES: list = ["txt", "pdf", "csv", "xlsx", "xml", "json"]
    MAX_PROCESSING_TIME: int = 600  # 10 minutes
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Database Configuration (for future use)
    DATABASE_URL: str = "sqlite:///./autopftreport.db"
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["*"]  # In production, specify actual origins
    ALLOWED_METHODS: list = ["*"]
    ALLOWED_HEADERS: list = ["*"]
    
    # Agent Configuration
    AGENT_TIMEOUT: int = 120  # seconds
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5  # seconds
    
    # Quality Thresholds
    MIN_INTERPRETATION_CONFIDENCE: float = 0.7
    MIN_REPORT_QUALITY_SCORE: float = 7.0
    MIN_TRIAGE_CONFIDENCE: float = 0.8
    
    # Performance Monitoring
    ENABLE_METRICS: bool = True
    METRICS_RETENTION_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env")
    


# PFT Interpretation Guidelines and Reference Values
PFT_REFERENCE_VALUES = {
    "normal_ranges": {
        "fev1_fvc_ratio": {
            "adult": {"min": 70, "max": 100},
            "pediatric": {"min": 85, "max": 100}
        },
        "fvc_percent_predicted": {"min": 80, "max": 120},
        "fev1_percent_predicted": {"min": 80, "max": 120},
        "dlco_percent_predicted": {"min": 75, "max": 125},
        "tlc_percent_predicted": {"min": 80, "max": 120}
    },
    "severity_thresholds": {
        "fev1_percent_predicted": {
            "normal": 80,
            "mild": 70,
            "moderate": 50,
            "severe": 30,
            "very_severe": 0
        }
    },
    "reversibility_criteria": {
        "adult": {
            "fev1_improvement_percent": 12,
            "fev1_improvement_ml": 200,
            "fvc_improvement_percent": 12,
            "fvc_improvement_ml": 200
        },
        "pediatric": {
            "fev1_improvement_percent": 12,
            "fvc_improvement_percent": 12
        }
    }
}

# Medical Guidelines and References
MEDICAL_GUIDELINES = {
    "ats_ers_2005": {
        "name": "ATS/ERS Task Force: Standardisation of spirometry",
        "url": "https://erj.ersjournals.com/content/26/2/319",
        "key_points": [
            "Standardized spirometry procedures",
            "Quality control criteria",
            "Reference equations"
        ]
    },
    "gold_2023": {
        "name": "Global Initiative for Chronic Obstructive Lung Disease",
        "url": "https://goldcopd.org/",
        "key_points": [
            "COPD diagnosis criteria",
            "Severity classification",
            "Treatment recommendations"
        ]
    },
    "aafp_2014": {
        "name": "AAFP: Office Spirometry",
        "url": "https://www.aafp.org/pubs/afp/issues/2014/0301/p359.html",
        "key_points": [
            "Stepwise interpretation approach",
            "Clinical correlation",
            "Common patterns"
        ]
    }
}

# Error Messages and User Feedback
ERROR_MESSAGES = {
    "file_too_large": "File size exceeds maximum limit of {max_size}MB",
    "unsupported_file_type": "File type '{file_type}' is not supported",
    "processing_timeout": "Processing timed out after {timeout} seconds",
    "invalid_patient_data": "Invalid patient demographic data provided",
    "agent_error": "Error in {agent_name}: {error_message}",
    "insufficient_data": "Insufficient PFT data for reliable interpretation",
    "quality_check_failed": "Report quality check failed: {reason}"
}

# Success Messages
SUCCESS_MESSAGES = {
    "upload_success": "PFT file uploaded successfully",
    "processing_complete": "PFT analysis completed successfully",
    "report_generated": "Medical report generated successfully",
    "feedback_received": "Feedback submitted successfully"
}

# Agent Prompts and Instructions
AGENT_INSTRUCTIONS = {
    "data_specialist": {
        "system_prompt": "You are a specialized AI agent for extracting and standardizing PFT data...",
        "quality_checks": [
            "Verify numeric values are within physiological ranges",
            "Check for missing critical parameters",
            "Validate data consistency"
        ]
    },
    "interpreter": {
        "system_prompt": "You are a specialized AI agent for interpreting PFT results...",
        "guidelines": [
            "Follow ATS/ERS interpretation guidelines",
            "Consider patient demographics",
            "Provide evidence-based interpretations"
        ]
    },
    "report_writer": {
        "system_prompt": "You are a specialized AI agent for writing professional medical reports...",
        "formatting_rules": [
            "Use clear, professional medical language",
            "Include all relevant clinical information",
            "Provide actionable recommendations"
        ]
    },
    "triage_specialist": {
        "system_prompt": "You are a specialized AI agent for triaging PFT cases...",
        "priority_criteria": [
            "Severity of impairment",
            "Clinical urgency",
            "Patient safety considerations"
        ]
    }
}

# Create settings instance
settings = Settings()

# Validation functions
def validate_openai_config() -> bool:
    """Validate OpenAI configuration."""
    return bool(settings.OPENAI_API_KEY)

def get_file_size_limit() -> int:
    """Get file size limit in bytes."""
    return settings.MAX_FILE_SIZE

def is_supported_file_type(file_type: str) -> bool:
    """Check if file type is supported."""
    return file_type.lower() in [ft.lower() for ft in settings.SUPPORTED_FILE_TYPES]

def get_processing_timeout() -> int:
    """Get processing timeout in seconds."""
    return settings.MAX_PROCESSING_TIME


# AutoPFT Backend Architecture 🚀

## 🏗️ Overview

The AutoPFT backend is a **FastAPI-based microservices architecture** that orchestrates multiple AI agents to provide automated Pulmonary Function Test (PFT) interpretation and reporting. The system is designed for high performance, scalability, and reliability in healthcare environments.

## 🛠️ Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs with Python 3.8+
- **Uvicorn**: ASGI server for high-performance async operations
- **Pydantic**: Data validation and settings management
- **Redis**: In-memory data store for caching and real-time updates

### AI & Machine Learning
- **OpenAI GPT-4**: Primary AI model for medical interpretation
- **LiteLLM**: Unified interface for multiple AI model providers
- **Scikit-learn**: Statistical analysis and data processing
- **Pandas & NumPy**: Data manipulation and numerical computing

### Data Processing
- **Python-multipart**: File upload handling
- **Aiofiles**: Asynchronous file operations
- **BeautifulSoup4 & LXML**: Document parsing and extraction
- **PyPDF2 & PDFPlumber**: PDF processing and text extraction

### Visualization & Reporting
- **Matplotlib & Seaborn**: Data visualization and charts
- **Plotly**: Interactive charts and dashboards
- **ReportLab & FPDF2**: PDF report generation
- **XlsxWriter**: Excel report creation

## 🏛️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Redis Cache   │    │   File Storage  │
│   (main.py)     │◄──►│   (Progress &   │    │   (PFT Files)   │
│                 │    │    Results)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI Agent Orchestrator                        │
│                    (orchestrator.py)                           │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         AI Agents                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │Data Specialist│ │Interpreter  │ │Report Writer│ │Triage Spec. │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│  ┌─────────────┐ ┌─────────────┐                               │
│  │Medical Chat │ │Learning Asst│                               │
│  └─────────────┘ └─────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## 🔌 API Endpoints

### Core PFT Processing

#### 1. File Upload & Processing
```http
POST /pft/upload
Content-Type: multipart/form-data

Parameters:
- patient_id: string (required)
- age: integer (required)
- gender: string (required)
- height: float (required)
- weight: float (required)
- ethnicity: string (optional)
- smoking_status: string (optional)
- file: UploadFile (required)
- priority: TriageLevel (optional)
- requesting_physician: string (optional)
```

**Response:**
```json
{
  "request_id": "uuid-string",
  "status": "processing",
  "estimated_completion": "2024-01-15T10:30:00Z",
  "message": "PFT file uploaded successfully"
}
```

#### 2. Processing Status
```http
GET /pft/status/{request_id}
```

**Response:**
```json
{
  "request_id": "uuid-string",
  "progress": 75,
  "current_step": "Generating final report",
  "estimated_completion": "2024-01-15T10:35:00Z",
  "error_message": null
}
```

#### 3. Retrieve Report
```http
GET /pft/report/{request_id}
```

**Response:**
```json
{
  "request_id": "uuid-string",
  "report": {
    "summary": "Moderate obstructive lung disease",
    "interpretation": "Detailed interpretation...",
    "recommendations": "Treatment recommendations...",
    "severity": "moderate",
    "confidence_score": 0.89
  },
  "raw_data": {...},
  "predicted_values": {...},
  "quality_metrics": {...}
  }
}
```

### Direct Interpretation
```http
POST /pft/interpret
Content-Type: application/json

{
  "raw_data": {...},
  "patient_demographics": {...},
  "predicted_values": {...},
  "percent_predicted": {...},
  "historical_data": [...]
}
```

### Medical Chat Interface
```http
POST /chat
Content-Type: application/json

{
  "message": "Explain the significance of FEV1/FVC ratio",
  "context": "pft_interpretation"
}
```

### WebSocket Progress Updates
```http
WS /pft/ws/{request_id}
```

**Real-time updates:**
```json
{
  "progress": 60,
  "current_step": "AI interpretation",
  "estimated_completion": "2024-01-15T10:32:00Z"
}
```

## 🤖 AI Agent Architecture

### 1. Data Specialist Agent (`data_specialist.py`)

**Purpose**: Extract and standardize PFT data from various file formats

**Key Responsibilities:**
- Parse multiple file formats (TXT, PDF, CSV, XLSX, XML, JSON)
- Extract PFT measurements (FVC, FEV1, FEV1/FVC ratio, PEF, etc.)
- Standardize data format and units
- Validate data quality and completeness
- Calculate predicted values when possible

**Core Methods:**
```python
class DataSpecialistAgent:
    async def process_file(self, file_content: str, file_type: str) -> Dict[str, Any]
    async def validate_pft_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]
    def extract_numeric_value(self, text: str, pattern: str) -> Optional[float]
```

**Data Quality Checks:**
- Physiological range validation
- Missing parameter identification
- Unit consistency verification
- Data entry error detection

### 2. Interpreter Agent (`interpreter.py`)

**Purpose**: Analyze PFT data and provide medical interpretation

**Key Responsibilities:**
- Analyze lung function parameters
- Identify patterns and abnormalities
- Provide differential diagnoses
- Assess disease severity
- Generate clinical insights

**Interpretation Criteria:**
- FEV1/FVC ratio analysis
- Percent predicted value assessment
- Bronchodilator response evaluation
- Pattern recognition (obstructive, restrictive, mixed)

### 3. Report Writer Agent (`report_writer.py`)

**Purpose**: Generate comprehensive, clinically relevant reports

**Key Responsibilities:**
- Structure clinical findings
- Generate treatment recommendations
- Format reports for different audiences
- Include relevant clinical guidelines
- Ensure medical accuracy and clarity

**Report Components:**
- Executive summary
- Detailed interpretation
- Clinical recommendations
- Follow-up suggestions
- References and guidelines

### 4. Triage Specialist Agent (`triage_specialist.py`)

**Purpose**: Assess urgency and prioritize cases

**Key Responsibilities:**
- Evaluate clinical urgency
- Assign priority levels
- Identify critical findings
- Recommend immediate actions
- Risk stratification

**Triage Levels:**
- **CRITICAL**: Immediate attention required
- **URGENT**: Attention within hours
- **ROUTINE**: Standard processing time
- **ELECTIVE**: Non-urgent cases

### 5. Medical Chatbot Agent (`medical_chatbot.py`)

**Purpose**: Provide interactive medical guidance and explanations

**Key Responsibilities:**
- Answer medical queries
- Explain PFT results
- Provide educational content
- Support clinical decision-making
- Maintain conversation context

**Chat Features:**
- Context-aware responses
- Medical terminology explanations
- Interactive Q&A sessions
- Educational resources

### 6. Learning Assistant Agent (`learning_assistant.py`)

**Purpose**: Continuously improve system performance and accuracy

**Key Responsibilities:**
- Learn from doctor feedback
- Update interpretation models
- Identify improvement areas
- Track performance metrics
- Adapt to new guidelines

**Learning Mechanisms:**
- Feedback integration
- Model fine-tuning
- Performance analytics
- Continuous improvement

## 🔄 Workflow Orchestration

### Processing Pipeline (`orchestrator.py`)

The `PFTWorkflowOrchestrator` manages the sequential execution of AI agents:

```python
class PFTWorkflowOrchestrator:
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
```

**Processing Stages:**
1. **QUEUED**: Request received and queued
2. **DATA_EXTRACTION**: Data specialist processes file
3. **INTERPRETATION**: AI interpretation of results
4. **TRIAGE_ASSESSMENT**: Urgency evaluation
5. **REPORT_GENERATION**: Final report creation
6. **QUALITY_VALIDATION**: Quality assurance checks
7. **COMPLETED**: Processing finished

**Progress Tracking:**
- Real-time WebSocket updates
- Redis-based status storage
- Estimated completion times
- Error handling and recovery

## 📊 Data Models

### Core PFT Models (`models/pft_models.py`)

#### Patient Demographics
```python
class PatientDemographics(BaseModel):
    patient_id: str
    age: int
    gender: str
    height: float  # in cm
    weight: float  # in kg
    ethnicity: Optional[str] = None
    smoking_status: Optional[str] = None
    requesting_physician: Optional[str] = None
```

#### PFT Raw Data
```python
class PFTRawData(BaseModel):
    fvc: Optional[float] = None  # Forced Vital Capacity (L)
    fev1: Optional[float] = None  # FEV1 (L)
    fev1_fvc_ratio: Optional[float] = None  # FEV1/FVC (%)
    pef: Optional[float] = None  # Peak Expiratory Flow (L/s)
    fef25_75: Optional[float] = None  # FEF25-75% (L/s)
    tlc: Optional[float] = None  # Total Lung Capacity (L)
    rv: Optional[float] = None  # Residual Volume (L)
    dlco: Optional[float] = None  # Diffusion Capacity (mL/min/mmHg)
```

#### PFT Report
```python
class PFTReport(BaseModel):
    summary: str
    interpretation: str
    recommendations: List[str]
    severity: str
    confidence_score: float
    quality_metrics: PFTQualityMetrics
    generated_at: datetime
    version: str
```

#### Doctor Feedback
```python
class DoctorFeedback(BaseModel):
    report_id: str
    doctor_id: str
    accuracy_rating: int  # 1-10
    clinical_usefulness: int  # 1-10
    suggestions: Optional[str] = None
    feedback_date: datetime
```

## ⚙️ Configuration Management

### Environment Settings (`config.py`)

**OpenAI Configuration:**
```python
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = "openai/gpt-4o"
OPENAI_TEMPERATURE: float = 0.1
OPENAI_MAX_TOKENS: int = 2000
```

**LiteLLM Configuration:**
```python
LITELLM_MODEL: str = os.getenv("LITELLM_MODEL", "openai/gpt-4o")
LITELLM_KEY: str = os.getenv("LITELLM_KEY", "sk-S")
LITELLM_API_BASE: str = os.getenv("LITELLM_API_BASE", "http://91.108.112.45:4000")
```

**Processing Configuration:**
```python
MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
SUPPORTED_FILE_TYPES: list = ["txt", "pdf", "csv", "xlsx", "xml", "json"]
MAX_PROCESSING_TIME: int = 600  # 10 minutes
MAX_CONCURRENT_REQUESTS: int = 10
```

**Quality Thresholds:**
```python
MIN_INTERPRETATION_CONFIDENCE: float = 0.7
MIN_REPORT_QUALITY_SCORE: float = 7.0
MIN_TRIAGE_CONFIDENCE: float = 0.8
```

## 🔒 Security & Compliance

### Data Protection
- **File Upload Validation**: File type and size restrictions
- **Input Sanitization**: Pydantic model validation
- **CORS Configuration**: Configurable origin restrictions
- **API Rate Limiting**: Request throttling capabilities

### Healthcare Compliance
- **HIPAA Considerations**: Patient data handling
- **Audit Logging**: Complete request/response logging
- **Data Encryption**: Secure data transmission
- **Access Control**: Role-based permissions (future)

## 📈 Performance & Scalability

### Async Architecture
- **FastAPI Async**: Non-blocking request handling
- **Background Tasks**: Long-running PFT processing
- **Redis Caching**: Fast data retrieval and storage
- **Connection Pooling**: Efficient database connections

### Monitoring & Metrics
```python
# Performance monitoring
ENABLE_METRICS: bool = True
METRICS_RETENTION_DAYS: int = 30

# Agent health monitoring
async def get_agent_health_status(self) -> Dict[str, Any]:
    return {
        "data_specialist": await self.data_specialist.health_check(),
        "interpreter": await self.interpreter.health_check(),
        "report_writer": await self.report_writer.health_check(),
        "triage_specialist": await self.triage_specialist.health_check(),
        "medical_chatbot": await self.medical_chatbot.health_check(),
        "learning_assistant": await self.learning_assistant.health_check()
    }
```

## 🧪 Testing & Quality Assurance

### System Testing (`test_system.py`)
- **Integration Tests**: End-to-end workflow testing
- **Agent Testing**: Individual agent functionality
- **Performance Testing**: Load and stress testing
- **Error Handling**: Failure scenario testing

### Data Validation
- **Pydantic Models**: Automatic data validation
- **Business Logic**: Custom validation rules
- **Quality Metrics**: Data completeness assessment
- **Error Reporting**: Detailed error messages

## 🚀 Deployment & Operations

### Docker Configuration
```dockerfile
# server/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# Required environment variables
OPENAI_API_KEY=your_openai_api_key
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_secret_key

# Optional configurations
LITELLM_MODEL=openai/gpt-4o
LITELLM_API_BASE=http://your_litellm_server:4000
LOG_LEVEL=INFO
DEBUG=false
```

### Health Checks
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.0.0",
  "agents": {
    "data_specialist": "healthy",
    "interpreter": "healthy",
    "report_writer": "healthy",
    "triage_specialist": "healthy",
    "medical_chatbot": "healthy",
    "learning_assistant": "healthy"
  },
  "redis": "connected",
  "openai": "configured"
}
```

## 🔮 Future Enhancements

### Planned Features
- **Database Integration**: PostgreSQL for persistent storage
- **User Authentication**: JWT-based authentication system
- **Role-Based Access**: Doctor, technician, and admin roles
- **Advanced Analytics**: Machine learning insights
- **Mobile API**: Optimized mobile endpoints
- **Webhook Support**: External system integrations

### Scalability Improvements
- **Microservices**: Service decomposition
- **Message Queues**: RabbitMQ/Kafka integration
- **Load Balancing**: Horizontal scaling support
- **Caching Layers**: Multi-level caching strategy
- **CDN Integration**: Static asset optimization

---

**The AutoPFT backend demonstrates enterprise-grade architecture with AI-first design, ensuring reliable, scalable, and secure PFT processing for healthcare professionals. The multi-agent system provides comprehensive medical interpretation while maintaining high performance and compliance standards.**

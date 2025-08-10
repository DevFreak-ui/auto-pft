# AutoPFT Technical Implementation Guide 🛠️

## 🏗️ System Architecture Overview

AutoPFT is built using a **microservices architecture** with clear separation of concerns between frontend, backend, and AI services. The system is containerized using Docker and orchestrated with Docker Compose for consistent deployment across environments.

## 📁 Code Structure Deep Dive

### Root Directory Structure
```
auto-pft/
├── client/                 # React frontend application
├── server/                 # FastAPI backend application
├── Docs/                   # Project documentation
├── docker-compose.yml      # Production Docker configuration
├── docker-compose.dev.yml  # Development Docker configuration
├── Makefile                # Development automation
└── README.md               # Main project documentation
```

### Frontend Architecture (`client/`)

#### Core Components
- **`src/components/`**: Reusable UI components
  - `custom/`: Application-specific components
  - `ui/`: Base UI components (Shadcn/ui)
- **`src/pages/`**: Page-level components
- **`src/hooks/`**: Custom React hooks for business logic
- **`src/services/`**: API service functions
- **`src/utils/`**: Utility functions and helpers

#### Key Technologies
- **React 19**: Latest React with concurrent features
- **TypeScript**: Full type safety and IntelliSense
- **Vite**: Fast build tool with HMR
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/ui**: High-quality component library

#### State Management
- **React Hooks**: `useState`, `useEffect`, `useCallback`
- **Custom Hooks**: Business logic encapsulation
- **Context API**: Global state management where needed
- **Local Storage**: Persistent data storage

### Backend Architecture (`server/`)

#### Core Structure
- **`main.py`**: FastAPI application entry point
- **`agent/`**: AI agent implementations
- **`models/`**: Pydantic data models
- **`utils/`**: Utility functions and helpers
- **`config.py`**: Configuration management

#### AI Agent System
1. **`DataSpecialistAgent`**: Data validation and preprocessing
2. **`InterpreterAgent`**: Clinical interpretation and analysis
3. **`ReportWriterAgent`**: Medical report generation
4. **`TriageSpecialistAgent`**: Severity assessment
5. **`MedicalChatbotAgent`**: Interactive chat support
6. **`LearningAssistantAgent`**: Continuous improvement

#### API Design
- **RESTful Endpoints**: Standard HTTP methods
- **OpenAPI Documentation**: Auto-generated API docs
- **Pydantic Validation**: Request/response validation
- **Async Support**: Full async/await implementation
- **WebSocket Support**: Real-time progress updates

## 🔧 Key Implementation Details

### 1. Multi-Agent AI Orchestration

#### Agent Communication Pattern
```python
# Example from server/main.py
@app.post("/pft/upload")
async def upload_pft_file(
    patient_id: str,
    age: int,
    gender: str,
    height: float,
    weight: float,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # 1. Data Specialist Agent processes the file
    # 2. Interpreter Agent analyzes the data
    # 3. Report Writer Agent generates the report
    # 4. Triage Specialist Agent assesses severity
    
    # Background processing for long-running tasks
    background_tasks.add_task(process_pft_file, request_id, file_data)
    return {"request_id": request_id, "status": "processing"}
```

#### Workflow Orchestration
```python
# From server/utils/orchestrator.py
class PFTWorkflowOrchestrator:
    def __init__(self):
        self.data_specialist = DataSpecialistAgent()
        self.interpreter = InterpreterAgent()
        self.report_writer = ReportWriterAgent()
        self.triage_specialist = TriageSpecialistAgent()
    
    async def process_pft_data(self, data, demographics):
        # Orchestrate the multi-agent workflow
        validated_data = await self.data_specialist.process(data)
        interpretation = await self.interpreter.analyze(validated_data, demographics)
        report = await self.report_writer.generate(interpretation)
        triage = await self.triage_specialist.assess(report)
        return {"report": report, "triage": triage}
```

### 2. Real-time Processing with WebSockets

#### WebSocket Implementation
```python
# From server/main.py
@app.websocket("/pft/ws/{request_id}")
async def websocket_progress(websocket: WebSocket, request_id: str):
    await websocket.accept()
    try:
        while True:
            # Get current processing status
            status = await get_processing_status_internal(request_id)
            
            # Send progress update to client
            await websocket.send_json({
                "progress": status.progress,
                "current_step": status.current_step,
                "estimated_completion": status.estimated_completion
            })
            
            # Check if processing is complete
            if status.progress >= 100:
                break
                
            await asyncio.sleep(1)  # Update every second
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for request {request_id}")
```

#### Frontend WebSocket Integration
```typescript
// From client/src/hooks/usePFTProcessing.ts
const usePFTProcessing = (requestId: string) => {
    const [progress, setProgress] = useState(0);
    const [currentStep, setCurrentStep] = useState('');
    
    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:8000/pft/ws/${requestId}`);
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setProgress(data.progress);
            setCurrentStep(data.current_step);
        };
        
        return () => ws.close();
    }, [requestId]);
    
    return { progress, currentStep };
};
```

### 3. Interactive Medical Chatbot

#### Chat System Architecture
```typescript
// From client/src/hooks/useGeneralChat.ts
export const useGeneralChat = () => {
    const [messages, setMessages] = useState<GeneralChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const sendMessage = useCallback(async (text: string) => {
        setIsLoading(true);
        setError(null);
        
        try {
            const response = await sendGeneralChat(text);
            setMessages(prev => [...prev, response]);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    }, []);
    
    return { messages, sendMessage, isLoading, error };
};
```

#### Backend Chat Processing
```python
# From server/main.py
@app.post("/chat")
async def chat_with_medical_bot(message: ChatMessage) -> ChatResponse:
    try:
        # Process the chat message through the medical chatbot agent
        response = await medical_chatbot.answer_question(
            message.message,
            context={
                "report_id": message.report_id,
                "user_id": message.user_id,
                "session_id": message.session_id
            }
        )
        
        return ChatResponse(
            message_id=message.message_id,
            response=response,
            confidence=0.9,
            sources=["Medical guidelines", "Clinical research"],
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Chat processing failed")
```

### 4. Data Validation and Error Handling

#### Pydantic Models
```python
# From server/models/pft_models.py
class PFTProcessingRequest(BaseModel):
    patient_id: str
    age: int = Field(ge=0, le=120)
    gender: str = Field(regex="^(male|female|other)$")
    height: float = Field(gt=0, le=300)  # cm
    weight: float = Field(gt=0, le=500)  # kg
    ethnicity: Optional[str] = None
    smoking_status: Optional[str] = None
    priority: TriageLevel = TriageLevel.ROUTINE
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "P12345",
                "age": 45,
                "gender": "male",
                "height": 175.0,
                "weight": 70.0,
                "ethnicity": "African",
                "smoking_status": "former",
                "priority": "routine"
            }
        }
```

#### Frontend Form Validation
```typescript
// From client/src/components/PFTUploadForm.tsx
const PFTUploadForm = () => {
    const [formData, setFormData] = useState({
        patientId: '',
        age: '',
        gender: '',
        height: '',
        weight: ''
    });
    
    const [errors, setErrors] = useState<Record<string, string>>({});
    
    const validateForm = () => {
        const newErrors: Record<string, string> = {};
        
        if (!formData.patientId.trim()) {
            newErrors.patientId = 'Patient ID is required';
        }
        
        const age = parseInt(formData.age);
        if (isNaN(age) || age < 0 || age > 120) {
            newErrors.age = 'Age must be between 0 and 120';
        }
        
        # ... more validation
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!validateForm()) return;
        
        # Submit form data
    };
};
```

## 🚀 Performance Optimizations

### 1. Backend Optimizations
- **Async Processing**: Non-blocking I/O operations
- **Background Tasks**: Long-running operations in background
- **Redis Caching**: Session and data caching
- **Connection Pooling**: Database connection optimization
- **Response Compression**: Gzip compression for large responses

### 2. Frontend Optimizations
- **Code Splitting**: Lazy loading of components
- **Memoization**: React.memo and useMemo for expensive operations
- **Virtual Scrolling**: Efficient rendering of large lists
- **Image Optimization**: WebP format and lazy loading
- **Bundle Optimization**: Tree shaking and minification

### 3. Infrastructure Optimizations
- **Docker Multi-stage Builds**: Optimized container images
- **Nginx Caching**: Static asset caching
- **Load Balancing**: Horizontal scaling capabilities
- **Health Checks**: Automatic service monitoring
- **Resource Limits**: Container resource constraints

## 🔒 Security Implementation

### 1. Data Protection
```python
# From server/config.py
class Settings(BaseSettings):
    # Encryption keys
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
```

### 2. Authentication & Authorization
```python
# JWT token validation
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return username
```

### 3. Input Validation
```python
# SQL injection prevention
async def get_patient_data(patient_id: str):
    # Use parameterized queries
    query = "SELECT * FROM patients WHERE id = :patient_id"
    result = await database.fetch_one(query=query, values={"patient_id": patient_id})
    return result
```

## 🧪 Testing Strategy

### 1. Backend Testing
```python
# From server/test_system.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_pft_upload():
    # Test file upload functionality
    with open("test_data.csv", "rb") as f:
        response = client.post(
            "/pft/upload",
            files={"file": f},
            data={
                "patient_id": "TEST123",
                "age": "45",
                "gender": "male",
                "height": "175",
                "weight": "70"
            }
        )
    assert response.status_code == 200
    assert "request_id" in response.json()
```

### 2. Frontend Testing
```typescript
// From client/src/components/__tests__/PFTUploadForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import PFTUploadForm from '../PFTUploadForm';

describe('PFTUploadForm', () => {
    test('renders form fields', () => {
        render(<PFTUploadForm />);
        
        expect(screen.getByLabelText(/patient id/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/age/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/gender/i)).toBeInTheDocument();
    });
    
    test('validates required fields', () => {
        render(<PFTUploadForm />);
        
        fireEvent.click(screen.getByText(/submit/i));
        
        expect(screen.getByText(/patient id is required/i)).toBeInTheDocument();
    });
});
```

## 📊 Monitoring and Logging

### 1. Application Logging
```python
# From server/main.py
import logging

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("autopftreport")

# Log all HTTP requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"HTTP request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"HTTP response: {response.status_code} {request.url}")
    return response
```

### 2. Health Monitoring
```python
@app.get("/health")
async def health_check():
    try:
        # Check Redis connection
        await redis_client.ping()
        
        # Check database connection
        # await database.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "version": "1.0.0",
            "services": {
                "redis": "healthy",
                "database": "healthy"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")
```

## 🚀 Deployment Considerations

### 1. Environment Configuration
```bash
# .env file structure
# Backend Configuration
PYTHONPATH=/app
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_APP_ENV=development

# Redis Configuration
REDIS_URL=redis://redis:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Docker Optimization
```dockerfile
# Multi-stage build for production
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Scaling Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./server
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    environment:
      - PYTHONPATH=/app
      - REDIS_URL=redis://redis:6379
```

---

**This automatically generated technical implementation guide provides a comprehensive overview of AutoPFT's architecture, key components, and implementation details. The system demonstrates modern software engineering practices with a focus on scalability, security, and maintainability.**

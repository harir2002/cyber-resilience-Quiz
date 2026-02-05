"""
FastAPI Backend for Cyber Resilience Assessment Platform
Main application entry point
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Union
from datetime import datetime
from contextlib import asynccontextmanager
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Disable ChromaDB Telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_SERVER_NO_INTERACTIVE_AUTH"] = "True"

from database.chromadb_manager import ChromaDBManager
from questionnaire.questionnaire_schema import get_questionnaire_schema, get_question_count
from utils.scoring import ResilienceScorer

# Initialize database and scorer
db = ChromaDBManager()
scorer = ResilienceScorer()

# Lifespan event handler (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[*] Starting Cyber Resilience Assessment API...")
    print("[*] Initializing ChromaDB...")
    
    # FORCE RELOAD: Always reload questions from schema
    print("[*] Loading questionnaire from schema...")
    schema = get_questionnaire_schema()
    expected_count = get_question_count()
    
    # Check if we need to reload
    existing_questions = db.get_all_questions()
    current_count = len(existing_questions) if existing_questions else 0
    
    if current_count != expected_count:
        print(f"[!] Question count mismatch: DB has {current_count}, Schema has {expected_count}")
        print("[*] Clearing old questions and reloading...")
        
        # Clear old questions
        db.clear_questions()
        
        # Load new questions from schema
        for section_name, questions in schema.items():
            for idx, question in enumerate(questions):
                question_data = {
                    "section": section_name,
                    "question_text": question["question_text"],
                    "question_type": question["question_type"],
                    "order": idx,
                    "required": question.get("required", True)
                }
                db.add_question(question_data)
        print(f"[✓] Loaded {expected_count} questions from schema")
    else:
        print(f"[OK] Questions already loaded ({current_count} questions)")
    
    stats = db.get_statistics()
    print(f"[Stats] Questions: {stats['total_questions']}, Companies: {stats['total_companies']}, Assessments: {stats['total_assessments']}")
    print("[OK] API Ready!")
    
    
    # Print registered routes
    print("\n[DEBUG] Registered Routes:")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"  - {route.path} [{','.join(route.methods)}]")
    print("----------------------------\n")
    
    yield
    
    # Shutdown
    print("[*] Shutting down API...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Cyber Resilience Assessment API",
    description="Backend API for SBA Info Solutions Cyber Resilience Assessment Platform",
    version="1.0.0",
    lifespan=lifespan
)


# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"\n[Validation Error] {json.dumps(exc.errors(), indent=2)}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# ========================================
# PYDANTIC MODELS
# ========================================

class CompanyInfo(BaseModel):
    company_name: str
    contact_email: EmailStr
    contact_name: Optional[str] = ""
    designation: Optional[str] = ""
    current_backup_solution: Optional[str] = ""
    
    # Deprecated/Hidden fields (made optional)
    industry: Optional[str] = ""
    company_size: Optional[str] = ""
    state: Optional[str] = ""
    additional_notes: Optional[str] = ""

class QuestionResponse(BaseModel):
    question_id: str
    section: str
    question_text: str
    question_type: str
    answer: Union[str, List[str]]
    comment: Optional[str] = ""

class Assessment(BaseModel):
    company_info: CompanyInfo
    responses: List[QuestionResponse]

class AssessmentSubmit(BaseModel):
    assessment_id: str
    company_info: CompanyInfo
    responses: Dict[str, List[QuestionResponse]]

# ========================================
# API ENDPOINTS
# ========================================

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "Cyber Resilience Assessment API",
        "company": "SBA Info Solutions",
        "version": "1.0.0"
    }

@app.get("/api/config")
async def get_config():
    """Get application configuration"""
    return {
        "app_title": "Cyber Resilience Maturity Assessment",
        "app_subtitle": "Enterprise Cybersecurity Assessment Platform",
        "company_name": "SBA Info Solutions",
        "company_tagline": "Powered by SBA Info Solutions",
        "colors": {
            "primary": "#000000",
            "secondary": "#e7000b",
            "text": "#ffffff",
            "background": "#000000",
            "card_bg": "#1a1a1a"
        },
        "company_sizes": [
            "1-50 employees",
            "51-200 employees",
            "201-500 employees",
            "501-1000 employees",
            "1001-5000 employees",
            "5000+ employees"
        ],
        "industries": [
            "Banking & Financial Services",
            "Insurance",
            "Healthcare",
            "Government",
            "Energy & Utilities",
            "Telecommunications",
            "Manufacturing",
            "Retail & E-commerce",
            "Technology",
            "Transportation & Logistics",
            "Education",
            "Other"
        ],
        "states": [
            "Andhra Pradesh",
            "Arunachal Pradesh",
            "Assam",
            "Bihar",
            "Chhattisgarh",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Madhya Pradesh",
            "Maharashtra",
            "Manipur",
            "Meghalaya",
            "Mizoram",
            "Nagaland",
            "Odisha",
            "Punjab",
            "Rajasthan",
            "Sikkim",
            "Tamil Nadu",
            "Telangana",
            "Tripura",
            "Uttar Pradesh",
            "Uttarakhand",
            "West Bengal",
            "Andaman and Nicobar Islands",
            "Chandigarh",
            "Dadra and Nagar Haveli and Daman and Diu",
            "Delhi",
            "Jammu and Kashmir",
            "Ladakh",
            "Lakshadweep",
            "Puducherry"
        ]
    }

@app.get("/api/questionnaire/schema")
async def get_questionnaire():
    """Get complete questionnaire schema"""
    schema = get_questionnaire_schema()
    total_questions = get_question_count()
    
    return {
        "total_questions": total_questions,
        "sections": list(schema.keys()),
        "schema": schema
    }

@app.get("/api/questionnaire/sections")
async def get_sections():
    """Get list of all sections"""
    schema = get_questionnaire_schema()
    sections = []
    
    for section_name, questions in schema.items():
        sections.append({
            "name": section_name,
            "question_count": len(questions)
        })
    
    return {"sections": sections}

@app.post("/api/company/create")
async def create_company(company: CompanyInfo):
    """Create a new company and start assessment"""
    try:
        # Save company to database
        company_data = company.dict()
        company_id = db.add_company(company_data)
        
        # Create assessment
        assessment_id = db.create_assessment(company_id)
        
        return {
            "success": True,
            "company_id": company_id,
            "assessment_id": assessment_id,
            "message": "Company created and assessment started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/responses/save")
async def save_responses(assessment_id: str, responses: List[QuestionResponse]):
    """Save assessment responses"""
    try:
        for response in responses:
            response_data = {
                "assessment_id": assessment_id,
                "section": response.section,
                "question_id": response.question_id,
                "question_text": response.question_text,
                "question_type": response.question_type,
                "answer": response.answer,
                "comment": response.comment or ""
            }
            db.add_response(response_data)
        
        return {
            "success": True,
            "message": f"Saved {len(responses)} responses successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/assessment/submit")
async def submit_assessment(submission: AssessmentSubmit):
    """Submit completed assessment and calculate scores"""
    try:
        assessment_id = submission.assessment_id
        
        # Save all responses
        all_responses = []
        for section_responses in submission.responses.values():
            all_responses.extend(section_responses)
        
        # Save responses to database
        for response in all_responses:
            response_data = {
                "assessment_id": assessment_id,
                "section": response.section,
                "question_id": response.question_id,
                "question_text": response.question_text,
                "question_type": response.question_type,
                "answer": response.answer,
                "comment": response.comment or ""
            }
            db.add_response(response_data)
        
        # Update assessment status
        completed_sections = list(submission.responses.keys())
        db.update_assessment_status(assessment_id, "completed", completed_sections)
        
        # Calculate scores using new 12-question logic
        # We need to pass a dictionary of {question_id: answer} to the scorer
        scoring_responses = {}
        for r in all_responses:
            scoring_responses[r.question_id] = r.answer
            
        results = scorer.calculate_score(scoring_responses)
        
        return {
            "success": True,
            "assessment_id": assessment_id,
            "results": results,
            "company_info": submission.company_info.dict()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/assessment/{assessment_id}")
async def get_assessment(assessment_id: str):
    """Get assessment details"""
    try:
        assessment = db.get_assessment(assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        responses = db.get_responses_by_assessment(assessment_id)
        
        return {
            "assessment": assessment,
            "responses": responses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_statistics():
    """Get database statistics"""
    try:
        stats = db.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Import email sender
from utils.email_sender import send_assessment_email

class EmailRequest(BaseModel):
    email: EmailStr
    company_name: str
    results: Dict

from fastapi import BackgroundTasks

@app.post("/api/assessment/send-email")
async def send_report_email(request: EmailRequest, background_tasks: BackgroundTasks):
    """Send assessment report via email (Background Task)"""
    try:
        # Send in background to avoid blocking the UI
        background_tasks.add_task(
            send_assessment_email,
            request.email,
            request.company_name,
            request.results
        )
            
        return {"success": True, "message": "Report email has been queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":

    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

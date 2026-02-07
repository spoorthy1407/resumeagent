from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.resume_model import ResumeDB
from app.schemas.resume import ResumeUploadResponse, ResumeAnalysisResponse, ResumeOptimizeRequest
from app.services.openai_service import parse_resume_with_ai, analyze_resume, optimize_resume_for_job
import shutil
from pathlib import Path
import PyPDF2
from docx import Document
import json

# Keep the prefix here
router = APIRouter(prefix="/resumes", tags=["resumes"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    parse_with_ai: bool = True
):
    """Upload and extract text from resume (PDF or DOCX), optionally parse with AI"""
    
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text
    extracted_text = ""
    try:
        if file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(str(file_path))
        elif file.filename.endswith('.docx'):
            extracted_text = extract_text_from_docx(str(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
    
    # Parse with AI if requested
    parsed_data = None
    if parse_with_ai and extracted_text:
        try:
            parsed_data = await parse_resume_with_ai(extracted_text)
        except Exception as e:
            print(f"AI parsing failed: {str(e)}")
            # Continue without AI parsing
    
    # Save to database
    resume = ResumeDB(
        user_id=1,
        filename=file.filename,
        file_path=str(file_path),
        extracted_text=extracted_text,
        parsed_data=parsed_data
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return resume

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

@router.get("/{resume_id}", response_model=ResumeUploadResponse)
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Get resume by ID"""
    resume = db.query(ResumeDB).filter(ResumeDB.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.get("/")
async def list_resumes(db: Session = Depends(get_db)):
    """List all resumes"""
    resumes = db.query(ResumeDB).all()
    return resumes

@router.post("/{resume_id}/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume_endpoint(resume_id: int, db: Session = Depends(get_db)):
    """Analyze resume and provide improvement suggestions"""
    
    # Get resume from database
    resume = db.query(ResumeDB).filter(ResumeDB.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Make sure resume has parsed data
    if not resume.parsed_data:
        raise HTTPException(status_code=400, detail="Resume must be parsed first. Upload with parse_with_ai=true")
    
    # Analyze with AI
    try:
        analysis = await analyze_resume(resume.parsed_data)
        
        # Save analysis to database
        resume.ai_analysis = analysis
        db.commit()
        
        # Format response
        suggestions = analysis.get('improvements', []) + analysis.get('formatting_tips', [])
        
        return {
            "resume_id": resume_id,
            "analysis": analysis,
            "suggestions": suggestions,
            "ats_score": analysis.get('ats_score', 0)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@router.post("/optimize")
async def optimize_for_job(request: ResumeOptimizeRequest):
    """Optimize resume for a specific job posting"""
    
    try:
        optimization = await optimize_resume_for_job(
            resume_data=request.resume.dict(),
            job_description=request.job_description,
            target_role=request.target_role
        )
        
        return {
            "success": True,
            "optimization": optimization
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")
    
    
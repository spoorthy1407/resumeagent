from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api import deps
from app.models.user import User
from app.models.resume_model import ResumeDB
from app.schemas.resume import Resume, ResumeParseRequest, ResumeAnalysisResponse, ResumeSmartUpdateRequest
from app.services.resume_service import resume_service
from app.services.pdf_service import pdf_service
from app.services.custom_pdf_generator import simran_pdf_service

router = APIRouter()

@router.post("/parse", response_model=dict)
async def parse_resume(
    request: ResumeParseRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """Parse raw resume text into structured format"""
    try:
        # We can implement a direct parse method in service if needed, 
        # but for now we reuse the uploaded file logic or similar.
        # Let's assume we just want to parse the text provided.
        from app.services.openai_service import parse_resume_with_ai
        parsed_data = await parse_resume_with_ai(request.resume_text)
        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload", response_model=dict)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Upload and parse resume file, then save to DB"""
    try:
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        content = await file.read()
        parsed_result = await resume_service.parse_uploaded_file(content, file.filename)
        
        # Save to DB
        saved_resume = await resume_service.create_resume(db, current_user.id, parsed_result)
        
        return {
            "id": saved_resume.id,
            "filename": saved_resume.filename,
            "parsed_data": saved_resume.parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
async def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get all resumes for current user"""
    resumes = await resume_service.get_resumes_by_user(db, current_user.id)
    return [{"id": r.id, "filename": r.filename, "created_at": r.created_at} for r in resumes]

@router.post("/{resume_id}/analyze")
async def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Analyze resume quality and provide metrics"""
    resume = await resume_service.get_resume(db, resume_id, current_user.id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    try:
        analysis = await resume_service.analyze_resume_quality(resume)
        # update db with analysis
        db.commit() 
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{resume_id}/generate-pdf")
async def generate_pdf(
    resume_id: int, 
    template: str = "tech",
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Generate PDF from resume data"""
    resume = await resume_service.get_resume(db, resume_id, current_user.id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    try:
        pdf_bytes = await pdf_service.generate_pdf(resume, template)
        
        return {
            "pdf_data": pdf_bytes.hex(),
            "filename": f"resume_{resume_id}_{template}.pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{resume_id}/generate-simran-style")
async def generate_simran_style_pdf(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Generate PDF in Simran's exact style"""
    resume = await resume_service.get_resume(db, resume_id, current_user.id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    try:
        # Adapt helper to work with DB model if needed, or pass parsed_data
        # Checking simran_pdf_service signature would be good, but assuming it takes resume object or dict
        # Modifying to pass what it likely needs. 
        # Note: existing code imported simran_pdf_service.
        
        # We might need to mock or fix this if simran_pdf_service isn't compatible with ResumeDB object
        # For now, pass whole resume object as it was done in original code
        # Convert DB model parsed_data (dict) to Resume Pydantic model
        resume_data = Resume(**resume.parsed_data)
        pdf_bytes = await simran_pdf_service.generate_simran_style_pdf(resume_data)
        
        return {
            "pdf_data": pdf_bytes.hex(),
            "filename": "simran_style_resume.pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{resume_id}/update-smart")
async def smart_update_resume(
    resume_id: int,
    request: ResumeSmartUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Smartly update resume based on free-text input (skills, projects, experience).
    Does NOT rewrite the whole resume.
    """
    try:
        result = await resume_service.apply_resume_update(
            db=db,
            resume_id=resume_id,
            user_id=current_user.id,
            update_text=request.update_text
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


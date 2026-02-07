from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.resume_model import ResumeDB
from app.services.job_matching_service import (
    match_resume_to_job,
    find_suitable_jobs,
    suggest_career_paths,
    generate_cover_letter
)
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/jobs", tags=["job-matching"])


class JobMatchRequest(BaseModel):
    resume_id: int
    job_description: str


class JobListingInput(BaseModel):
    id: str
    title: str
    company: str
    description: str
    location: Optional[str] = None
    salary: Optional[str] = None


class JobSearchRequest(BaseModel):
    resume_id: int
    job_listings: List[JobListingInput]


class CoverLetterRequest(BaseModel):
    resume_id: int
    job_description: str
    company_name: str
    role_title: str


@router.post("/match")
async def match_job(request: JobMatchRequest, db: Session = Depends(get_db)):
    """
    Match a resume to a specific job description
    """
    # Get resume from database
    resume = db.query(ResumeDB).filter(ResumeDB.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Resume must be parsed first. Upload with parse_with_ai=true"
        )
    
    try:
        match_result = await match_resume_to_job(
            resume_data=resume.parsed_data,
            job_description=request.job_description
        )
        
        return {
            "resume_id": request.resume_id,
            "match_result": match_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching job: {str(e)}")


@router.post("/search")
async def search_jobs(request: JobSearchRequest, db: Session = Depends(get_db)):
    """
    Search and rank jobs based on resume
    """
    # Get resume from database
    resume = db.query(ResumeDB).filter(ResumeDB.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Resume must be parsed first. Upload with parse_with_ai=true"
        )
    
    try:
        # Convert Pydantic models to dicts
        job_listings = [job.dict() for job in request.job_listings]
        
        ranked_jobs = await find_suitable_jobs(
            resume_data=resume.parsed_data,
            job_listings=job_listings
        )
        
        return {
            "resume_id": request.resume_id,
            "total_jobs": len(ranked_jobs),
            "ranked_jobs": ranked_jobs
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")


@router.get("/{resume_id}/career-suggestions")
async def get_career_suggestions(resume_id: int, db: Session = Depends(get_db)):
    """
    Get career path suggestions based on resume
    """
    # Get resume from database
    resume = db.query(ResumeDB).filter(ResumeDB.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Resume must be parsed first. Upload with parse_with_ai=true"
        )
    
    try:
        suggestions = await suggest_career_paths(resume_data=resume.parsed_data)
        
        return {
            "resume_id": resume_id,
            "career_suggestions": suggestions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")


@router.post("/cover-letter")
async def create_cover_letter(request: CoverLetterRequest, db: Session = Depends(get_db)):
    """
    Generate a tailored cover letter for a job
    """
    # Get resume from database
    resume = db.query(ResumeDB).filter(ResumeDB.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Resume must be parsed first. Upload with parse_with_ai=true"
        )
    
    try:
        cover_letter = await generate_cover_letter(
            resume_data=resume.parsed_data,
            job_description=request.job_description,
            company_name=request.company_name,
            role_title=request.role_title
        )
        
        return {
            "resume_id": request.resume_id,
            "company": request.company_name,
            "role": request.role_title,
            "cover_letter": cover_letter
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cover letter: {str(e)}")
    
    
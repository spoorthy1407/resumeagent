from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Experience(BaseModel):
    title: str
    company: str
    duration: str
    location: Optional[str] = None
    bullets: List[str] = []

class Education(BaseModel):
    degree: str
    school: str
    year: str
    gpa: Optional[str] = None
    location: Optional[str] = None

class Resume(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    phone: str
    location: Optional[str] = None
    summary: Optional[str] = None
    experience: List[Experience] = []
    education: List[Education] = []
    skills: List[str] = []
    certifications: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ResumeParseRequest(BaseModel):
    resume_text: str

class ResumeOptimizeRequest(BaseModel):
    resume: Resume
    job_description: str
    target_role: Optional[str] = None

class ResumeCreate(Resume):
    pass

class ResumeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    skills: Optional[List[str]] = None
    certifications: Optional[List[str]] = None

# Add these new schemas for our API
class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume"""
    id: int
    filename: str
    extracted_text: Optional[str] = None
    parsed_data: Optional[Resume] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeAnalysisResponse(BaseModel):
    """Response for AI analysis"""
    resume_id: int
    analysis: dict
    suggestions: List[str]
    ats_score: Optional[float] = None

class ResumeSmartUpdateRequest(BaseModel):
    update_text: str


    
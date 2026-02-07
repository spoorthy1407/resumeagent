from pydantic import BaseModel
from typing import List, Optional

class JobRequirements(BaseModel):
    required_skills: List[str]
    preferred_qualifications: List[str]
    key_responsibilities: List[str]
    ats_keywords: List[str]
    industry: str
    experience_level: str
    role_type: str

class JobMatchResult(BaseModel):
    overall_score: float
    breakdown: dict
    missing_skills: List[str]
    matched_skills: List[str]
    recommendations: List[str]

class JobAnalysisRequest(BaseModel):
    job_description: str

    
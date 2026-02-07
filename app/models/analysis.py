from pydantic import BaseModel
from typing import List, Dict, Optional

class ATSAnalysis(BaseModel):
    ats_score: int
    critical_issues: List[str]
    recommendations: List[str]
    keyword_density: Dict[str, int]
    formatting_score: int

class ResumeAnalytics(BaseModel):
    word_count: int
    readability_score: float
    experience_count: int
    skills_count: int
    quantified_achievements: int
    action_verb_strength: float

class ImprovementSuggestion(BaseModel):
    section: str
    priority: str  # high, medium, low
    suggestion: str
    example: Optional[str] = None

    
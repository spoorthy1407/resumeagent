from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.models.resume import Resume

class PDFFormatPreferences(BaseModel):
    fonts: Dict[str, str] = {"primary": "Helvetica", "secondary": "Helvetica-Bold"}
    colors: Dict[str, str] = {"primary": "#000000", "accent": "#2C3E50"}
    spacing: Dict[str, int] = {"section": 15, "paragraph": 8, "line": 3}
    margins: Dict[str, float] = {"top": 0.5, "bottom": 0.5, "left": 0.75, "right": 0.75}
    alignment: Dict[str, str] = {"header": "center", "content": "left"}
    font_sizes: Dict[str, int] = {
        "name": 22,
        "contact": 11,
        "section_header": 14,
        "job_header": 11,
        "bullet": 10,
        "summary": 11
    }

class LayoutRequirements(BaseModel):
    section_order: List[str] = ["header", "summary", "experience", "education", "skills", "certifications"]
    header_style: str = "centered_with_contact"
    section_headers: str = "bold_with_underline"
    bullet_style: str = "standard_bullets"
    spacing_rules: str = "moderate"
    page_breaks: List[str] = []

class TrainingExample(BaseModel):
    id: str
    resume_data: Resume
    desired_format: PDFFormatPreferences
    layout_requirements: LayoutRequirements
    example_pdf_path: Optional[str] = None
    notes: Optional[str] = None

class TrainingRequest(BaseModel):
    examples: List[TrainingExample]
    training_name: str
    description: Optional[str] = None

class TrainingResult(BaseModel):
    training_id: str
    patterns_learned: List[Dict]
    style_preferences: PDFFormatPreferences
    layout_rules: LayoutRequirements
    accuracy_score: Optional[float] = None
    training_summary: str

    
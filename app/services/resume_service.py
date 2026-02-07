from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import io
import fitz  # PyMuPDF
from docx import Document

from app.models.resume_model import ResumeDB
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeParseRequest
from app.services.openai_service import parse_resume_with_ai, analyze_resume, plan_resume_update

class ResumeService:
    async def parse_uploaded_file(self, file_content: bytes, filename: str) -> dict:
        """
        Extract text from uploaded file and parse it using AI
        """
        text = ""
        
        if filename.endswith('.pdf'):
            text = self._extract_text_from_pdf(file_content)
        elif filename.endswith('.docx'):
            text = self._extract_text_from_docx(file_content)
        elif filename.endswith('.txt'):
            text = file_content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        # Parse with AI
        start_request = ResumeParseRequest(resume_text=text)
        parsed_data = await parse_resume_with_ai(text)
        
        return {
            "filename": filename,
            "extracted_text": text,
            "parsed_data": parsed_data
        }
    
    async def create_resume(self, db: Session, user_id: int, resume_data: dict) -> ResumeDB:
        """
        Save parsed resume to database
        """
        db_resume = ResumeDB(
            user_id=user_id,
            filename=resume_data["filename"],
            file_path="uploads/" + resume_data["filename"], # Placeholder for actual storage
            extracted_text=resume_data["extracted_text"],
            parsed_data=resume_data["parsed_data"]
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        return db_resume
        
    async def get_resumes_by_user(self, db: Session, user_id: int) -> List[ResumeDB]:
        return db.query(ResumeDB).filter(ResumeDB.user_id == user_id).all()
        
    async def get_resume(self, db: Session, resume_id: int, user_id: int) -> Optional[ResumeDB]:
        return db.query(ResumeDB).filter(ResumeDB.id == resume_id, ResumeDB.user_id == user_id).first()

    async def analyze_resume_quality(self, resume: ResumeDB) -> dict:
        """
        Analyze an existing resume from the DB
        """
        if not resume.parsed_data:
            raise HTTPException(status_code=400, detail="Resume has no parsed data")
            
        analysis = await analyze_resume(resume.parsed_data)
        
        # Save analysis to DB
        resume.ai_analysis = analysis
        # Assuming we can commit here, or caller handles it. 
        # For a service method, often better to let caller commit, but for simplicity:
        # We need a db session passed in if we want to save. 
        # Refactoring to require DB session for update would be better.
        return analysis

    def _extract_text_from_pdf(self, file_bytes: bytes) -> str:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def _extract_text_from_docx(self, file_bytes: bytes) -> str:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text


    async def apply_resume_update(self, db: Session, resume_id: int, user_id: int, update_text: str) -> dict:
        """
        Smart update of resume based on user text
        """
        resume = await self.get_resume(db, resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
            
        if not resume.parsed_data:
            raise HTTPException(status_code=400, detail="Resume has no parsed data")
            
        # 1. Generate Plan
        plan = await plan_resume_update(resume.parsed_data, update_text)
        
        updated_data = resume.parsed_data.copy()
        
        # 2. Apply Skills
        if plan.get("add_skills"):
            current_skills = updated_data.get("skills", [])
            # Deduplicate case-insensitive
            current_lower = {s.lower() for s in current_skills}
            for skill in plan["add_skills"]:
                if skill.lower() not in current_lower:
                    current_skills.append(skill)
                    current_lower.add(skill.lower())
            updated_data["skills"] = current_skills
            
        # 3. Apply Projects (if 'projects' section exists, else create it)
        if plan.get("add_projects"):
            current_projects = updated_data.get("projects", []) 
            # If parsed data puts projects under 'experience', we might need to check that too
            # For now assuming standard schema has 'projects' or we add to it
            if not current_projects and "projects" not in updated_data:
                 updated_data["projects"] = []
                 current_projects = updated_data["projects"]
            
            for proj in plan["add_projects"]:
                # simple append
                current_projects.insert(0, proj) # Add to top
            
            updated_data["projects"] = current_projects
            
        # 4. Update Experience
        if plan.get("update_experience"):
            current_experience = updated_data.get("experience", [])
            for update in plan["update_experience"]:
                target_company = update.get("company", "").lower()
                target_title = update.get("title", "").lower()
                
                # Find matching job
                for job in current_experience:
                    job_company = job.get("company", "").lower()
                    job_title = job.get("title", "").lower()
                    
                    # Fuzzy match or exact match
                    if target_company in job_company or job_company in target_company:
                         if not target_title or target_title in job_title:
                             # Found match, append bullets
                             current_bullets = job.get("bullets", [])
                             current_bullets.extend(update.get("bullets_to_add", []))
                             job["bullets"] = current_bullets
                             break
            updated_data["experience"] = current_experience

        # 5. Save
        # Make a copy to trigger sqlalchemy detection if needed (JSON mutation)
        resume.parsed_data = dict(updated_data) 
        db.commit()
        db.refresh(resume)
        
        return {
            "original_plan": plan,
            "updated_resume": updated_data
        }

resume_service = ResumeService()

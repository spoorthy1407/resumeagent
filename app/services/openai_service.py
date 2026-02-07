from openai import OpenAI
from app.core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def parse_resume_with_ai(extracted_text: str) -> dict:
    """
    Parse resume text into structured data using OpenAI
    """
    prompt = f"""
    Parse the following resume text and extract structured information.
    Return a JSON object with these fields:
    - name (string)
    - email (string)
    - phone (string)
    - location (string or null)
    - summary (string or null)
    - experience (array of objects with: title, company, duration, location, bullets)
    - education (array of objects with: degree, school, year, gpa, location)
    - skills (array of strings)
    - certifications (array of strings)
    
    Resume text:
    {extracted_text}
    
    Return ONLY valid JSON, no additional text.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a resume parsing assistant. Extract structured data from resumes and return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        parsed_data = json.loads(response.choices[0].message.content)
        return parsed_data
    
    except Exception as e:
        raise Exception(f"Error parsing resume with AI: {str(e)}")


async def analyze_resume(parsed_resume: dict) -> dict:
    """
    Analyze resume and provide suggestions for improvement
    """
    prompt = f"""
    Analyze this resume and provide:
    1. Overall strengths (3-5 points)
    2. Areas for improvement (3-5 points)
    3. ATS compatibility score (0-100)
    4. Keyword suggestions for better ATS ranking
    5. Formatting recommendations
    
    Resume data:
    {json.dumps(parsed_resume, indent=2)}
    
    Return as JSON with keys: strengths, improvements, ats_score, keywords, formatting_tips
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume analyst. Provide actionable feedback to improve resumes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    
    except Exception as e:
        raise Exception(f"Error analyzing resume: {str(e)}")


async def optimize_resume_for_job(resume_data: dict, job_description: str, target_role: str = None) -> dict:
    """
    Optimize resume for a specific job posting
    """
    role_context = f"for the role of {target_role}" if target_role else ""
    
    prompt = f"""
    Optimize this resume {role_context} based on the job description below.
    Provide:
    1. Tailored summary/objective
    2. Skills to emphasize
    3. Experience bullet points to highlight or rewrite
    4. Keywords to add
    5. Overall match score (0-100)
    
    Resume:
    {json.dumps(resume_data, indent=2)}
    
    Job Description:
    {job_description}
    
    Return as JSON with keys: tailored_summary, skills_to_emphasize, experience_updates, keywords_to_add, match_score, recommendations
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career coach specializing in resume optimization for job applications."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            response_format={"type": "json_object"}
        )
        
        optimization = json.loads(response.choices[0].message.content)
        return optimization
    
    except Exception as e:
        raise Exception(f"Error optimizing resume: {str(e)}")


async def plan_resume_update(current_resume: dict, update_text: str) -> dict:
    """
    Generate a structural update plan based on user text and current resume.
    """
    prompt = f"""
    You are a resume updating assistant. 
    Review the Current Resume and the User Update Text.
    Identify new skills, projects, or experience updates from the text.
    
    Current Resume:
    {json.dumps(current_resume, indent=2)}
    
    User Update Text:
    {update_text}
    
    Rules:
    1. Do NOT rewrite the resume.
    2. Only extract information explicitly present in the User Update Text.
    3. Determine where the new info belongs: 'add_skills', 'add_projects' (under experience or projects), or 'update_experience' (modifying existing).
    4. Return empty arrays if nothing fits.
    
    Output strictly as JSON:
    {{
      "add_skills": ["skill1", "skill2"],
      "add_projects": [
         {{ "title": "Project Title", "company": "Company/Context", "duration": "Duration", "bullets": ["bullet1", "bullet2"] }}
      ],
      "update_experience": [
         {{ "company": "Company Name", "title": "Title to Match", "bullets_to_add": ["new bullet"] }}
      ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise resume updater. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        plan = json.loads(response.choices[0].message.content)
        return plan
    
    except Exception as e:
        raise Exception(f"Error formulating resume update plan: {str(e)}")

    
    
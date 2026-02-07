from openai import OpenAI
from app.core.config import settings
import json
from typing import List, Dict

client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def match_resume_to_job(resume_data: dict, job_description: str) -> dict:
    """
    Match a resume to a job description and provide compatibility score
    """
    prompt = f"""
    Analyze how well this resume matches the job description.
    
    Resume:
    {json.dumps(resume_data, indent=2)}
    
    Job Description:
    {job_description}
    
    Provide:
    1. Overall match score (0-100)
    2. Matching skills (list)
    3. Missing skills (list)
    4. Experience relevance score (0-100)
    5. Key strengths for this role (3-5 points)
    6. Gaps to address (3-5 points)
    7. Recommendation (apply/skip/improve first)
    
    Return as JSON with keys: match_score, matching_skills, missing_skills, experience_score, strengths, gaps, recommendation
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a recruitment AI that matches candidates to job postings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        match_result = json.loads(response.choices[0].message.content)
        return match_result
    
    except Exception as e:
        raise Exception(f"Error matching resume to job: {str(e)}")


async def find_suitable_jobs(resume_data: dict, job_listings: List[dict]) -> List[dict]:
    """
    Find and rank suitable jobs from a list of job postings
    """
    results = []
    
    for job in job_listings:
        match_result = await match_resume_to_job(resume_data, job.get('description', ''))
        
        results.append({
            "job_id": job.get('id'),
            "job_title": job.get('title'),
            "company": job.get('company'),
            "match_score": match_result.get('match_score', 0),
            "matching_skills": match_result.get('matching_skills', []),
            "missing_skills": match_result.get('missing_skills', []),
            "recommendation": match_result.get('recommendation', 'unknown')
        })
    
    # Sort by match score (highest first)
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    return results


async def suggest_career_paths(resume_data: dict) -> dict:
    """
    Suggest potential career paths based on resume
    """
    prompt = f"""
    Based on this resume, suggest potential career paths and roles.
    
    Resume:
    {json.dumps(resume_data, indent=2)}
    
    Provide:
    1. Current career level (entry/mid/senior/executive)
    2. Suggested next roles (5-7 role titles)
    3. Skills to develop for career growth (5-7 skills)
    4. Industries to consider (3-5 industries)
    5. Potential career pivots (2-3 alternative paths)
    
    Return as JSON with keys: current_level, suggested_roles, skills_to_develop, industries, career_pivots
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career counselor providing career path guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            response_format={"type": "json_object"}
        )
        
        suggestions = json.loads(response.choices[0].message.content)
        return suggestions
    
    except Exception as e:
        raise Exception(f"Error suggesting career paths: {str(e)}")


async def generate_cover_letter(resume_data: dict, job_description: str, company_name: str, role_title: str) -> str:
    """
    Generate a tailored cover letter for a job application
    """
    prompt = f"""
    Write a professional cover letter for this job application.
    
    Candidate Resume:
    {json.dumps(resume_data, indent=2)}
    
    Job Title: {role_title}
    Company: {company_name}
    Job Description:
    {job_description}
    
    The cover letter should:
    - Be 3-4 paragraphs
    - Highlight relevant experience
    - Show enthusiasm for the role
    - Mention specific skills that match the job
    - Be professional but personable
    - End with a call to action
    
    Return ONLY the cover letter text, no JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        cover_letter = response.choices[0].message.content
        return cover_letter
    
    except Exception as e:
        raise Exception(f"Error generating cover letter: {str(e)}")
    
    
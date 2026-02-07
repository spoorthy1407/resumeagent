import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.resume_service import resume_service
from app.models.resume_model import ResumeDB

@pytest.mark.asyncio
async def test_apply_resume_update_logic():
    # Mock data
    initial_resume_data = {
        "skills": ["Python", "FastAPI"],
        "projects": [],
        "experience": [
            {
                "company": "Tech Corp",
                "title": "Developer",
                "bullets": ["Wrote code"]
            }
        ]
    }
    
    mock_plan = {
        "add_skills": ["Docker", "Kubernetes"],
        "add_projects": [
            {
                "title": "New AI App",
                "company": "Personal",
                "duration": "2024",
                "bullets": ["Built an agent"]
            }
        ],
        "update_experience": [
            {
                "company": "Tech Corp",
                "title": "Developer",
                "bullets_to_add": ["Led team meeting"]
            }
        ]
    }
    
    # Mock DB Session and Resume Object
    mock_db = MagicMock()
    mock_resume = MagicMock(spec=ResumeDB)
    mock_resume.id = 1
    mock_resume.user_id = 1
    mock_resume.parsed_data = initial_resume_data.copy()
    
    # Mock get_resume to return our mock object
    with patch.object(resume_service, 'get_resume', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_resume
        
        # Mock OpenAI planner to return deterministic plan
        with patch('app.services.resume_service.plan_resume_update', new_callable=AsyncMock) as mock_plan_func:
            mock_plan_func.return_value = mock_plan
            
            # Execute
            result = await resume_service.apply_resume_update(
                db=mock_db,
                resume_id=1,
                user_id=1,
                update_text="I learned Docker and built an AI app."
            )
            
            # Verify Results
            updated_data = result["updated_resume"]
            
            # 1. Check Skills Added
            assert "Docker" in updated_data["skills"]
            assert "Kubernetes" in updated_data["skills"]
            assert "Python" in updated_data["skills"]
            
            # 2. Check Project Added
            assert len(updated_data["projects"]) == 1
            assert updated_data["projects"][0]["title"] == "New AI App"
            
            # 3. Check Experience Updated
            tech_corp = next(j for j in updated_data["experience"] if j["company"] == "Tech Corp")
            assert "Led team meeting" in tech_corp["bullets"]
            assert "Wrote code" in tech_corp["bullets"]
            
            # 4. Verify DB Commit
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()

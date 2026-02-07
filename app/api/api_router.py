from fastapi import APIRouter
from .resume import router as resume_router
from .routes.auth import router as auth_router

router = APIRouter()

# Include the resume router
router.include_router(resume_router, prefix="/resumes", tags=["resumes"])
router.include_router(auth_router, tags=["login"])


# You can add your API endpoints here later
# Example:
# @router.get("/health")
# async def health_check():
#     return {"status": "healthy"}


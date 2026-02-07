from fastapi import APIRouter
from .resume import router as resume_router
from .job_matching import router as job_router
from .analysis import router as analysis_router
from .training import router as training_router

api_router = APIRouter()

api_router.include_router(resume_router, prefix="/resume", tags=["resume"])
api_router.include_router(job_router, prefix="/jobs", tags=["job-matching"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
api_router.include_router(training_router, prefix="/training", tags=["training"])


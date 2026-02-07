from fastapi import FastAPI  # Fixed: was "rom" instead of "from"
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.base import Base  # Import Base
from app.core.database import engine  # Import engine
from app.api.api_router import router as api_router  # Moved imports to top

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-powered resume optimization and job matching API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Resume Agent API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include API router with prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

# Create all tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
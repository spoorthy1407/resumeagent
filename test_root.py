print("Starting import test...")

print("1. Importing settings...")
from app.core.config import settings
print("   ✓ Settings imported")

print("2. Importing FastAPI...")
from fastapi import FastAPI
print("   ✓ FastAPI imported")

print("3. Creating app...")
app = FastAPI(title="Test")
print("   ✓ App created")

print("4. Importing api_router...")
from app.api.api_router import router as api_router
print("   ✓ Router imported")

print("5. Including router...")
app.include_router(api_router)
print("   ✓ Router included")

print("\n✅ All imports successful!")


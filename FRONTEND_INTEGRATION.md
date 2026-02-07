# Frontend Integration Guide

## What's Connected

✅ **Frontend**: Next.js app in `src/app/`  
✅ **Backend**: FastAPI server in `app/`  
✅ **Environment**: `.env.local` configured with `NEXT_PUBLIC_API_URL`

## Running Locally

### Terminal 1 - Backend
```bash
python -m uvicorn app.main:app --reload
```
Backend runs on: `http://localhost:8000`

### Terminal 2 - Frontend
```bash
npm run dev
```
Frontend runs on: `http://localhost:3000`

## Features Demonstrated

The minimal frontend demonstrates:
1. **Authentication**: Signup and Login with JWT
2. **Resume Parsing**: Send text to backend, get structured JSON
3. **API Integration**: All requests use environment variable `NEXT_PUBLIC_API_URL`

## How It Works

### API Calls
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Example: Login
fetch(`${API_URL}/api/v1/login/access-token`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: `username=${email}&password=${password}`
});
```

### Environment Variables
- **Local**: `.env.local` → `NEXT_PUBLIC_API_URL=http://localhost:8000`
- **Production**: Vercel env → `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

## Deployment

See `DEPLOYMENT.md` for production deployment steps.

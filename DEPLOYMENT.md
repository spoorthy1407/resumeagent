# Deployment Guide

## Backend Deployment (FastAPI on Render)

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### 2. Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `spoorthy1407/resumeagent`
3. Configure:
   - **Name**: `resumeagent-backend`
   - **Root Directory**: Leave empty (or `.` for root)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: Generate with `openssl rand -hex 32`
   - `DATABASE_URL`: (Render provides PostgreSQL, or use SQLite for now)
5. Click **"Create Web Service"**

Your backend URL will be: `https://resumeagent-backend.onrender.com`

---

## Frontend Deployment (Next.js on Vercel)

### 1. Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign up with GitHub

### 2. Deploy Frontend
1. Click **"Add New Project"**
2. Import `spoorthy1407/resumeagent`
3. Configure:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `.` (or leave empty)
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://resumeagent-backend.onrender.com`
5. Click **"Deploy"**

Your frontend URL will be: `https://resumeagent.vercel.app`

---

## Testing Deployment

1. Visit frontend URL
2. Try signup/login
3. Upload a resume
4. Generate PDF

---

## Important Notes

- **CORS**: Backend must allow frontend origin. Update `app/main.py`:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://resumeagent.vercel.app"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

- **Database**: For production, use PostgreSQL (Render provides free tier)
- **Environment Variables**: Never commit `.env` to git (already in `.gitignore`)

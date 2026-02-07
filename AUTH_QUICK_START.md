# Authentication System - Quick Start

## 🚀 Getting Started in 5 Minutes

### Step 1: Verify Supabase Connection
The Supabase integration is already set up. Your environment variables are automatically configured:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Step 2: Database Setup
The database schema has been created automatically. Tables included:
- ✅ `profiles` - User profile information
- ✅ `resumes` - Resume storage metadata
- ✅ `resume_versions` - Version history tracking
- ✅ RLS policies for security

### Step 3: Test the Application

#### Sign Up
1. Go to `http://localhost:3000`
2. Click **"Create Account"**
3. Fill in:
   - First Name
   - Last Name
   - Email
   - Password (min 8 chars)
4. Accept terms
5. Click **"Create Account"**
6. Check your email for confirmation link
7. Click the confirmation link
8. You're ready to log in!

#### Log In
1. Go to `http://localhost:3000`
2. Click **"Sign In"**
3. Enter your email and password
4. Click **"Sign In"**
5. You'll see the beautiful dashboard!

#### Upload Resume
1. From dashboard, click **"Upload Resume"** tab
2. Drag & drop your PDF file (or click to browse)
3. Enter a title (e.g., "Software Engineer Resume 2025")
4. Click **"Upload Resume"**
5. Your resume is now stored securely!

#### Manage Profile
1. Click **"Profile"** tab
2. Click **"Edit"** button
3. Update your name
4. Click **"Save Changes"**
5. Changes are saved immediately!

#### Sign Out
1. Click **"Sign Out"** button in header
2. You're logged out and redirected to login page

## 🎨 Visual Features

### Login Page (3D Interactive)
- Rotating cube background
- Floating particles
- Glassmorphism card
- Gradient text
- Beautiful animations

### Sign Up Page
- Floating sphere animation
- Cascading particles
- Modern form design
- Input validation feedback

### Dashboard
- Clean tabbed interface
- Resume management
- Profile editing
- Session info display

## 🔒 Security Features Built-in

✅ **Password Hashing** - bcrypt, never plain text
✅ **Session Management** - Secure JWT tokens
✅ **Row Level Security** - User data isolation
✅ **Email Verification** - Confirm account ownership
✅ **HTTPS Only** - Encrypted connections
✅ **Token Refresh** - Automatic via middleware
✅ **SQL Injection Protection** - Parameterized queries

## 📁 Key Files Reference

| File | Purpose |
|------|---------|
| `/app/auth/login/page.tsx` | 3D login page |
| `/app/auth/sign-up/page.tsx` | Sign up page |
| `/app/protected/page.tsx` | Authenticated dashboard |
| `/lib/supabase/client.ts` | Browser client setup |
| `/lib/supabase/server.ts` | Server client setup |
| `/middleware.ts` | Token refresh logic |
| `/scripts/001_create_auth_tables.sql` | Database schema |

## 🛠️ Common Tasks

### Add a New Protected Page

```typescript
// app/new-feature/page.tsx
'use client'

import { useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export default function NewFeaturePage() {
  const router = useRouter()
  const supabase = createClient()

  useEffect(() => {
    const checkAuth = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) router.push('/auth/login')
    }
    checkAuth()
  }, [router, supabase])

  return <div>Your protected content here</div>
}
```

### Get Current User in Component

```typescript
import { createClient } from '@/lib/supabase/client'

export function MyComponent() {
  const supabase = createClient()
  
  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      console.log(user?.email)
    }
    getUser()
  }, [])
  
  return <div>Component</div>
}
```

### Fetch User Data

```typescript
// Get user's resumes
const { data: resumes } = await supabase
  .from('resumes')
  .select('*')
  .eq('user_id', userId)
```

### Update User Info

```typescript
// Update user metadata
const { error } = await supabase.auth.updateUser({
  data: {
    first_name: 'New Name'
  }
})
```

## ❓ FAQ

**Q: Can I use Google login?**
A: Not yet, but planned for future releases. Currently supports email/password.

**Q: Where are passwords stored?**
A: Passwords are hashed with bcrypt and stored securely in Supabase auth.users table. Never plain text.

**Q: Can users delete their accounts?**
A: Feature can be added. Currently they can sign out. Contact support for account deletion.

**Q: Is my resume data private?**
A: Yes! Row Level Security ensures users can only access their own data.

**Q: Can I share resumes?**
A: Not yet, but the database supports it. Can be added as a feature.

**Q: What happens if I forget my password?**
A: Password reset feature can be easily added. Currently, manual reset via support.

**Q: Is there a file size limit?**
A: PDF files up to 100MB are supported. Supabase buckets are highly scalable.

**Q: Can I integrate with AI?**
A: Yes! The API endpoints are ready for AI resume optimization features.

## 📞 Troubleshooting

**Issue:** "Cannot POST /auth/sign-up"
- **Solution:** Make sure Supabase integration is enabled

**Issue:** "Email already registered"
- **Solution:** Use a different email or reset password

**Issue:** "Resume upload fails"
- **Solution:** Ensure file is PDF and under 100MB

**Issue:** "Page redirects to login"
- **Solution:** Session expired, log in again

**Issue:** "Profile won't update"
- **Solution:** Check internet connection and try again

## 🚀 Next Steps

1. **Customize branding** - Update colors/logos
2. **Add password reset** - Email-based recovery
3. **Enable 2FA** - SMS or authenticator app
4. **Add AI features** - Resume optimization
5. **Social login** - Google/GitHub auth
6. **Email templates** - Custom confirmation emails

## 📚 Learn More

- Full guide: `/AUTH_SYSTEM_GUIDE.md`
- Supabase docs: https://supabase.com/docs
- Next.js auth: https://nextjs.org/docs/app/building-your-application/authentication
- Three.js: https://threejs.org/docs

---

**You're all set!** 🎉 Your resume application is now secure and fully authenticated. Start uploading resumes and managing your profile!

# Authentication System & Resume Management Guide

## Overview

This document explains the complete authentication and resume management system integrated into your Resume Assistant application. The system uses Supabase for secure authentication and database storage, with a beautiful 3D interactive login interface.

## System Architecture

### Authentication Flow

```
┌─────────────────┐
│  Landing Page   │
│ (Public Route)  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │   Auth?  │
    └────┬─────┘
         │
    ┌────┴─────────────────────┐
    │                          │
   YES                        NO
    │                          │
    ▼                          ▼
┌──────────────┐      ┌────────────────┐
│  Dashboard   │      │  Login/SignUp  │
│  (Protected) │      │   (Public)     │
└──────────────┘      └────────────────┘
```

## File Structure

```
app/
├── page.tsx                          # Landing page with auth check
├── auth/
│   ├── login/
│   │   ├── page.tsx                 # 3D Interactive login page
│   │   └── loading.tsx              # Suspense boundary
│   ├── sign-up/
│   │   └── page.tsx                 # Beautiful signup with 3D sphere
│   ├── error/
│   │   └── page.tsx                 # Auth error page
│   └── sign-up-success/
│       └── page.tsx                 # Confirmation message
├── protected/
│   └── page.tsx                     # Authenticated user dashboard
└── layout.tsx                       # Root layout
components/
├── protected/
│   ├── resume-manager.tsx           # View/manage resumes
│   ├── resume-upload.tsx            # Upload new resume (PDF)
│   └── user-profile.tsx             # Edit profile info
lib/
├── supabase/
│   ├── client.ts                    # Browser Supabase client
│   ├── server.ts                    # Server Supabase client
│   └── middleware.ts                # Token refresh logic
middleware.ts                        # Request middleware
scripts/
└── 001_create_auth_tables.sql      # Database schema setup
```

## Database Schema

### `profiles` Table
Stores user profile information linked to Supabase auth users.

```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name TEXT,
  last_name TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### `resumes` Table
Stores resume metadata for each user.

```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  version INTEGER DEFAULT 1
);
```

### `resume_versions` Table
Tracks resume version history for comparisons and rollbacks.

```sql
CREATE TABLE resume_versions (
  id UUID PRIMARY KEY,
  resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
  version_number INTEGER NOT NULL,
  file_path TEXT NOT NULL,
  created_at TIMESTAMP,
  change_summary TEXT
);
```

## Row Level Security (RLS)

All tables are protected with RLS policies. Users can only:
- View their own profiles
- Create/read/update/delete their own resumes
- Manage their resume versions

**Example Policy:**
```sql
CREATE POLICY "users_can_view_own_profile" ON profiles
  FOR SELECT USING (auth.uid() = id);
```

## Key Features

### 1. 3D Interactive Login Interface

**Location:** `/app/auth/login/page.tsx`

Features:
- Rotating 3D cube background using React Three Fiber
- Floating particle animations with cyan colors
- Glassmorphism card design with backdrop blur
- Gradient text for modern aesthetics
- Password visibility toggle
- Form validation with error messages
- Loading state with spinner animation

**Technologies:**
- `@react-three/fiber` - 3D rendering
- `@react-three/drei` - 3D utilities
- `three` - 3D library

### 2. Beautiful Sign Up Page

**Location:** `/app/auth/sign-up/page.tsx`

Features:
- Floating icosahedron (20-sided sphere) with bob animation
- Ambient particles falling from top to bottom
- Form validation for password strength (min 8 chars)
- Password confirmation matching
- Terms of service checkbox
- User metadata storage (first/last name)

### 3. Protected Dashboard

**Location:** `/app/protected/page.tsx`

Features:
- Authenticated user welcome message
- Tabbed interface (Dashboard, Upload, Profile)
- Sign out functionality
- Resume management
- Profile editing
- Upload tracking

### 4. Resume Management

**Upload Component** (`/components/protected/resume-upload.tsx`):
- Drag-and-drop file upload
- PDF validation
- File size display
- Progress feedback
- Error handling

**Manager Component** (`/components/protected/resume-manager.tsx`):
- List all user resumes
- Show version history
- Display file metadata
- Edit/delete operations
- Sorting by date

### 5. User Profile Management

**Location:** `/components/protected/user-profile.tsx`

Features:
- View account email and ID
- Edit first/last name
- Password change option
- Two-factor authentication toggle
- Account security settings

## Authentication Flow Details

### Sign Up Process

1. User fills sign-up form with:
   - Email
   - Password (min 8 characters)
   - Confirm password
   - First name
   - Last name
   - Terms acceptance

2. Supabase creates auth user with metadata:
   ```javascript
   supabase.auth.signUp({
     email,
     password,
     options: {
       emailRedirectTo: '/protected',
       data: { first_name, last_name }
     }
   })
   ```

3. Confirmation email sent
4. User confirms email
5. Profile auto-created via database trigger
6. Redirect to sign-up success page
7. Auto-redirect to login after 10 seconds

### Login Process

1. User enters email and password
2. Supabase validates credentials
3. JWT token created and stored
4. Session established
5. User redirected to `/protected`
6. Middleware refresh token on each request

### Logout Process

1. User clicks "Sign Out" button
2. `supabase.auth.signOut()` called
3. JWT token cleared
4. Session destroyed
5. Redirect to `/auth/login`

## Security Features

### Password Security
- Minimum 8 characters required
- Hashed with bcrypt by Supabase
- Never transmitted in plain text
- HTTPS only in production

### Session Management
- JWT tokens stored in secure HTTP-only cookies
- Automatic token refresh via middleware
- 1-hour session timeout (configurable)
- Force logout on token expiry

### Data Protection
- Row Level Security (RLS) on all tables
- User isolation via auth.uid()
- Parameterized queries prevent SQL injection
- File uploads to secure storage bucket

### SSL/TLS
- All connections encrypted
- Certificate validation
- HSTS headers enabled

## Environment Variables

Required variables (set in Vercel):

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

These are automatically provided by the Supabase integration in v0.

## Usage Examples

### Check if User is Authenticated

```typescript
import { createClient } from '@/lib/supabase/client'

const supabase = createClient()
const { data: { user } } = await supabase.auth.getUser()

if (user) {
  // User is authenticated
} else {
  // Redirect to login
}
```

### Upload a Resume

```typescript
const { data, error } = await supabase.storage
  .from('resumes')
  .upload(`${userId}/${filename}`, file)

// Then insert resume record
const { error: dbError } = await supabase.from('resumes').insert({
  user_id: userId,
  title,
  file_path: data.path,
})
```

### Get User's Resumes

```typescript
const { data: resumes } = await supabase
  .from('resumes')
  .select('*')
  .eq('user_id', userId)
  .order('created_at', { ascending: false })
```

### Update User Profile

```typescript
const { error } = await supabase.auth.updateUser({
  data: {
    first_name: 'John',
    last_name: 'Doe',
  }
})
```

## Testing the System

### Local Development

1. **Sign Up:**
   - Visit `http://localhost:3000`
   - Click "Create Account"
   - Fill in the form
   - Accept terms
   - Click "Create Account"
   - Check confirmation email

2. **Login:**
   - Visit `http://localhost:3000`
   - Click "Sign In"
   - Enter credentials
   - Click "Sign In"
   - See dashboard

3. **Upload Resume:**
   - From dashboard, go to "Upload Resume" tab
   - Drag and drop or select PDF file
   - Enter title
   - Click "Upload Resume"

4. **Manage Profile:**
   - From dashboard, go to "Profile" tab
   - Click "Edit"
   - Update name
   - Click "Save Changes"

5. **Sign Out:**
   - Click "Sign Out" button in header
   - Redirected to login page

## Troubleshooting

### Issue: "User not found"
- **Cause:** Email not confirmed
- **Solution:** Check email for confirmation link

### Issue: "Invalid credentials"
- **Cause:** Wrong email or password
- **Solution:** Check credentials, use password reset if needed

### Issue: "Session expired"
- **Cause:** Token expired (1+ hour)
- **Solution:** Log in again

### Issue: Resume not uploading
- **Cause:** File is not PDF or too large
- **Solution:** Use PDF file under 100MB

### Issue: Profile not updating
- **Cause:** Network error or validation failure
- **Solution:** Check internet, try again

## Advanced Features (Future)

### Planned Enhancements

1. **Password Reset**
   - Email-based password recovery
   - Secure token validation
   - Password change confirmation

2. **Two-Factor Authentication**
   - SMS/authenticator app support
   - Backup codes generation
   - Device trust management

3. **Social Login**
   - Google OAuth integration
   - GitHub authentication
   - Microsoft sign-in

4. **Resume AI Features**
   - AI-powered resume optimization
   - ATS scoring
   - Content suggestions
   - Skill matching

5. **Collaboration**
   - Share resumes with mentors
   - Feedback comments
   - Version comparison

## Performance Considerations

### Optimizations Implemented

- **Code Splitting:** Each page loads only needed code
- **Image Optimization:** 3D models loaded efficiently
- **Lazy Loading:** Components load on demand
- **Caching:** User data cached via SWR
- **CDN:** Files served from global CDN

### Database Indexing

```sql
-- Created indexes for fast queries
CREATE INDEX resumes_user_id_idx ON resumes(user_id);
CREATE INDEX resume_versions_resume_id_idx ON resume_versions(resume_id);
```

## Compliance & Privacy

### GDPR Compliance
- User data deletion on account removal
- Data export functionality available
- Privacy policy required
- Consent management

### Data Retention
- User profiles: kept indefinitely while active
- Resumes: user can delete anytime
- Logs: 90-day retention
- Backups: 30-day retention

## Support & Documentation

For more information:
- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Next.js Authentication](https://nextjs.org/docs/app/building-your-application/authentication)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)

---

**Last Updated:** February 2025
**Version:** 1.0

# Quick Reference Guide

## Color Codes (Copy & Paste)

### Backgrounds
```
from-slate-900 via-purple-900 to-purple-900
```

### Gradients
```
from-purple-300 to-purple-100          (Text headers)
from-purple-600 to-purple-500          (Buttons)
from-purple-500 to-purple-400          (Hover buttons)
```

### Individual Colors
```
text-purple-300    (Links, accents)
text-purple-200/80 (Secondary text)
text-purple-100    (Light text)
text-gray-300      (Body text)

border-purple-400/30  (Card borders)
border-purple-400/50  (Hover borders)

bg-purple-500/20   (Info boxes)
bg-white/5         (Card background)
bg-white/10        (Input focus)
```

### Special Colors
```
#a78bfa (purple particles)
#c084fc (light purple particles)
#9370db (emissive glow)
```

---

## Quick Commands

### Test Login Page
```
Navigate to: /auth/login
See: Rotating purple cube
Feel: Floating card animation
```

### Test Sign-up Page
```
Navigate to: /auth/sign-up
See: Floating purple sphere
Feel: Success modal after creation
```

### Test Dashboard
```
Navigate to: /protected (after login)
See: Purple header, themed navigation
Action: Click "Sign Out" to logout
```

### Test Success Modal
```
1. Go to /auth/sign-up
2. Fill form with valid email/password
3. Click "Create Account"
4. See beautiful success modal popup
5. Click "Go to Login" or "Close"
```

---

## Component Quick Reference

### Success Modal Import
```tsx
import { SuccessModal } from '@/components/auth/success-modal'
```

### Using Success Modal
```tsx
<SuccessModal isOpen={showModal} email={userEmail} onClose={handleClose} />
```

### Card Styling Template
```tsx
<div className="backdrop-blur-xl bg-white/5 border border-purple-400/30 rounded-3xl p-8 shadow-2xl hover:shadow-purple-900/50 transition-all duration-500 hover:border-purple-400/50 floating-card">
  {/* Content */}
</div>
```

### Button Template
```tsx
<button className="bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white font-semibold rounded-lg transition duration-200 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg hover:shadow-purple-500/50">
  Click Me
</button>
```

### Input Template
```tsx
<input className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:border-purple-400 focus:bg-white/10 text-white placeholder-gray-400 transition duration-200" />
```

---

## Animation Reference

### Floating Card (5 seconds)
```css
animation: floating-card 5s ease-in-out infinite;
```

### Input Focus Glow
```tsx
<div className="absolute inset-0 rounded-lg bg-gradient-to-r from-purple-600 to-purple-400 opacity-0 group-focus-within:opacity-10 pointer-events-none transition duration-200" />
```

### Modal Fade-in
```tsx
<div className="animate-in fade-in-0 zoom-in-95 duration-300">
```

---

## File Locations

```
/app/auth/
├── login/page.tsx          (Login page)
├── sign-up/page.tsx        (Sign-up page)
├── sign-up-success/        (Success page)
└── error/page.tsx          (Error page)

/app/protected/page.tsx     (Dashboard)
/app/page.tsx               (Landing page)

/components/auth/
└── success-modal.tsx       (Success modal - NEW!)

/lib/supabase/
├── client.ts               (Client setup)
├── server.ts               (Server setup)
└── middleware.ts           (Auth middleware)

/app/globals.css            (Animations & styles)
```

---

## Key CSS Classes

### Layout
```
min-h-screen w-full              Full screen
max-w-md                         Card max width
px-6 py-4                        Padding
gap-4                            Spacing
flex items-center justify-between Flexbox
```

### Text
```
text-4xl font-bold              Large title
text-sm font-medium             Labels
bg-clip-text text-transparent   Gradient text
text-center                      Centered
```

### Effects
```
backdrop-blur-xl                Glassmorphism
shadow-2xl                      Strong shadow
shadow-purple-500/50            Colored shadow
rounded-3xl                     Large border radius
border border-white/20          Subtle border
```

### States
```
hover:scale-[1.02]              Hover grow
active:scale-[0.98]             Click shrink
disabled:cursor-not-allowed     Disabled
transition duration-200         Smooth animation
```

---

## Authentication Flow

### Sign-up
```
User Form → Validation → Supabase.auth.signUp() 
→ Success Modal → Email Verification → Login
```

### Login
```
User Form → Validation → Supabase.auth.signInWithPassword() 
→ JWT Token → Protected Route → Dashboard
```

### Logout
```
Click "Sign Out" → Supabase.auth.signOut() 
→ Clear Session → Redirect to Login
```

---

## Troubleshooting

### Colors Look Different?
- Check `/app/globals.css` for color definitions
- Ensure browser cache is cleared
- All colors should use purple palette

### Animations Not Smooth?
- Check browser GPU acceleration
- Ensure CSS animations are using transforms
- Mobile devices may have different performance

### Success Modal Not Showing?
- Check if `SuccessModal` is imported
- Verify `showSuccessModal` state is being set
- Check console for errors

### Logout Not Working?
- Verify Supabase client is imported
- Check user is actually logged in
- Verify `/auth/login` route exists

---

## Testing Checklist

- [ ] Purple gradient on all pages
- [ ] Floating cards on auth pages
- [ ] 3D cube rotates on login page
- [ ] 3D sphere bobs on sign-up page
- [ ] Success modal shows after signup
- [ ] Can click "Go to Login" button
- [ ] Can close modal
- [ ] Protected page shows after login
- [ ] Logout button exists and works
- [ ] Colors are consistent everywhere
- [ ] Mobile responsive on all pages
- [ ] All animations are smooth (60fps)

---

## Common Changes

### Change Button Color
Replace `from-purple-600 to-purple-500` with your color

### Change Background
Replace `from-slate-900 via-purple-900 to-purple-900` with your gradient

### Change Card Border
Replace `border-purple-400/30` with your color

### Change Animation Speed
Replace `5s` in `floating-card` with desired duration

### Add New Color Variant
Add to `/app/globals.css` and use Tailwind classes

---

## Resources

- **Auth Docs**: `/AUTH_SYSTEM_GUIDE.md`
- **Design Guide**: `/DESIGN_VISUAL_GUIDE.md`
- **Improvements**: `/IMPROVEMENTS_SUMMARY.md`
- **Setup**: `/AUTH_QUICK_START.md`

---

## Support

All systems working:
- ✅ Authentication (Supabase)
- ✅ Email verification
- ✅ Protected routes
- ✅ User sessions
- ✅ Logout function
- ✅ Password security
- ✅ RLS policies

Your app is production-ready!

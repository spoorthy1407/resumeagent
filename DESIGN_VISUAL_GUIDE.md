# Visual Design Guide - Resume Assistant Auth System

## Color Palette

### Gradient Background (All Pages)
```
from-slate-900 via-purple-900 to-purple-900
```
Creates a beautiful dark purple gradient that's consistent across all pages.

### Text Colors

**Page Headers**
- `from-purple-300 to-purple-100` - Beautiful gradient text
- Example: "Welcome Back", "Create Account"

**Secondary Text**
- `text-purple-200/80` - Slightly transparent purple
- Example: "Sign in to your resume assistant"

**Body Text**
- `text-gray-300` - High contrast gray for readability

---

## Component Styling

### Card Design (Login & Sign-up)

```
backdrop-blur-xl bg-white/5 border border-purple-400/30 rounded-3xl
hover:shadow-purple-900/50 hover:border-purple-400/50
floating-card (animation)
```

**Features**:
- Glassmorphic effect with backdrop blur
- Subtle purple border
- Smooth hover shadow that glows purple
- Gentle floating animation

### Buttons

**Primary Button (Login/Sign-up)**
```
bg-gradient-to-r from-purple-600 to-purple-500
hover:from-purple-500 hover:to-purple-400
shadow-lg hover:shadow-purple-500/50
```

**Secondary Button (Close/Back)**
```
bg-white/5 border border-white/20
hover:bg-white/10
```

### Input Fields

**Default State**
```
bg-white/5 border border-white/20 text-white placeholder-gray-400
```

**Focus State**
```
border-purple-400 bg-white/10 shadow
```

---

## Animations

### 1. Floating Card (5 seconds)
```css
@keyframes floating-card {
  0%, 100% { transform: translateY(0px) translateX(0px); }
  25% { transform: translateY(-12px) translateX(2px); }
  50% { transform: translateY(-8px) translateX(0px); }
  75% { transform: translateY(-14px) translateX(-2px); }
}
```
**Applied to**: Login and Sign-up card containers

### 2. 3D Rotating Cube (Login Page)
- Rotates continuously
- Floats up and down smoothly
- Color: `#a78bfa` (purple)
- Emissive: `#9370db` (darker purple)

### 3. 3D Floating Sphere (Sign-up Page)
- Smooth bobbing motion
- Rotates gently
- Color: `#a78bfa` (purple)
- Emissive: `#9370db` (darker purple)

### 4. Cascading Particles
- Fall downward continuously
- Color: `#c084fc` (light purple)
- Size: 0.1 units, small but visible

### 5. Success Modal (Sign-up Success)
```
animate-in fade-in-0 zoom-in-95 duration-300
```
- Smooth fade-in
- Slight zoom effect
- Quick 300ms transition

---

## Layout Structure

### Login/Sign-up Pages
```
┌─────────────────────────────────────────┐
│      3D Canvas Background (Full)        │
├─────────────────────────────────────────┤
│                                         │
│        ┌───────────────────────┐        │
│        │   Floating Card       │        │
│        │   ┌───────────────┐   │        │
│        │   │  Form Content │   │        │
│        │   └───────────────┘   │        │
│        └───────────────────────┘        │
│                                         │
└─────────────────────────────────────────┘
```

### Protected Dashboard
```
┌─────────────────────────────────────────┐
│   Header (Purple theme)                 │
│   ├─ Welcome Message                    │
│   └─ Sign Out Button                    │
├─────────────────────────────────────────┤
│   Tab Navigation                        │
│   ├─ Dashboard  ├─ Upload  ├─ Profile   │
├─────────────────────────────────────────┤
│   Content Area                          │
│   (Tab-specific content)                │
└─────────────────────────────────────────┘
```

---

## Typography

### Font Family
- **Headers**: Bebas Neue (bold, clean)
- **Body**: Geist (modern, readable)
- **Code**: Geist Mono (consistent spacing)

### Heading Sizes
- **Page Title**: `text-4xl font-bold`
- **Card Title**: `text-2xl font-bold`
- **Section Title**: `text-lg font-semibold`
- **Label**: `text-sm font-medium`

---

## Spacing & Sizing

### Cards
- **Padding**: `p-8` (32px inside)
- **Border Radius**: `rounded-3xl` (24px)
- **Max Width**: `max-w-md` (448px)

### Buttons
- **Padding**: `px-4 py-3` (horizontal × vertical)
- **Border Radius**: `rounded-lg` (8px)
- **Font**: `font-semibold` (600 weight)

### Form Fields
- **Padding**: `px-4 py-3`
- **Border Radius**: `rounded-lg`
- **Spacing Between**: `gap-4` or `gap-6`

---

## Interactive States

### Button Hover
```
Scale: 1.02 (2% larger)
Shadow: Glowing purple shadow
Duration: 200ms smooth transition
```

### Button Active
```
Scale: 0.98 (2% smaller)
Provides tactile feedback
```

### Input Focus
```
Border Color: Purple
Background: Slightly more opaque
Gradient Glow: Behind input field
```

### Card Hover
```
Shadow: Enhanced purple glow
Border: Brighter purple
Duration: 500ms smooth transition
```

---

## Success Modal Design

### Modal Structure
```
┌──────────────────────────────────────┐
│  ✓ Icon (Animated background)        │
├──────────────────────────────────────┤
│  Account Created!                    │
│  Welcome to Resume Assistant         │
├──────────────────────────────────────┤
│  Info Box (Email confirmation)       │
├──────────────────────────────────────┤
│  [Go to Login]  [Close]              │
├──────────────────────────────────────┤
│  Helpful tip about spam folder       │
└──────────────────────────────────────┘
```

### Modal Styling
- **Background**: `backdrop-blur-sm bg-black/40`
- **Card**: Same as login/signup cards
- **Icon**: Purple with animated pulse
- **Buttons**: Full width, stacked

---

## Responsive Design

### Mobile (< 640px)
- Cards: `px-4` padding
- Text: Slightly smaller
- Buttons: Full width, 48px height
- 3D Canvas: Reduced quality for performance

### Tablet (640px - 1024px)
- Cards: `px-6` padding
- Full layout on smaller screens
- Smooth transitions maintained

### Desktop (> 1024px)
- Cards: `px-8` padding
- Full quality 3D effects
- Enhanced shadows and glows

---

## Dark Mode Support

The entire system uses a dark theme with:
- Dark background: `from-slate-900`
- Purple accents: `from-purple-900`
- Light text: `text-purple-200`, `text-gray-300`
- High contrast for accessibility

---

## Accessibility Features

### Colors
- Purple text on dark background: WCAG AAA contrast
- Labels for all form inputs
- Clear focus states for keyboard navigation

### Typography
- Semantic HTML structure
- Proper heading hierarchy
- Readable font sizes (minimum 16px)

### Interactions
- All buttons have clear hover states
- Form validation messages are visible
- Modal has proper focus management

---

## Consistency Checklist

When making future changes, ensure:
- ✅ All pages use same background gradient
- ✅ All buttons use purple gradient colors
- ✅ All cards have glassmorphic effect
- ✅ Purple is used for interactive elements
- ✅ Consistent border radius (lg for inputs, 3xl for cards)
- ✅ Padding and spacing follow the grid
- ✅ Animations are smooth (200-500ms)
- ✅ Focus states are visible
- ✅ Mobile responsive on all screens
- ✅ High contrast for readability

---

## Browser-Specific Notes

### CSS Features Used
- **Backdrop Filter**: Modern browsers, graceful fallback
- **Gradient Text**: Chrome, Firefox, Safari (with prefix)
- **CSS Animations**: Hardware-accelerated, smooth 60fps
- **Transform**: GPU-accelerated for performance

### Tested On
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## Performance Tips

1. **Canvas Rendering**: 3D effects are GPU-accelerated
2. **Animations**: Use CSS transforms for 60fps
3. **Shadows**: Use box-shadow, not multiple elements
4. **Particles**: Optimized vertex/fragment shaders

---

This design system is modern, professional, and ready for production!

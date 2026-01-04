# Vercel Deployment Fix for 404 Errors

## Problem
Getting 404 errors when accessing `/auth/login` and `/learn` routes on Vercel deployment.

## Root Cause
The project has a monorepo structure with `frontend/` and `backend/` directories. Vercel needs to be configured to build from the `frontend` directory specifically.

## Solution

### Step 1: Update Vercel Project Settings

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your `happy-hanzy` project
3. Go to **Settings** → **General**
4. Find the **Root Directory** section
5. Click **Edit** and set it to: `frontend`
6. Save the changes

### Step 2: Verify Build & Development Settings

While in Settings, verify these configurations:

**Build & Development Settings:**
- **Framework Preset**: Next.js
- **Build Command**: `npm run build` (or leave auto-detected)
- **Output Directory**: `.next` (or leave auto-detected)
- **Install Command**: `npm install` (or leave auto-detected)

### Step 3: Set Environment Variables

Go to **Settings** → **Environment Variables** and add:

```
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

**Important:** Make sure to add these for all environments (Production, Preview, Development)

### Step 4: Redeploy

After updating the settings:

1. Go to **Deployments** tab
2. Find your latest deployment
3. Click the three dots menu (⋯)
4. Select **Redeploy**
5. Check "Use existing Build Cache" (optional)
6. Click **Redeploy**

### Step 5: Verify Pages Exist

The following pages should now work:
- ✅ `/` - Home page
- ✅ `/auth/login` - Login/signup page
- ✅ `/learn` - Radical library
- ✅ `/dashboard` - User dashboard (requires authentication)

## Alternative: Using Vercel CLI

If you prefer using the CLI:

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to project root
cd c:/Users/mihai/ws/happy-hanzy

# Deploy with proper configuration
vercel --prod --cwd frontend

# Or set up a vercel.json in the frontend directory
```

### Frontend-specific vercel.json

If you want to use `vercel.json`, create it inside the `frontend/` directory:

**frontend/vercel.json:**
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install"
}
```

## Testing Locally

Before deploying, test locally to ensure all routes work:

```bash
cd frontend
npm install
npm run build
npm run start
```

Then test:
- http://localhost:3000/
- http://localhost:3000/auth/login
- http://localhost:3000/learn
- http://localhost:3000/dashboard

## Common Issues

### Issue: Still getting 404s
**Solution:** Clear Vercel's build cache
1. Go to Settings → General
2. Scroll to "Build & Development Settings"
3. Click "Clear Build Cache"
4. Redeploy

### Issue: Environment variables not working
**Solution:** 
- Ensure all variables start with `NEXT_PUBLIC_`
- Redeploy after adding environment variables
- Check browser console for actual values (they should NOT show as undefined)

### Issue: TypeScript errors blocking build
**Solution:** Add to `frontend/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // ⚠️ Dangerously allow production builds to successfully complete even if
    // your project has type errors. Only use temporarily!
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    domains: ['firebasestorage.googleapis.com'],
  },
}

module.exports = nextConfig
```

### Issue: Module not found errors
**Solution:**
- Ensure `package.json` has all required dependencies
- Check that `tailwindcss-animate` is installed: `npm install tailwindcss-animate`
- Run `npm install` in the frontend directory

## Checklist

- [ ] Set Root Directory to `frontend` in Vercel project settings
- [ ] Added all Firebase environment variables
- [ ] Redeployed the project
- [ ] Tested all routes (/, /auth/login, /learn, /dashboard)
- [ ] Verified Firebase authentication works
- [ ] Checked browser console for errors

## Need More Help?

If issues persist:
1. Check Vercel deployment logs for specific errors
2. Verify the build completed successfully
3. Test the same setup locally with `npm run build && npm run start`
4. Check that all required files are committed to git
5. Ensure `.env` files are NOT committed (use environment variables in Vercel dashboard instead)

---

**After fixing:** Your app should work at:
- Production: `https://your-app.vercel.app`
- All routes should be accessible without 404 errors

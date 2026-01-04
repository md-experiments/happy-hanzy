# Firebase API Key Error Fix

## Error Message
```
Firebase: Error (auth/api-key-not-valid.-please-pass-a-valid-api-key.)
```

## Root Cause
Environment variables are not being loaded correctly in your Vercel deployment. This typically happens when:
1. Variables are missing the `NEXT_PUBLIC_` prefix
2. Variables weren't redeployed after being added
3. Variables have typos or incorrect values

## Step-by-Step Fix

### 1. Check Browser Console First

Open your Vercel deployed site, open Developer Tools (F12), go to Console tab, and look for these error messages:
```
Missing Firebase environment variables: [...]
Please check your Vercel environment variables settings
```

This will tell you exactly which variables are missing.

### 2. Verify Environment Variables in Vercel

Go to Vercel Dashboard → Your Project → Settings → Environment Variables

**CRITICAL:** Each variable name MUST start with `NEXT_PUBLIC_`. Check that you have:

```
NEXT_PUBLIC_FIREBASE_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
NEXT_PUBLIC_FIREBASE_APP_ID
```

❌ **WRONG:**
```
FIREBASE_API_KEY=your_key
```

✅ **CORRECT:**
```
NEXT_PUBLIC_FIREBASE_API_KEY=your_key
```

### 3. Get the Correct Values

Go to [Firebase Console](https://console.firebase.google.com/) → Your Project → Project Settings → General

Scroll down to "Your apps" section, find your web app, and you'll see:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

Copy these EXACT values to Vercel.

### 4. Add Variables to Vercel

For each variable in Vercel:

1. **Name:** `NEXT_PUBLIC_FIREBASE_API_KEY`
2. **Value:** Your actual API key (e.g., `AIzaSyXXXXXX...`)
3. **Environment:** Select ALL (Production, Preview, Development)
4. Click "Save"

Repeat for all 6 variables.

### 5. Important: Redeploy After Adding Variables

**Environment variables are NOT automatically applied to existing deployments!**

After adding/updating environment variables:

1. Go to **Deployments** tab
2. Find your latest deployment
3. Click the three dots menu (⋯)
4. Select **"Redeploy"**
5. ✅ **DO NOT** check "Use existing Build Cache"
6. Click **Redeploy**

### 6. Verify Locally First (Optional but Recommended)

Create a `.env.local` file in your `frontend` directory:

```bash
# frontend/.env.local
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyXXXXXX...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789012
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789012:web:abcdef123456
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then test locally:
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000/auth/login` and try to login. If it works locally but not on Vercel, the issue is definitely with Vercel's environment variables.

## Common Mistakes

### ❌ Mistake 1: Missing NEXT_PUBLIC_ Prefix
```
FIREBASE_API_KEY=value  # Won't work!
```

### ✅ Fix:
```
NEXT_PUBLIC_FIREBASE_API_KEY=value
```

---

### ❌ Mistake 2: Not Redeploying After Adding Variables
Adding variables doesn't automatically update existing deployments.

### ✅ Fix:
Always redeploy without cache after adding environment variables.

---

### ❌ Mistake 3: Quotes Around Values
```
NEXT_PUBLIC_FIREBASE_API_KEY="AIzaSyXXX"  # Extra quotes!
```

### ✅ Fix:
```
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyXXX  # No quotes in Vercel UI
```

---

### ❌ Mistake 4: Only Adding to Production
If you only add variables to "Production" environment, preview deployments won't work.

### ✅ Fix:
Select **All Environments** when adding each variable.

---

### ❌ Mistake 5: Typos in Variable Names
```
NEXT_PUBLIC_FIREBASE_APIKEY=value  # Missing underscore!
```

### ✅ Fix:
```
NEXT_PUBLIC_FIREBASE_API_KEY=value
```

## Quick Checklist

Use this checklist to verify everything:

- [ ] All 6 Firebase variables are in Vercel settings
- [ ] Each variable name starts with `NEXT_PUBLIC_`
- [ ] Variable names match EXACTLY (check underscores, spelling)
- [ ] Values are copied correctly from Firebase Console
- [ ] Variables are added to ALL environments (Production, Preview, Development)
- [ ] No extra quotes around values
- [ ] Redeployed WITHOUT using existing build cache
- [ ] Waited for deployment to complete (check Deployments tab)
- [ ] Tested the login page after redeployment

## Still Not Working?

### Debug in Browser Console

1. Visit your deployed site
2. Open DevTools (F12) → Console
3. Type: `console.log(process.env.NEXT_PUBLIC_FIREBASE_API_KEY)`
4. If it shows `undefined`, variables aren't loaded
5. Check the console for error messages about missing variables

### Check Vercel Build Logs

1. Go to Deployments → Click on your latest deployment
2. Look for the "Building" section logs
3. Search for any errors related to environment variables
4. Firebase initialization errors will show here

### Nuclear Option: Delete and Re-add Project

If nothing works:

1. Note down all your settings
2. Delete the project from Vercel
3. Re-import from GitHub
4. Set Root Directory to `frontend`
5. Add ALL environment variables
6. Deploy

## After It Works

Once your login works:

1. Test all three login methods:
   - Email/Password
   - Google Sign-in
   - Guest/Anonymous

2. Verify the dashboard loads after login

3. Check that logout works

4. Test on different browsers/devices

## Need Your Firebase Config?

Run this in your local terminal:

```bash
# From the project root
cat frontend/.env.local
```

Or check Firebase Console → Project Settings → Your apps → Config

---

**Most Common Solution:** Missing `NEXT_PUBLIC_` prefix + not redeploying after adding variables. Fix both and it should work!

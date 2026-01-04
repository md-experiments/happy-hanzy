# Happy Hanzy - Complete Setup Guide

This guide will walk you through setting up the Happy Hanzy Chinese learning application from scratch.

## Prerequisites

- Node.js 18+ installed
- Python 3.9+ installed
- A Firebase account (free tier works fine)
- Git installed

## Step 1: Firebase Setup

### 1.1 Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" and follow the wizard
3. Give your project a name (e.g., "happy-hanzy")

### 1.2 Enable Firestore Database

1. In your Firebase project, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (you can update rules later)
4. Select a region close to your users

### 1.3 Enable Authentication

1. Go to "Authentication" in Firebase Console
2. Click "Get started"
3. Enable the following sign-in methods:
   - Email/Password
   - Google
   - Anonymous

### 1.4 Get Firebase Configuration

#### For Frontend (Web App):
1. Go to Project Settings (gear icon) → General
2. Scroll to "Your apps" and click the web icon (</>)
3. Register your app with a nickname
4. Copy the `firebaseConfig` object values

#### For Backend (Admin SDK):
1. Go to Project Settings → Service Accounts
2. Click "Generate new private key"
3. Save the JSON file securely (you'll need values from it)

## Step 2: Frontend Setup

### 2.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 2.2 Install Dependencies

```bash
npm install
```

If you encounter issues, try:
```bash
npm install --legacy-peer-deps
```

### 2.3 Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Firebase credentials:

```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2.4 Run Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Step 3: Backend Setup

### 3.1 Navigate to Backend Directory

```bash
cd ../backend
```

### 3.2 Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` with values from your Firebase Admin SDK JSON file:

```env
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your_project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CERT_URL=your_client_cert_url

API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### 3.5 Seed the Database

Run the seed script to populate Firestore with sample data:

```bash
python seed_data.py
```

### 3.6 Run Development Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Step 4: Testing the Application

1. Open `http://localhost:3000` in your browser
2. You should see the Happy Hanzy landing page
3. Click "Get Started" to create an account or sign in
4. Try the different features:
   - Browse radicals
   - Learn characters
   - Take quizzes
   - View your progress

## Step 5: Deployment (Optional)

### Frontend Deployment (Vercel)

1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Click "Import Project"
4. Select your repository
5. Set the root directory to `frontend`
6. Add your environment variables in Vercel's dashboard
7. Deploy!

### Backend Deployment (Railway.app)

1. Go to [Railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Set the root directory to `backend`
5. Add all environment variables
6. Add a start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Deploy!

### Alternative: Render.com

1. Go to [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your repository
4. Set:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

## Firestore Security Rules

For production, update your Firestore rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Radicals and characters are readable by all
    match /radicals/{radical} {
      allow read: if true;
      allow write: if false;
    }
    
    match /characters/{character} {
      allow read: if true;
      allow write: if false;
    }
    
    // User progress is private
    match /user_progress/{progress} {
      allow read, write: if request.auth != null 
        && request.auth.uid == resource.data.user_id;
    }
    
    // Quiz attempts are private
    match /quiz_attempts/{attempt} {
      allow read, write: if request.auth != null 
        && request.auth.uid == resource.data.user_id;
    }
  }
}
```

## Troubleshooting

### "Cannot find module" errors in frontend
- Run `npm install` again
- Try `npm install --legacy-peer-deps`
- Delete `node_modules` and `package-lock.json`, then reinstall

### Python import errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Firebase connection errors
- Double-check all environment variables
- Ensure Firebase project is properly configured
- Check that Firestore is enabled

### CORS errors
- Ensure backend `CORS_ORIGINS` includes your frontend URL
- Check that both servers are running

## Support

For issues and questions:
- Check the [Firebase documentation](https://firebase.google.com/docs)
- Review the [Next.js documentation](https://nextjs.org/docs)
- See [FastAPI documentation](https://fastapi.tiangolo.com/)

## Next Steps

1. Add more radicals and characters to your database
2. Customize the UI/styling to your preference
3. Add more quiz types
4. Implement additional features (writing practice, etc.)
5. Set up monitoring and analytics

Happy learning! 学习快乐！

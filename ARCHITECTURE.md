# Happy Hanzy - Architecture Documentation

## Overview

Happy Hanzy is a Chinese character learning application with a **serverless, Firebase-first architecture**. The frontend communicates directly with Firebase Firestore for all user data operations, while the backend serves purely as a content generation and management tool.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Users                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Next.js Frontend (Vercel)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - Pages (Learn, Dashboard, Auth)                    │   │
│  │  - React Components                                   │   │
│  │  - Firestore Service (Direct DB Access)              │   │
│  │  - Firebase Auth Integration                          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Firebase Services                            │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │  Authentication  │  │    Firestore     │                 │
│  │                  │  │   (Database)     │                 │
│  │  - Email/Pass    │  │                  │                 │
│  │  - Google OAuth  │  │  - Radicals      │                 │
│  │  - Anonymous     │  │  - Characters    │                 │
│  │                  │  │  - User Progress │                 │
│  │                  │  │  - Quiz Attempts │                 │
│  └──────────────────┘  └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│       Backend (FastAPI) - Content Management Only            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - Seed Script (populate Firestore)                  │   │
│  │  - Content Generation Tools                           │   │
│  │  - Data Import/Export Utilities                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  Note: NOT deployed - runs locally for admin tasks          │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Firebase-First Approach

**Why?**
- **Simplicity**: No need to manage a separate backend server for user operations
- **Cost**: Firebase free tier is generous (50K reads, 20K writes/day)
- **Real-time**: Built-in real-time listeners for live updates
- **Scalability**: Automatic scaling with no DevOps required
- **Security**: Row-level security via Firestore security rules

**Implementation:**
- Frontend uses `firestore-service.ts` to interact directly with Firestore
- All user data (progress, quiz attempts, stats) stored in Firestore
- Firebase Auth handles all authentication flows

### 2. Backend as Content Tool

**Purpose:**
The FastAPI backend is **not a runtime dependency**. It serves only as a development/admin tool for:

1. **Data Seeding**: Populate Firestore with radicals and characters
2. **Content Generation**: Generate additional learning content
3. **Data Management**: Bulk operations, imports, exports
4. **Analytics**: Process data for insights (optional)

**Key Point**: Users never interact with the backend directly. It doesn't need to be deployed.

### 3. Deployment Strategy

#### Frontend (Next.js → Vercel)
- **Auto-deploy** from Git on every push
- **Environment Variables**: Firebase credentials
- **Free Tier**: Generous limits for hobby projects
- **Global CDN**: Fast worldwide access

#### Backend (Optional)
- **Not deployed** by default
- Run locally when needed for content management
- Could be deployed to Railway/Render if admin panel needed

## Data Flow Examples

### User Learns a Radical

```
1. User visits /learn
   └─→ Frontend calls getRadicals() from firestore-service.ts
       └─→ Direct query to Firestore: collection('radicals')
           └─→ Returns radical data to frontend
               └─→ Displayed to user

No backend involved!
```

### User Records Progress

```
1. User completes a quiz question
   └─→ Frontend calls recordReview(userId, itemId, correct)
       └─→ Direct write to Firestore: collection('user_progress')
           └─→ Updates or creates progress document
               └─→ Real-time sync across devices

No backend involved!
```

### Admin Adds New Content

```
1. Admin runs: python backend/seed_data.py
   └─→ Backend script connects to Firestore (Firebase Admin SDK)
       └─→ Writes new radicals/characters to Firestore
           └─→ Content immediately available to all users

Backend runs locally, not deployed
```

## Firestore Collections

### `radicals`
```javascript
{
  id: "auto-generated",
  character: "人",
  meaning: "person",
  stroke_count: 2,
  frequency: 95,
  examples: ["他", "你", "們"]
}
```

### `characters`
```javascript
{
  id: "auto-generated",
  hanzi: "好",
  pinyin: "hǎo",
  meaning: "good, well",
  hsk_level: 1,
  frequency: 95,
  radicals: ["radical_id_1", "radical_id_2"]
}
```

### `user_progress`
```javascript
{
  id: "auto-generated",
  user_id: "firebase_uid",
  item_id: "radical_or_character_id",
  item_type: "radical" | "character",
  mastery_level: "new" | "learning" | "familiar" | "mastered",
  last_reviewed: timestamp,
  next_review: timestamp,
  correct_count: 5,
  incorrect_count: 2,
  ease_factor: 2.5,
  interval: 7  // days
}
```

### `quiz_attempts`
```javascript
{
  id: "auto-generated",
  user_id: "firebase_uid",
  question_id: "generated_question_id",
  question_type: "radical_recognition" | "meaning_match" | "composition",
  answer: "user_answer",
  correct: true,
  timestamp: timestamp
}
```

## Security Rules

Firestore security rules ensure data privacy:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public read for learning content
    match /radicals/{radical} {
      allow read: if true;
      allow write: if false;  // Only backend can write
    }
    
    match /characters/{character} {
      allow read: if true;
      allow write: if false;
    }
    
    // Private user data
    match /user_progress/{progress} {
      allow read, write: if request.auth != null 
        && request.auth.uid == resource.data.user_id;
    }
    
    match /quiz_attempts/{attempt} {
      allow read, write: if request.auth != null 
        && request.auth.uid == resource.data.user_id;
    }
  }
}
```

## Frontend Services

### `firestore-service.ts`
Central service for all Firestore operations:
- `getRadicals()` - Fetch radicals
- `getRadicalById(id)` - Get specific radical
- `getCharacters()` - Fetch characters
- `getUserProgress(userId)` - Get user's progress
- `recordReview()` - Save quiz results
- `getProgressStats()` - Calculate statistics
- `submitQuizAnswer()` - Record quiz attempts
- `getMistakes()` - Get frequently missed items

### `firebase.ts`
Firebase initialization and configuration:
- Initializes Firebase app
- Exports auth and db instances
- Handles configuration from environment variables

### `AuthContext.tsx`
React Context for authentication:
- Manages user auth state
- Provides login/logout functions
- Handles Google OAuth and anonymous auth

## Benefits of This Architecture

### ✅ Advantages

1. **Simpler Deployment**: Only frontend needs to be deployed
2. **Lower Costs**: No backend server costs (Firebase free tier)
3. **Better Performance**: Direct client-to-database reduces latency
4. **Real-time Updates**: Built-in sync across devices
5. **Easier Maintenance**: Fewer moving parts
6. **Better Security**: Firebase handles authentication & authorization
7. **Scalability**: Automatic with Firebase

### ⚠️ Considerations

1. **Firebase Limits**: 
   - Free tier: 50K reads, 20K writes/day
   - Adequate for 100s of users
   
2. **Complex Queries**:
   - Some queries may be limited by Firestore capabilities
   - Use composite indexes for complex filters

3. **Cost at Scale**:
   - Monitor usage as app grows
   - May need Spark/Blaze plan for larger user base

## Migration from API-based Architecture

If upgrading from the old API-based design:

1. ✅ Frontend already uses `firestore-service.ts` (done)
2. ✅ Remove `lib/api.ts` dependencies
3. ✅ Update all pages to use Firestore service
4. ✅ Backend only needed for seeding
5. ✅ Remove backend from deployment pipeline

## Development Workflow

### For Content Updates

```bash
# 1. Update seed_data.py with new content
cd backend
python seed_data.py

# 2. Content is now live for all users
```

### For Frontend Changes

```bash
# 1. Make changes
cd frontend
npm run dev

# 2. Test locally
# 3. Push to Git
git push

# 4. Vercel auto-deploys
```

## Monitoring & Analytics

Track usage via:
- **Firebase Console**: Real-time database usage, auth stats
- **Vercel Analytics**: Page views, performance
- **Custom Events**: Add tracking to firestore-service.ts

## Future Enhancements

Possible additions while maintaining architecture:
- Cloud Functions for complex operations (e.g., daily email reminders)
- Firebase Cloud Messaging for push notifications
- Firebase Storage for user-generated content (if needed)
- Admin panel (Next.js admin routes with authentication)

## Conclusion

This architecture provides a modern, scalable, cost-effective solution for Happy Hanzy. The separation of content management (backend) from user operations (Firebase direct) simplifies deployment while maintaining flexibility for future growth.

# Happy Hanzy - Chinese Character Learning App

A comprehensive application for learning Chinese Hanzi characters through radicals, interactive diagrams, flashcards, and quizzes.

## Features

- **Radical Library**: Browse and learn 214 Chinese radicals with meanings
- **Character Builder**: Interactive diagrams showing how characters are composed from radicals
- **Flashcards**: Spaced repetition system for effective memorization
- **Quizzes**: Multiple quiz types (radical recognition, composition, meanings)
- **Progress Tracking**: Dashboard with statistics, mistake logs, and review history

## Architecture

**Happy Hanzy uses a serverless, Firebase-first architecture:**

### Frontend (Deployed)
- **Framework**: Next.js 14+ (App Router)
- **UI**: shadcn/ui + Tailwind CSS
- **Hosting**: Vercel (auto-deploy from Git)
- **Database Access**: Direct Firestore queries via `firestore-service.ts`
- **Auth**: Firebase Authentication (Email, Google, Anonymous)

### Backend (Local Only - Not Deployed)
- **Purpose**: Content generation and data seeding ONLY
- **Framework**: FastAPI (Python)
- **Usage**: Run locally to populate Firestore with learning content
- **Note**: Users never interact with backend directly

**Key Benefits:**
- ✅ Simpler deployment (frontend only)
- ✅ Lower costs (no backend server)
- ✅ Better performance (direct Firebase access)
- ✅ Real-time sync across devices
- ✅ Automatic scalability

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed documentation.

## Project Structure

```
hanzi-app/
├── frontend/          # Next.js application
│   ├── app/          # App router pages
│   ├── components/   # React components
│   └── lib/          # Utilities and configs
└── backend/          # FastAPI application
    ├── main.py       # Entry point
    ├── models/       # Data models
    ├── routes/       # API routes
    └── services/     # Business logic
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- Firebase account

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variables

See `.env.example` files in both frontend and backend directories.

## License

MIT

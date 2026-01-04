# Happy Hanzy - Chinese Character Learning App

A comprehensive application for learning Chinese Hanzi characters through radicals, interactive diagrams, flashcards, and quizzes.

## Features

- **Radical Library**: Browse and learn 214 Chinese radicals with meanings
- **Character Builder**: Interactive diagrams showing how characters are composed from radicals
- **Flashcards**: Spaced repetition system for effective memorization
- **Quizzes**: Multiple quiz types (radical recognition, composition, meanings)
- **Progress Tracking**: Dashboard with statistics, mistake logs, and review history

## Architecture

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **UI**: shadcn/ui + Tailwind CSS
- **Hosting**: Vercel
- **State**: React Context + SWR

### Backend
- **API**: FastAPI (Python)
- **Hosting**: Railway.app / Render.com
- **Database**: Firebase Firestore
- **Auth**: Firebase Authentication

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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import radicals, characters, progress, quiz
from services.firebase_service import initialize_firebase

# Load environment variables
load_dotenv()

# Initialize Firebase
initialize_firebase()

app = FastAPI(
    title="Happy Hanzy API",
    description="API for Chinese Hanzi learning application",
    version="1.0.0"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(radicals.router, prefix="/api/radicals", tags=["radicals"])
app.include_router(characters.router, prefix="/api/characters", tags=["characters"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Happy Hanzy API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

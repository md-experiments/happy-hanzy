from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ItemType(str, Enum):
    RADICAL = "radical"
    CHARACTER = "character"

class MasteryLevel(str, Enum):
    NEW = "new"
    LEARNING = "learning"
    FAMILIAR = "familiar"
    MASTERED = "mastered"

class Radical(BaseModel):
    id: str
    character: str
    meaning: str
    stroke_count: int
    frequency: int
    examples: Optional[List[str]] = []

class Character(BaseModel):
    id: str
    hanzi: str
    pinyin: str
    meaning: str
    hsk_level: int
    frequency: int
    radicals: List[str] = []

class CharacterRadical(BaseModel):
    character_id: str
    radical_id: str
    position: str  # left, right, top, bottom, enclosure, etc.

class UserProgress(BaseModel):
    user_id: str
    item_id: str
    item_type: ItemType
    mastery_level: MasteryLevel = MasteryLevel.NEW
    last_reviewed: datetime
    next_review: datetime
    correct_count: int = 0
    incorrect_count: int = 0
    ease_factor: float = 2.5
    interval: int = 0  # days

class QuizAttempt(BaseModel):
    user_id: str
    question_id: str
    question_type: str  # radical_recognition, character_composition, meaning_match, etc.
    answer: str
    correct: bool
    timestamp: datetime

class QuizQuestion(BaseModel):
    id: str
    question_type: str
    question_text: str
    correct_answer: str
    options: List[str]
    item_id: str
    item_type: ItemType

class ProgressStats(BaseModel):
    total_learned: int
    radicals_mastered: int
    characters_mastered: int
    accuracy_rate: float
    streak_days: int
    total_reviews: int

class MistakeLog(BaseModel):
    user_id: str
    item_id: str
    item_type: ItemType
    timestamp: datetime
    mistake_count: int

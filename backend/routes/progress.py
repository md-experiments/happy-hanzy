from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.schemas import UserProgress, ProgressStats, MasteryLevel, ItemType
from services.firebase_service import get_db
from services.spaced_repetition import SpacedRepetitionService

router = APIRouter()
srs = SpacedRepetitionService()

@router.get("/{user_id}", response_model=List[UserProgress])
async def get_user_progress(user_id: str):
    """Get all progress for a user"""
    try:
        db = get_db()
        docs = db.collection('user_progress').where('user_id', '==', user_id).stream()
        
        progress_list = []
        for doc in docs:
            data = doc.to_dict()
            # Convert timestamps
            if 'last_reviewed' in data and isinstance(data['last_reviewed'], str):
                data['last_reviewed'] = datetime.fromisoformat(data['last_reviewed'])
            if 'next_review' in data and isinstance(data['next_review'], str):
                data['next_review'] = datetime.fromisoformat(data['next_review'])
            progress_list.append(UserProgress(**data))
        
        return progress_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/due")
async def get_due_items(user_id: str):
    """Get items due for review"""
    try:
        db = get_db()
        docs = db.collection('user_progress').where('user_id', '==', user_id).stream()
        
        progress_list = []
        for doc in docs:
            data = doc.to_dict()
            if 'last_reviewed' in data and isinstance(data['last_reviewed'], str):
                data['last_reviewed'] = datetime.fromisoformat(data['last_reviewed'])
            if 'next_review' in data and isinstance(data['next_review'], str):
                data['next_review'] = datetime.fromisoformat(data['next_review'])
            progress_list.append(UserProgress(**data))
        
        due_items = srs.get_items_due_for_review(progress_list)
        return due_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}/review")
async def record_review(user_id: str, item_id: str, item_type: ItemType, correct: bool):
    """Record a review attempt and update progress"""
    try:
        db = get_db()
        
        # Find or create progress record
        progress_ref = db.collection('user_progress')
        query = progress_ref.where('user_id', '==', user_id).where('item_id', '==', item_id)
        docs = list(query.stream())
        
        if docs:
            # Update existing progress
            doc = docs[0]
            data = doc.to_dict()
            if 'last_reviewed' in data and isinstance(data['last_reviewed'], str):
                data['last_reviewed'] = datetime.fromisoformat(data['last_reviewed'])
            if 'next_review' in data and isinstance(data['next_review'], str):
                data['next_review'] = datetime.fromisoformat(data['next_review'])
            progress = UserProgress(**data)
            updated_progress = srs.calculate_next_review(progress, correct)
            
            # Save to Firestore
            progress_dict = updated_progress.dict()
            progress_dict['last_reviewed'] = updated_progress.last_reviewed.isoformat()
            progress_dict['next_review'] = updated_progress.next_review.isoformat()
            progress_dict['mastery_level'] = updated_progress.mastery_level.value
            progress_dict['item_type'] = updated_progress.item_type.value
            
            doc.reference.update(progress_dict)
        else:
            # Create new progress record
            new_progress = UserProgress(
                user_id=user_id,
                item_id=item_id,
                item_type=item_type,
                mastery_level=MasteryLevel.NEW,
                last_reviewed=datetime.now(),
                next_review=datetime.now(),
                correct_count=0,
                incorrect_count=0,
                ease_factor=2.5,
                interval=0
            )
            updated_progress = srs.calculate_next_review(new_progress, correct)
            
            progress_dict = updated_progress.dict()
            progress_dict['last_reviewed'] = updated_progress.last_reviewed.isoformat()
            progress_dict['next_review'] = updated_progress.next_review.isoformat()
            progress_dict['mastery_level'] = updated_progress.mastery_level.value
            progress_dict['item_type'] = updated_progress.item_type.value
            
            progress_ref.add(progress_dict)
        
        return {"status": "success", "progress": updated_progress}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/stats", response_model=ProgressStats)
async def get_progress_stats(user_id: str):
    """Get progress statistics for a user"""
    try:
        db = get_db()
        docs = db.collection('user_progress').where('user_id', '==', user_id).stream()
        
        total_learned = 0
        radicals_mastered = 0
        characters_mastered = 0
        total_correct = 0
        total_attempts = 0
        
        for doc in docs:
            data = doc.to_dict()
            total_learned += 1
            
            if data.get('mastery_level') == MasteryLevel.MASTERED.value:
                if data.get('item_type') == ItemType.RADICAL.value:
                    radicals_mastered += 1
                elif data.get('item_type') == ItemType.CHARACTER.value:
                    characters_mastered += 1
            
            total_correct += data.get('correct_count', 0)
            total_attempts += data.get('correct_count', 0) + data.get('incorrect_count', 0)
        
        accuracy_rate = (total_correct / total_attempts * 100) if total_attempts > 0 else 0.0
        
        # Calculate streak (simplified - would need more complex logic for real streak)
        streak_days = 0
        
        return ProgressStats(
            total_learned=total_learned,
            radicals_mastered=radicals_mastered,
            characters_mastered=characters_mastered,
            accuracy_rate=accuracy_rate,
            streak_days=streak_days,
            total_reviews=total_attempts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

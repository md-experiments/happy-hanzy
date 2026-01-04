from fastapi import APIRouter, HTTPException
from typing import List
import random
from datetime import datetime
from models.schemas import QuizQuestion, QuizAttempt, ItemType
from services.firebase_service import get_db

router = APIRouter()

@router.get("/generate/{user_id}")
async def generate_quiz(user_id: str, count: int = 10, quiz_type: str = "mixed"):
    """
    Generate a quiz with questions based on user's progress
    
    quiz_type: radical_recognition, character_composition, meaning_match, or mixed
    """
    try:
        db = get_db()
        
        # Get user's learned items
        progress_docs = db.collection('user_progress').where('user_id', '==', user_id).stream()
        learned_items = []
        
        for doc in progress_docs:
            data = doc.to_dict()
            learned_items.append({
                'item_id': data['item_id'],
                'item_type': data['item_type']
            })
        
        if len(learned_items) < 4:
            raise HTTPException(status_code=400, detail="Not enough learned items to generate quiz")
        
        # Generate questions
        questions = []
        quiz_types = ['radical_recognition', 'meaning_match', 'character_composition'] if quiz_type == "mixed" else [quiz_type]
        
        for _ in range(count):
            selected_type = random.choice(quiz_types)
            item = random.choice(learned_items)
            
            if item['item_type'] == 'radical':
                question = await _generate_radical_question(db, item['item_id'], selected_type)
            else:
                question = await _generate_character_question(db, item['item_id'], selected_type)
            
            if question:
                questions.append(question)
        
        return questions
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def _generate_radical_question(db, radical_id: str, question_type: str):
    """Generate a question for a radical"""
    doc = db.collection('radicals').document(radical_id).get()
    if not doc.exists:
        return None
    
    radical_data = doc.to_dict()
    
    # Get other radicals for wrong options
    all_radicals = list(db.collection('radicals').limit(20).stream())
    wrong_options = [r.to_dict() for r in all_radicals if r.id != radical_id][:3]
    
    if question_type == "radical_recognition":
        options = [radical_data['meaning']] + [r['meaning'] for r in wrong_options]
        random.shuffle(options)
        
        return QuizQuestion(
            id=f"q_{radical_id}_{datetime.now().timestamp()}",
            question_type="radical_recognition",
            question_text=f"What does the radical '{radical_data['character']}' mean?",
            correct_answer=radical_data['meaning'],
            options=options,
            item_id=radical_id,
            item_type=ItemType.RADICAL
        )
    else:  # meaning_match
        options = [radical_data['character']] + [r['character'] for r in wrong_options]
        random.shuffle(options)
        
        return QuizQuestion(
            id=f"q_{radical_id}_{datetime.now().timestamp()}",
            question_type="meaning_match",
            question_text=f"Which radical means '{radical_data['meaning']}'?",
            correct_answer=radical_data['character'],
            options=options,
            item_id=radical_id,
            item_type=ItemType.RADICAL
        )

async def _generate_character_question(db, character_id: str, question_type: str):
    """Generate a question for a character"""
    doc = db.collection('characters').document(character_id).get()
    if not doc.exists:
        return None
    
    char_data = doc.to_dict()
    
    # Get other characters for wrong options
    all_chars = list(db.collection('characters').limit(20).stream())
    wrong_options = [c.to_dict() for c in all_chars if c.id != character_id][:3]
    
    if question_type == "meaning_match":
        options = [char_data['meaning']] + [c['meaning'] for c in wrong_options]
        random.shuffle(options)
        
        return QuizQuestion(
            id=f"q_{character_id}_{datetime.now().timestamp()}",
            question_type="meaning_match",
            question_text=f"What does '{char_data['hanzi']}' mean?",
            correct_answer=char_data['meaning'],
            options=options,
            item_id=character_id,
            item_type=ItemType.CHARACTER
        )
    else:  # character_composition
        # Get radicals for this character
        radical_ids = char_data.get('radicals', [])
        if not radical_ids:
            return None
        
        radicals = []
        for r_id in radical_ids:
            r_doc = db.collection('radicals').document(r_id).get()
            if r_doc.exists:
                radicals.append(r_doc.to_dict()['character'])
        
        # Get wrong radical options
        all_radicals = list(db.collection('radicals').limit(10).stream())
        wrong_radical_chars = [r.to_dict()['character'] for r in all_radicals if r.id not in radical_ids][:3]
        
        options = [', '.join(radicals)] + [', '.join(random.sample(wrong_radical_chars, min(len(radicals), len(wrong_radical_chars)))) for _ in range(3)]
        random.shuffle(options)
        
        return QuizQuestion(
            id=f"q_{character_id}_{datetime.now().timestamp()}",
            question_type="character_composition",
            question_text=f"Which radicals compose '{char_data['hanzi']}'?",
            correct_answer=', '.join(radicals),
            options=options,
            item_id=character_id,
            item_type=ItemType.CHARACTER
        )

@router.post("/submit")
async def submit_quiz_answer(attempt: QuizAttempt):
    """Submit a quiz answer and record it"""
    try:
        db = get_db()
        
        # Save attempt
        attempt_dict = attempt.dict()
        attempt_dict['timestamp'] = attempt.timestamp.isoformat()
        db.collection('quiz_attempts').add(attempt_dict)
        
        return {"status": "success", "correct": attempt.correct}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/history")
async def get_quiz_history(user_id: str, limit: int = 50):
    """Get quiz attempt history for a user"""
    try:
        db = get_db()
        docs = db.collection('quiz_attempts').where('user_id', '==', user_id).order_by('timestamp', direction='DESCENDING').limit(limit).stream()
        
        attempts = []
        for doc in docs:
            data = doc.to_dict()
            if 'timestamp' in data and isinstance(data['timestamp'], str):
                data['timestamp'] = datetime.fromisoformat(data['timestamp'])
            attempts.append(data)
        
        return attempts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/mistakes")
async def get_mistakes(user_id: str):
    """Get items the user frequently gets wrong"""
    try:
        db = get_db()
        docs = db.collection('quiz_attempts').where('user_id', '==', user_id).where('correct', '==', False).stream()
        
        mistakes = {}
        for doc in docs:
            data = doc.to_dict()
            question_id = data.get('question_id')
            if question_id in mistakes:
                mistakes[question_id]['count'] += 1
            else:
                mistakes[question_id] = {
                    'question_id': question_id,
                    'question_type': data.get('question_type'),
                    'count': 1
                }
        
        # Sort by count
        sorted_mistakes = sorted(mistakes.values(), key=lambda x: x['count'], reverse=True)
        
        return sorted_mistakes[:20]  # Return top 20 mistakes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

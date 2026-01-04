from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import Character
from services.firebase_service import get_db

router = APIRouter()

@router.get("/", response_model=List[Character])
async def get_characters(limit: int = 50, offset: int = 0, hsk_level: int = None):
    """Get all characters with pagination and optional HSK level filter"""
    try:
        db = get_db()
        characters_ref = db.collection('characters')
        
        # Query with optional HSK filter
        query = characters_ref
        if hsk_level:
            query = query.where('hsk_level', '==', hsk_level)
        
        query = query.order_by('frequency', direction='DESCENDING').limit(limit).offset(offset)
        docs = query.stream()
        
        characters = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            characters.append(Character(**data))
        
        return characters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{character_id}", response_model=Character)
async def get_character(character_id: str):
    """Get a specific character by ID"""
    try:
        db = get_db()
        doc = db.collection('characters').document(character_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Character not found")
        
        data = doc.to_dict()
        data['id'] = doc.id
        return Character(**data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{character_id}/radicals")
async def get_character_radicals(character_id: str):
    """Get all radicals that compose a character"""
    try:
        db = get_db()
        
        # Get character
        char_doc = db.collection('characters').document(character_id).get()
        if not char_doc.exists:
            raise HTTPException(status_code=404, detail="Character not found")
        
        char_data = char_doc.to_dict()
        radical_ids = char_data.get('radicals', [])
        
        # Get radical details
        radicals = []
        for radical_id in radical_ids:
            radical_doc = db.collection('radicals').document(radical_id).get()
            if radical_doc.exists:
                data = radical_doc.to_dict()
                data['id'] = radical_doc.id
                radicals.append(data)
        
        return radicals
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{query}")
async def search_characters(query: str):
    """Search characters by meaning, pinyin, or hanzi"""
    try:
        db = get_db()
        characters_ref = db.collection('characters')
        
        docs = characters_ref.stream()
        
        results = []
        query_lower = query.lower()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Simple text search
            if (query_lower in data.get('meaning', '').lower() or 
                query_lower in data.get('pinyin', '').lower() or 
                query in data.get('hanzi', '')):
                results.append(Character(**data))
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

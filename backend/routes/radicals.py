from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import Radical
from services.firebase_service import get_db

router = APIRouter()

@router.get("/", response_model=List[Radical])
async def get_radicals(limit: int = 50, offset: int = 0):
    """Get all radicals with pagination"""
    try:
        db = get_db()
        radicals_ref = db.collection('radicals')
        
        # Query with pagination
        query = radicals_ref.order_by('frequency', direction='DESCENDING').limit(limit).offset(offset)
        docs = query.stream()
        
        radicals = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            radicals.append(Radical(**data))
        
        return radicals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{radical_id}", response_model=Radical)
async def get_radical(radical_id: str):
    """Get a specific radical by ID"""
    try:
        db = get_db()
        doc = db.collection('radicals').document(radical_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Radical not found")
        
        data = doc.to_dict()
        data['id'] = doc.id
        return Radical(**data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{query}")
async def search_radicals(query: str):
    """Search radicals by meaning or character"""
    try:
        db = get_db()
        radicals_ref = db.collection('radicals')
        
        # Search by meaning or character (Firestore limitations apply)
        docs = radicals_ref.stream()
        
        results = []
        query_lower = query.lower()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Simple text search (in production, use a proper search service)
            if (query_lower in data.get('meaning', '').lower() or 
                query in data.get('character', '')):
                results.append(Radical(**data))
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

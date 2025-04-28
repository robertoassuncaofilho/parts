from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from typing import List
from uuid import UUID, uuid4

from app.database import get_db
from app.models.part import Part as PartModel
from app.schemas.part import PartCreate, PartUpdate, Part, WordCount
from app.cache import cache

router = APIRouter()

@router.post("/", response_model=Part)
def create_part(part: PartCreate, db: Session = Depends(get_db)):
    """
    Create a new part.
    """
    db_part = PartModel(
        id=uuid4(),
        name=part.name,
        sku=part.sku,
        description=part.description,
        weight_ounces=part.weight_ounces,
        is_active=part.is_active
    )
    db.add(db_part)
    cache.clear()  # Clear cache before commit
    db.commit()
    db.refresh(db_part)
    return db_part

@router.get("/", response_model=List[Part])
def read_parts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all parts with pagination.
    """
    stmt = select(PartModel).offset(skip).limit(limit)
    parts = db.scalars(stmt).all()
    return parts

@router.get("/{part_id}", response_model=Part)
def read_part(part_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific part by ID.
    """
    stmt = select(PartModel).where(PartModel.id == part_id)
    part = db.scalar(stmt)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

@router.put("/{part_id}", response_model=Part)
def update_part(part_id: UUID, part: PartUpdate, db: Session = Depends(get_db)):
    """
    Update a specific part.
    """
    stmt = select(PartModel).where(PartModel.id == part_id)
    db_part = db.scalar(stmt)
    if db_part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    
    update_data = part.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_part, key, value)
    
    cache.clear()
    db.commit()
    db.refresh(db_part)
    return db_part

@router.delete("/{part_id}")
def delete_part(part_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a specific part.
    """
    stmt = select(PartModel).where(PartModel.id == part_id)
    part = db.scalar(stmt)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    
    db.delete(part)
    cache.clear()
    db.commit()
    return {"message": "Part deleted successfully"}

@router.get("/common-words/", response_model=List[WordCount])
def get_common_words(db: Session = Depends(get_db)):
    """
    Get the 5 most common words in part descriptions.
    """
    # Try to get from cache first
    cached_words = cache.get()
    if cached_words is not None:
        return cached_words

    # If not in cache, query database
    query = text(r"""
        SELECT word, COUNT(*) as total_occurrences
        FROM (
            SELECT regexp_split_to_table(lower(description), '\s+') as word
            FROM part
            WHERE description IS NOT NULL
        ) t
        GROUP BY word
        ORDER BY total_occurrences DESC
        LIMIT 5;
    """)
    
    result = db.execute(query)
    words = [WordCount(word=row[0], total_occurrences=row[1]) for row in result]
    
    # Only cache if we have results
    if words:
        cache.set(words)
    
    return words 
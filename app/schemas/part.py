from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PartBase(BaseModel):
    """
    Base schema for part data.
    """
    name: str = Field(..., max_length=150)
    sku: str = Field(..., max_length=30)
    description: Optional[str] = Field(None, max_length=1024)
    weight_ounces: Optional[int] = None
    is_active: bool = True

class PartCreate(PartBase):
    """
    Schema for creating a new part.
    """
    pass

class PartUpdate(PartBase):
    """
    Schema for updating an existing part.
    """
    name: Optional[str] = Field(None, max_length=150)
    sku: Optional[str] = Field(None, max_length=30)

class Part(PartBase):
    """
    Schema for part response.
    """
    id: UUID

    class Config:
        from_attributes = True

class WordCount(BaseModel):
    """
    Schema for word count response.
    """
    word: str
    total_occurrences: int

    class Config:
        from_attributes = True 
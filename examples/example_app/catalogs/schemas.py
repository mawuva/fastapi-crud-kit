from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class CategoryBase(BaseModel):
    """Base schema for Category."""
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a Category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a Category."""
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    """Schema for Category response."""
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class TagBase(BaseModel):
    """Base schema for Tag."""
    name: str
    description: Optional[str] = None


class TagCreate(TagBase):
    """Schema for creating a Tag."""
    pass


class TagUpdate(BaseModel):
    """Schema for updating a Tag."""
    name: Optional[str] = None
    description: Optional[str] = None


class TagResponse(TagBase):
    """Schema for Tag response."""
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


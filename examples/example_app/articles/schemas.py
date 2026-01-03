from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ArticleBase(BaseModel):
    """Schéma de base pour Role."""
    title: str
    content: str


class ArticleCreate(ArticleBase):
    """Schéma pour créer un Article."""
    pass


class ArticleUpdate(BaseModel):
    """Schéma pour mettre à jour un Article."""
    title: Optional[str] = None
    content: Optional[str] = None
    
    
class ArticleResponse(ArticleBase):
    """Schéma pour la réponse d'un Article."""
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }
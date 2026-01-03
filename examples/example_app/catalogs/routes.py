from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from .models import Category, Tag


router = APIRouter(prefix="/catalogs", tags=["catalogs"])

@router.get("/categories")
async def list_categories(
    session: AsyncSession = Depends(get_db),
):
    """List all categories."""
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return {
        "categories": [
            {
                "id": cat.id,
                "uuid": str(cat.uuid),
                "name": cat.name,
                "description": cat.description,
            }
            for cat in categories
        ]
    }
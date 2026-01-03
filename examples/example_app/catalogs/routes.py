from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from .models import Category, Tag
from fastapi_crud_kit.query import QueryParams, get_query_parser


router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.get("/categories")
async def list_categories(
    db: AsyncSession = Depends(get_db),
    query: QueryParams = Depends(get_query_parser),
):
    """List all categories."""
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    
    filters = query.filters
    for filter in filters:
        print(filter)
            
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
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .models import Category, Tag
from fastapi_crud_kit.query import parse_query_params, QueryBuilder


router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.get("/categories")
async def list_categories(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """List all categories."""
    # result = await db.execute(select(Category))
    # categories = result.scalars().all()
    
    qp = parse_query_params(request.query_params)
    builder = QueryBuilder(Category)
    statement = builder.apply(qp)
    result = await db.execute(statement)
    categories = result.scalars().all()
    return categories
            
    # return {
    #     "categories": [
    #         {
    #             "id": cat.id,
    #             "uuid": str(cat.uuid),
    #             "name": cat.name,
    #             "description": cat.description,
    #         }
    #         for cat in categories
    #     ]
    # }
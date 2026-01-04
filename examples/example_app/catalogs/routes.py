from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..database import get_db
from .crud import CategoryCRUD, TagCRUD
from .schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    TagCreate,
    TagUpdate,
    TagResponse,
)
from fastapi_crud_kit.query import (
    parse_query_params,
    FilterValidationError,
    FilterValueTypeError,
)
from fastapi_crud_kit.database.exceptions import NotFoundError, ValidationError


router = APIRouter(prefix="/catalogs", tags=["catalogs"])

# Initialize CRUD instances
category_crud = CategoryCRUD()
tag_crud = TagCRUD()


# Category routes
@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    List all categories with optional filtering, sorting, and field selection.
    
    Query parameters:
    - filter[name]=value: Filter by exact name match
    - filter[description]=value: Filter by description (partial match/LIKE)
    - filter[created_at][gte]=value: Filter by created_at (gte, lte, gt, lt)
    - sort=field or sort=-field: Sort by field (prefix with - for descending)
    - include=relation: Include related objects (e.g., include=articles)
    - fields=field1,field2: Select only specific fields
    
    Allowed filters: name (exact), description (partial), created_at (comparison)
    """
    try:
        query_params = parse_query_params(request.query_params)
        categories = await category_crud.list(db, query_params)
        return categories
    except (FilterValidationError, FilterValueTypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid filter: {str(e)}"
        ) from e


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a single category by UUID.
    
    Query parameters:
    - include=relation: Include related objects (e.g., include=articles)
    - fields=field1,field2: Select only specific fields
    """
    query_params = parse_query_params(request.query_params)
    category = await category_crud.get(db, category_id, query_params)
    
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    return category


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new category."""
    try:
        category = await category_crud.create(db, category_in.model_dump())
        return category
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        ) from e


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing category."""
    try:
        # Only include non-None values
        update_data = category_in.model_dump(exclude_unset=True)
        category = await category_crud.update(db, category_id, update_data)
        return category
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        ) from e


@router.delete("/categories/{category_id}", response_model=CategoryResponse)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a category."""
    try:
        category = await category_crud.delete(db, category_id)
        return category
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e


# Tag routes
@router.get("/tags", response_model=list[TagResponse])
async def list_tags(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    List all tags with optional filtering, sorting, and field selection.
    
    Query parameters:
    - filter[name]=value: Filter by exact name match
    - filter[description]=value: Filter by description (partial match/LIKE)
    - filter[created_at][gte]=value: Filter by created_at (gte, lte, gt, lt)
    - sort=field or sort=-field: Sort by field (prefix with - for descending)
    - include=relation: Include related objects (e.g., include=articles)
    - fields=field1,field2: Select only specific fields
    
    Allowed filters: name (exact), description (partial), created_at (comparison)
    """
    try:
        query_params = parse_query_params(request.query_params)
        tags = await tag_crud.list(db, query_params)
        return tags
    except (FilterValidationError, FilterValueTypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid filter: {str(e)}"
        ) from e


@router.get("/tags/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a single tag by UUID.
    
    Query parameters:
    - include=relation: Include related objects (e.g., include=articles)
    - fields=field1,field2: Select only specific fields
    """
    query_params = parse_query_params(request.query_params)
    tag = await tag_crud.get(db, tag_id, query_params)
    
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found"
        )
    
    return tag


@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: TagCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new tag."""
    try:
        tag = await tag_crud.create(db, tag_in.model_dump())
        return tag
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        ) from e


@router.put("/tags/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: UUID,
    tag_in: TagUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing tag."""
    try:
        # Only include non-None values
        update_data = tag_in.model_dump(exclude_unset=True)
        tag = await tag_crud.update(db, tag_id, update_data)
        return tag
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        ) from e


@router.delete("/tags/{tag_id}", response_model=TagResponse)
async def delete_tag(
    tag_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a tag."""
    try:
        tag = await tag_crud.delete(db, tag_id)
        return tag
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
"""
CRUD operations for Category and Tag models.
"""

from fastapi_crud_kit.crud.base import CRUDBase
from fastapi_crud_kit.query import AllowedFilters, QueryBuilderConfig
from .models import Category, Tag


class CategoryCRUD(CRUDBase[Category]):
    """
    CRUD operations for Category model.
    
    Inherits from CRUDBase and provides all standard CRUD operations:
    - list: List all categories with filtering, sorting, etc.
    - get: Get a single category by ID
    - create: Create a new category
    - update: Update an existing category
    - delete: Delete a category
    """
    
    def __init__(self):
        # Define allowed filters for Category
        query_config = QueryBuilderConfig(
            allowed_filters=[
                # Exact match for name
                AllowedFilters.exact("name"),
                # Partial match (LIKE) for description
                AllowedFilters.partial("description"),
                # Multiple operators for created_at (if needed)
                AllowedFilters(
                    field="created_at",
                    default_operator="gte",
                    allowed_operators=["gte", "lte", "gt", "lt"],
                ),
            ],
            ignore_invalid_filters=False,  # Reject invalid filters with error
        )
        super().__init__(model=Category, use_async=True, query_config=query_config)


class TagCRUD(CRUDBase[Tag]):
    """
    CRUD operations for Tag model.
    
    Inherits from CRUDBase and provides all standard CRUD operations:
    - list: List all tags with filtering, sorting, etc.
    - get: Get a single tag by ID
    - create: Create a new tag
    - update: Update an existing tag
    - delete: Delete a tag
    """
    
    def __init__(self):
        # Define allowed filters for Tag
        query_config = QueryBuilderConfig(
            allowed_filters=[
                # Exact match for name
                AllowedFilters.exact("name"),
                # Partial match (LIKE) for description
                AllowedFilters.partial("description"),
                # Multiple operators for created_at (if needed)
                AllowedFilters(
                    field="created_at",
                    default_operator="gte",
                    allowed_operators=["gte", "lte", "gt", "lt"],
                ),
            ],
            ignore_invalid_filters=False,  # Reject invalid filters with error
        )
        super().__init__(model=Tag, use_async=True, query_config=query_config)

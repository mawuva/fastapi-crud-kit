# CRUD Operations

FastAPI CRUD Kit provides a complete set of CRUD operations through the `CRUDBase` class.

## Creating a CRUD Class

Inherit from `CRUDBase` and configure it:

```python
from fastapi_crud_kit.crud.base import CRUDBase
from fastapi_crud_kit.query import QueryBuilderConfig

class CategoryCRUD(CRUDBase[Category]):
    def __init__(self):
        super().__init__(
            model=Category,
            use_async=True,  # or False for sync
            query_config=None,  # Optional query configuration
            default_limit=100,  # Default limit for list()
        )
```

## List Operations

### Basic List

List all items matching query parameters:

```python
query_params = parse_query_params(request.query_params)
categories = await category_crud.list(db, query_params)
```

**Parameters:**
- `session`: SQLAlchemy session (AsyncSession or Session)
- `query_params`: QueryParams object with filters, sort, etc.
- `include_deleted`: If True, include soft-deleted records (default: False)

**Returns:** List of model instances

**Note:** If no pagination is specified, a default limit is applied to prevent loading the entire database.

### Paginated List

Get paginated results with complete metadata:

```python
result = await category_crud.list_paginated(
    db,
    query_params,
    default_per_page=20
)
```

**Returns:** `PaginatedResponse` with:
- `items`: List of results
- `total`: Total number of items
- `page`: Current page number
- `per_page`: Items per page
- `total_pages`: Total number of pages
- `has_next`: Whether there's a next page
- `has_prev`: Whether there's a previous page

**Example Response:**

```python
PaginatedResponse(
    items=[...],
    total=150,
    page=1,
    per_page=20,
    total_pages=8,
    has_next=True,
    has_prev=False
)
```

## Get Operation

Get a single item by ID:

```python
category = await category_crud.get(
    db,
    category_id,
    query_params=None,  # Optional: for includes, fields
    include_deleted=False
)
```

**Parameters:**
- `session`: SQLAlchemy session
- `id`: Primary key value (int, UUID, or string)
- `query_params`: Optional QueryParams for includes/fields
- `include_deleted`: If True, include soft-deleted records

**Returns:** Model instance or None if not found

**Note:** The method automatically detects whether to use `id` or `uuid` based on the identifier type and model structure.

## Create Operation

Create a new item:

```python
category = await category_crud.create(
    db,
    {"name": "Tech", "description": "Technology category"}
)
```

**Parameters:**
- `session`: SQLAlchemy session
- `obj_in`: Dictionary with data or model instance

**Returns:** Created model instance

**Raises:** `ValidationError` if creation fails

**Example:**

```python
# Using dictionary
category = await category_crud.create(db, {
    "name": "Tech",
    "description": "Technology"
})

# Using model instance
new_category = Category(name="Tech", description="Technology")
category = await category_crud.create(db, new_category)
```

## Update Operation

Update an existing item:

```python
category = await category_crud.update(
    db,
    category_id,
    {"name": "Technology", "description": "Updated description"}
)
```

**Parameters:**
- `session`: SQLAlchemy session
- `id`: Primary key value
- `obj_in`: Dictionary with data to update or model instance

**Returns:** Updated model instance

**Raises:**
- `NotFoundError`: If object not found
- `ValidationError`: If update fails

**Example:**

```python
# Partial update (only specified fields)
category = await category_crud.update(db, category_id, {
    "name": "New Name"
})

# Full update
category = await category_crud.update(db, category_id, {
    "name": "New Name",
    "description": "New Description"
})
```

## Delete Operation

Delete an item (soft delete by default if supported):

```python
category = await category_crud.delete(
    db,
    category_id,
    hard=False  # True for hard delete
)
```

**Parameters:**
- `session`: SQLAlchemy session
- `id`: Primary key value
- `hard`: If True, perform hard delete even if soft delete is supported

**Returns:** Deleted model instance

**Raises:** `NotFoundError` if object not found

**Behavior:**
- If model supports soft delete and `hard=False`: Performs soft delete (sets `deleted_at`)
- Otherwise: Performs hard delete (permanent removal)

## Restore Operation

Restore a soft-deleted item:

```python
category = await category_crud.restore(db, category_id)
```

**Parameters:**
- `session`: SQLAlchemy session
- `id`: Primary key value

**Returns:** Restored model instance

**Raises:**
- `NotFoundError`: If object not found
- `ValueError`: If model doesn't support soft delete

## Complete Example

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_crud_kit.query import parse_query_params
from fastapi_crud_kit.database.exceptions import NotFoundError

router = APIRouter()
category_crud = CategoryCRUD()

@router.get("/categories")
async def list_categories(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    query_params = parse_query_params(request.query_params)
    result = await category_crud.list_paginated(db, query_params)
    return result

@router.get("/categories/{category_id}")
async def get_category(
    category_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    query_params = parse_query_params(request.query_params)
    category = await category_crud.get(db, category_id, query_params)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories")
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    category = await category_crud.create(db, category_data.dict())
    return category

@router.put("/categories/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = await category_crud.update(db, category_id, category_data.dict())
        return category
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: UUID,
    hard: bool = False,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = await category_crud.delete(db, category_id, hard=hard)
        return {"message": "Category deleted", "category": category}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")

@router.post("/categories/{category_id}/restore")
async def restore_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = await category_crud.restore(db, category_id)
        return category
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
```

## Error Handling

The CRUD operations raise specific exceptions:

- `NotFoundError`: Object not found
- `ValidationError`: Invalid data
- `DatabaseError`: Database operation failed

Handle them in your routes:

```python
from fastapi_crud_kit.database.exceptions import NotFoundError, ValidationError

try:
    category = await category_crud.get(db, category_id)
except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

## Async vs Sync

All CRUD operations work with both async and sync sessions:

```python
# Async
category_crud = CategoryCRUD()  # use_async=True by default
await category_crud.list(db, query_params)

# Sync
category_crud = CategoryCRUD()
category_crud.use_async = False
category_crud.list(db, query_params)  # No await needed
```

## Next Steps

- Learn about [Query Building](query-building.md) for advanced filtering
- Explore [Database Setup](database-setup.md) for session management
- Check out [Advanced Features](advanced-features.md) for transactions

---

**Previous:** [Models](models.md) | **Next:** [Query Building →](query-building.md)


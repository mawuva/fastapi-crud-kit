# Getting Started

This guide will help you get started with FastAPI CRUD Kit in just a few minutes.

## Installation

Install FastAPI CRUD Kit using pip:

```bash
pip install fastapi-crud-kit
```

Or using poetry:

```bash
poetry add fastapi-crud-kit
```

## Quick Start

### 1. Define Your Model

First, define your SQLAlchemy model. You can use the provided base models or create your own:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    description: Mapped[str | None]
```

Or use the provided base models with built-in features:

```python
from fastapi_crud_kit.models import BaseModel
from sqlalchemy import Column, String

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
```

The `BaseModel` includes:
- Auto-increment integer primary key (`id`)
- UUID field (`uuid`) for external identifiers
- Automatic timestamps (`created_at`, `updated_at`)
- Soft delete support (`deleted_at`)

### 2. Create CRUD Class

Create a CRUD class by inheriting from `CRUDBase`:

```python
from fastapi_crud_kit.crud.base import CRUDBase
from fastapi_crud_kit.query import AllowedFilters, QueryBuilderConfig

class CategoryCRUD(CRUDBase[Category]):
    def __init__(self):
        query_config = QueryBuilderConfig(
            allowed_filters=[
                AllowedFilters.exact("name"),
                AllowedFilters.partial("description"),
            ],
        )
        super().__init__(model=Category, use_async=True, query_config=query_config)
```

### 3. Set Up Database

Configure your database connection:

```python
from fastapi_crud_kit.database import DatabaseFactory

# Async mode (recommended)
factory = DatabaseFactory(
    database_url="postgresql+asyncpg://user:pass@localhost/db",
    use_async=True
)
engine = factory.get_engine()
SessionLocal = factory.get_session_maker(engine)
```

### 4. Create FastAPI Dependency

Create a dependency to get the database session:

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    async with SessionLocal() as session:
        yield session
```

### 5. Use in FastAPI Routes

Create your API routes:

```python
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_crud_kit.query import parse_query_params

router = APIRouter()
category_crud = CategoryCRUD()

@router.get("/categories")
async def list_categories(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    query_params = parse_query_params(request.query_params)
    categories = await category_crud.list(db, query_params)
    return categories

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
    category_data: dict,
    db: AsyncSession = Depends(get_db),
):
    category = await category_crud.create(db, category_data)
    return category

@router.put("/categories/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: dict,
    db: AsyncSession = Depends(get_db),
):
    category = await category_crud.update(db, category_id, category_data)
    return category

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    category = await category_crud.delete(db, category_id)
    return category
```

## Query Parameters

FastAPI CRUD Kit supports powerful query parameters for filtering, sorting, and more:

### Filtering

```
GET /categories?filter[name]=Tech&filter[description][like]=%web%
```

### Sorting

```
GET /categories?sort=name&sort=-created_at
```

Prefix with `-` for descending order.

### Field Selection

```
GET /categories?fields=id,name
```

### Include Relations

```
GET /categories?include=articles
```

### Pagination

```
GET /categories?page=1&per_page=20
```

Or using limit/offset:

```
GET /categories?limit=20&offset=0
```

## Next Steps

- Learn about [Models](models.md) and available mixins
- Explore [CRUD Operations](crud-operations.md) in detail
- Discover [Query Building](query-building.md) features
- Set up your [Database](database-setup.md) properly

---

**Previous:** [Home](index.md) | **Next:** [Models →](models.md)


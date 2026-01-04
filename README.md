# FastAPI CRUD Kit

[![CI](https://github.com/mawuva/fastapi-crud-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/mawuva/fastapi-crud-kit/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/fastapi-crud-kit.svg)](https://pypi.org/project/fastapi-crud-kit/)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-crud-kit.svg)](https://pypi.org/project/fastapi-crud-kit/)
![GitHub License](https://img.shields.io/github/license/mawuva/fastapi-crud-kit)

A powerful CRUD toolkit for FastAPI with SQLAlchemy, featuring query building, filtering, sorting, and field selection with async/sync support.

## Features

- 🚀 **Full CRUD Operations**: Create, Read, Update, Delete with minimal boilerplate
- 🔍 **Advanced Query Building**: Filtering, sorting, field selection, and relationship loading
- ⚡ **Async & Sync Support**: Works with both async and sync SQLAlchemy sessions
- 🛡️ **Filter Validation**: Configurable filter validation with custom callbacks
- 🔒 **Type Safe**: Full type hints support
- 📦 **Production Ready**: Context managers for transactions, retries, and timeouts

## Installation

```bash
pip install fastapi-crud-kit
```

## Quick Start

### 1. Define Your Model

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

### 2. Create CRUD Class

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

### 3. Use in FastAPI Routes

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

### Filtering

```
GET /categories?filter[name]=Tech&filter[description][like]=%web%
```

Supported operators: `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `like`, `ilike`, `in`

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

## Filter Configuration

Configure allowed filters with validation:

```python
from fastapi_crud_kit.query import AllowedFilters, QueryBuilderConfig

query_config = QueryBuilderConfig(
    allowed_filters=[
        AllowedFilters.exact("name"),  # Exact match
        AllowedFilters.partial("description"),  # LIKE search
        AllowedFilters(
            field="created_at",
            default_operator="gte",
            allowed_operators=["gte", "lte", "gt", "lt"],
        ),
    ],
    ignore_invalid_filters=False,  # Raise error on invalid filters
)
```

## Database Setup

### Async Mode

```python
from fastapi_crud_kit.database import DatabaseFactory
from fastapi_crud_kit.database.mode import AsyncModeHandler

handler = AsyncModeHandler()
engine = handler.create_engine("postgresql+asyncpg://user:pass@localhost/db")
session_maker = handler.create_session_maker(engine)
```

### Sync Mode

```python
from fastapi_crud_kit.database.mode import SyncModeHandler

handler = SyncModeHandler()
engine = handler.create_engine("postgresql+psycopg2://user:pass@localhost/db")
session_maker = handler.create_session_maker(engine)
```

## Examples

See the `examples/` directory for complete working examples.

## Requirements

- Python >= 3.10
- SQLAlchemy >= 2.0.45
- Pydantic >= 2.12.5
- FastAPI >= 0.128.0

## License

See LICENSE file for details.

# FastAPI CRUD Kit Documentation

Welcome to the comprehensive documentation for **FastAPI CRUD Kit**, a powerful toolkit for building CRUD operations with FastAPI and SQLAlchemy.

## Overview

FastAPI CRUD Kit provides a complete solution for building RESTful APIs with minimal boilerplate. It offers:

- 🚀 **Full CRUD Operations**: Create, Read, Update, Delete with minimal code
- 🔍 **Advanced Query Building**: Filtering, sorting, field selection, and relationship loading
- ⚡ **Async & Sync Support**: Works seamlessly with both async and sync SQLAlchemy sessions
- 🛡️ **Filter Validation**: Configurable filter validation with custom callbacks
- 🔒 **Type Safe**: Full type hints support throughout
- 📦 **Production Ready**: Context managers for transactions, retries, and timeouts
- 🗑️ **Soft Delete**: Built-in support for soft delete functionality
- 📊 **Pagination**: Built-in pagination support with metadata

## Table of Contents

1. [Getting Started](getting-started.md) - Installation and quick start guide
2. [Models](models.md) - Base models and mixins for your SQLAlchemy models
3. [CRUD Operations](crud-operations.md) - Complete guide to CRUD operations
4. [Query Building](query-building.md) - Filtering, sorting, field selection, and includes
5. [Database Setup](database-setup.md) - Database configuration and session management
6. [Advanced Features](advanced-features.md) - Context managers, transactions, and more
7. [API Reference](api-reference.md) - Complete API reference

## Quick Example

```python
from fastapi_crud_kit.crud.base import CRUDBase
from fastapi_crud_kit.query import AllowedFilters, QueryBuilderConfig, parse_query_params
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

# Define your model
class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

# Create CRUD class
class CategoryCRUD(CRUDBase[Category]):
    def __init__(self):
        query_config = QueryBuilderConfig(
            allowed_filters=[
                AllowedFilters.exact("name"),
                AllowedFilters.partial("description"),
            ],
        )
        super().__init__(model=Category, use_async=True, query_config=query_config)

# Use in FastAPI routes
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
```

## Requirements

- Python >= 3.10
- SQLAlchemy >= 2.0.45
- Pydantic >= 2.12.5
- FastAPI >= 0.128.0

## Installation

```bash
pip install fastapi-crud-kit
```

---

**Next:** [Getting Started →](getting-started.md)

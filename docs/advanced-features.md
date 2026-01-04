# Advanced Features

FastAPI CRUD Kit provides advanced features for production-ready applications including transactions, retries, timeouts, and read-only operations.

## Transactions

Manage database transactions with context managers or decorators.

### TransactionAsync

For async operations:

```python
from fastapi_crud_kit.database import TransactionAsync
from sqlalchemy.ext.asyncio import AsyncSession

# As context manager
async with TransactionAsync(db) as session:
    category = await category_crud.create(session, {"name": "Tech"})
    product = await product_crud.create(session, {"name": "Laptop"})
    # Automatically commits on success, rolls back on exception

# As decorator
@TransactionAsync(db)
async def create_category_and_product():
    category = await category_crud.create(db, {"name": "Tech"})
    product = await product_crud.create(db, {"name": "Laptop"})
```

### TransactionSync

For sync operations:

```python
from fastapi_crud_kit.database import TransactionSync
from sqlalchemy.orm import Session

# As context manager
with TransactionSync(db) as session:
    category = category_crud.create(session, {"name": "Tech"})
    product = product_crud.create(session, {"name": "Laptop"})
    # Automatically commits on success, rolls back on exception

# As decorator
@TransactionSync(db)
def create_category_and_product():
    category = category_crud.create(db, {"name": "Tech"})
    product = product_crud.create(db, {"name": "Laptop"})
```

### Isolation Levels

Set transaction isolation level:

```python
from fastapi_crud_kit.database import TransactionAsync

async with TransactionAsync(
    db,
    isolation_level="READ COMMITTED"
) as session:
    # Transaction with specific isolation level
    pass
```

Supported levels:
- `READ UNCOMMITTED`
- `READ COMMITTED` (default)
- `REPEATABLE READ`
- `SERIALIZABLE`

## Retry Operations

Automatically retry operations on transient failures with exponential backoff.

### RetryAsync

For async operations:

```python
from fastapi_crud_kit.database import RetryAsync

# As context manager
async with RetryAsync(max_attempts=3, delay=1.0, backoff=2.0):
    result = await category_crud.list(db, query_params)
    # Retries on database exceptions

# As decorator
@RetryAsync(max_attempts=3, delay=1.0, backoff=2.0)
async def get_categories():
    return await category_crud.list(db, query_params)
```

### RetrySync

For sync operations:

```python
from fastapi_crud_kit.database import RetrySync

# As context manager
with RetrySync(max_attempts=3, delay=1.0, backoff=2.0):
    result = category_crud.list(db, query_params)
    # Retries on database exceptions

# As decorator
@RetrySync(max_attempts=3, delay=1.0, backoff=2.0)
def get_categories():
    return category_crud.list(db, query_params)
```

### Retry Configuration

```python
RetryAsync(
    max_attempts=3,  # Maximum retry attempts
    delay=1.0,  # Initial delay in seconds
    backoff=2.0,  # Exponential backoff multiplier
    exceptions=(OperationalError, ConnectionError),  # Exceptions to retry
    log=True,  # Enable logging
)
```

**Retry delays:**
- Attempt 1: 1.0 seconds
- Attempt 2: 2.0 seconds
- Attempt 3: 4.0 seconds

## Timeouts

Add timeouts to prevent operations from running indefinitely.

### TimeoutAsync

For async operations:

```python
from fastapi_crud_kit.database import TimeoutAsync

# As context manager
async with TimeoutAsync(seconds=5.0):
    result = await category_crud.list(db, query_params)
    # Raises TimeoutError if operation takes longer than 5 seconds

# As decorator
@TimeoutAsync(seconds=5.0)
async def get_categories():
    return await category_crud.list(db, query_params)
```

### TimeoutSync

For sync operations:

```python
from fastapi_crud_kit.database import TimeoutSync

# As context manager
with TimeoutSync(seconds=5.0):
    result = category_crud.list(db, query_params)
    # Raises TimeoutError if operation takes longer than 5 seconds

# As decorator
@TimeoutSync(seconds=5.0)
def get_categories():
    return category_crud.list(db, query_params)
```

### Timeout Configuration

```python
TimeoutAsync(
    seconds=5.0,  # Timeout in seconds
    timeout_exception=TimeoutError,  # Exception to raise
    log=True,  # Enable logging
)
```

## Read-Only Operations

Enforce read-only operations and detect accidental writes.

### ReadOnlyAsync

For async operations:

```python
from fastapi_crud_kit.database import ReadOnlyAsync

# As context manager
async with ReadOnlyAsync(db, strict=True):
    # Only read operations allowed
    categories = await category_crud.list(db, query_params)
    # Raises ReadOnlyViolationError on write operations

# As decorator
@ReadOnlyAsync(db, strict=True)
async def get_categories():
    return await category_crud.list(db, query_params)
```

### ReadOnlySync

For sync operations:

```python
from fastapi_crud_kit.database import ReadOnlySync

# As context manager
with ReadOnlySync(db, strict=True):
    # Only read operations allowed
    categories = category_crud.list(db, query_params)
    # Raises ReadOnlyViolationError on write operations

# As decorator
@ReadOnlySync(db, strict=True)
def get_categories():
    return category_crud.list(db, query_params)
```

### Read-Only Configuration

```python
ReadOnlyAsync(
    session=db,  # Session to monitor (optional, auto-detected)
    strict=True,  # Raise error on write operations
    log=True,  # Enable logging
    session_param="db",  # Parameter name for session (auto-detected)
)
```

**Monitored operations:**
- `add`, `add_all`
- `delete`
- `merge`
- `bulk_insert_mappings`, `bulk_update_mappings`, `bulk_save_objects`
- `execute` (for INSERT/UPDATE/DELETE)
- `commit`, `flush`

## Combining Context Managers

Combine multiple context managers for complex scenarios:

```python
from fastapi_crud_kit.database import (
    TransactionAsync,
    RetryAsync,
    TimeoutAsync,
)

async with TransactionAsync(db) as session:
    async with RetryAsync(max_attempts=3):
        async with TimeoutAsync(seconds=10.0):
            # Transaction with retry and timeout
            category = await category_crud.create(session, {"name": "Tech"})
```

## Decorator Usage

All context managers can be used as decorators:

```python
from fastapi_crud_kit.database import TransactionAsync, RetryAsync

@TransactionAsync(db)
@RetryAsync(max_attempts=3)
async def create_category_with_retry(data: dict):
    return await category_crud.create(db, data)
```

## Error Handling

### Database Exceptions

```python
from fastapi_crud_kit.database.exceptions import (
    DatabaseError,
    ConnectionError,
    TransactionError,
    ReadOnlyViolationError,
    NotFoundError,
    ValidationError,
)

try:
    category = await category_crud.get(db, category_id)
except NotFoundError:
    raise HTTPException(status_code=404, detail="Category not found")
except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
except DatabaseError as e:
    raise HTTPException(status_code=500, detail="Database error")
```

### Retry Exceptions

```python
from fastapi_crud_kit.database import RetryAsync
from sqlalchemy.exc import OperationalError

async with RetryAsync(
    max_attempts=3,
    exceptions=(OperationalError, ConnectionError)
):
    try:
        result = await category_crud.list(db, query_params)
    except OperationalError:
        # Will be retried automatically
        pass
```

## Best Practices

1. **Use transactions for multi-step operations**: Ensure atomicity
2. **Add retries for transient failures**: Handle network issues gracefully
3. **Set timeouts for long operations**: Prevent hanging requests
4. **Use read-only for queries**: Prevent accidental writes
5. **Combine context managers**: Build robust operations
6. **Handle exceptions properly**: Provide meaningful error messages
7. **Enable logging**: Monitor operations in production

## Complete Example

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi_crud_kit.database import (
    TransactionAsync,
    RetryAsync,
    TimeoutAsync,
    ReadOnlyAsync,
)
from fastapi_crud_kit.database.exceptions import NotFoundError, ValidationError

router = APIRouter()

@router.get("/categories")
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    async with ReadOnlyAsync(db):
        async with RetryAsync(max_attempts=3):
            async with TimeoutAsync(seconds=5.0):
                query_params = parse_query_params(request.query_params)
                return await category_crud.list_paginated(db, query_params)

@router.post("/categories")
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    async with TransactionAsync(db):
        async with RetryAsync(max_attempts=3):
            try:
                return await category_crud.create(db, category_data.dict())
            except ValidationError as e:
                raise HTTPException(status_code=400, detail=str(e))
```

## Next Steps

- Review the [API Reference](api-reference.md) for complete details
- Check [Database Setup](database-setup.md) for configuration
- Explore [CRUD Operations](crud-operations.md) usage

---

**Previous:** [Database Setup](database-setup.md) | **Next:** [API Reference →](api-reference.md)


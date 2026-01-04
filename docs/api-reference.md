# API Reference

Complete API reference for FastAPI CRUD Kit.

## CRUD Operations

### CRUDBase

Base class for CRUD operations.

```python
class CRUDBase(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        use_async: bool | None = None,
        query_config: Optional[QueryBuilderConfig] = None,
        default_limit: int = 100,
    )
```

**Methods:**

- `list(session, query_params, include_deleted=False)` - List items
- `list_paginated(session, query_params, include_deleted=False, default_per_page=20)` - List with pagination
- `get(session, id, query_params=None, include_deleted=False)` - Get single item
- `create(session, obj_in)` - Create new item
- `update(session, id, obj_in)` - Update item
- `delete(session, id, hard=False)` - Delete item
- `restore(session, id)` - Restore soft-deleted item

## Query Building

### QueryBuilder

Build SQLAlchemy queries from query parameters.

```python
class QueryBuilder:
    def __init__(self, model: Type[Any], config: Optional[QueryBuilderConfig] = None)
    
    def apply(self, query_params: QueryParams) -> Select[Any]
    def apply_filters(self, filters: list[FilterSchema]) -> "QueryBuilder"
    def apply_sort(self, sort: list[str]) -> "QueryBuilder"
    def apply_fields(self, fields: list[str]) -> "QueryBuilder"
    def apply_include(self, include: list[str]) -> "QueryBuilder"
    def apply_pagination(self, page: int, per_page: int) -> "QueryBuilder"
```

### QueryBuilderConfig

Configuration for query building and validation.

```python
class QueryBuilderConfig:
    def __init__(
        self,
        allowed_filters: Optional[List[AllowedFilters]] = None,
        allowed_sorts: Optional[List[AllowedSort]] = None,
        allowed_fields: Optional[List[AllowedField]] = None,
        allowed_includes: Optional[List[AllowedInclude]] = None,
        ignore_invalid_errors: bool = False,
    )
```

**Methods:**

- `get_allowed_filter(field_or_alias)` - Get allowed filter config
- `is_filter_allowed(field_or_alias)` - Check if filter is allowed
- `get_allowed_sort(field_or_alias)` - Get allowed sort config
- `is_sort_allowed(field_or_alias)` - Check if sort is allowed
- `get_allowed_field(field_or_alias)` - Get allowed field config
- `is_field_allowed(field_or_alias)` - Check if field is allowed
- `get_allowed_include(relationship_or_alias)` - Get allowed include config
- `is_include_allowed(relationship_or_alias)` - Check if include is allowed

### QueryParams

Query parameters schema.

```python
class QueryParams:
    filters: List[FilterSchema]
    sort: List[str]
    include: List[str]
    fields: List[str]
    page: Optional[int]
    per_page: Optional[int]
    limit: Optional[int]
    offset: Optional[int]
```

### FilterSchema

Filter condition schema.

```python
class FilterSchema:
    field: str
    operator: str
    value: Any
```

### PaginatedResponse

Paginated response schema.

```python
class PaginatedResponse(Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
```

## Filters

### AllowedFilters

Configuration for allowed filters.

```python
class AllowedFilters:
    def __init__(
        self,
        field: str,
        default_operator: FilterOperator | str = FilterOperator.EQUAL,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
        alias: str | None = None,
        callback: Optional[Callable[[Any, Any], Any]] = None,
    )
    
    @classmethod
    def exact(cls, field: str, alias: Optional[str] = None) -> "AllowedFilters"
    
    @classmethod
    def partial(cls, field: str, alias: Optional[str] = None) -> "AllowedFilters"
    
    @classmethod
    def custom(
        cls,
        field: str,
        callback: Callable[[Any, Any], Any],
        alias: Optional[str] = None,
    ) -> "AllowedFilters"
```

### FilterOperator

Enumeration of filter operators.

```python
class FilterOperator(str, Enum):
    EQUAL = "eq"
    NOT_EQUAL = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    LIKE = "like"
    ILIKE = "ilike"
    IN = "in"
```

## Sorting

### AllowedSort

Configuration for allowed sort fields.

```python
class AllowedSort:
    def __init__(
        self,
        *fields: str,
        direction: Literal["asc", "desc"] = "asc",
        alias: Optional[str] = None,
    )
```

## Fields

### AllowedField

Configuration for allowed field selection.

```python
class AllowedField:
    def __init__(
        self,
        field: str,
        alias: Optional[str] = None,
    )
```

## Includes

### AllowedInclude

Configuration for allowed relationship includes.

```python
class AllowedInclude:
    def __init__(
        self,
        relationship: str,
        alias: Optional[str] = None,
    )
```

## Database

### DatabaseFactory

Factory for creating database components.

```python
class DatabaseFactory:
    def __init__(
        self,
        database_url: str,
        database_type: Optional[str] = None,
        use_async: bool = True,
        base: Optional[Any] = None,
        echo: bool = False,
        pool_pre_ping: bool = True,
    )
    
    def get_engine(self) -> Any
    def get_session_maker(self, engine: Optional[Any] = None) -> Any
    def get_base(self) -> Any
    def create_all_tables(self, engine: Optional[Any] = None) -> None
    async def create_all_tables_async(self, engine: Optional[Any] = None) -> None
    def drop_all_tables(self, engine: Optional[Any] = None) -> None
    async def drop_all_tables_async(self, engine: Optional[Any] = None) -> None
    
    @classmethod
    def from_settings(
        cls,
        settings: Any,
        use_async: bool = True,
        base: Optional[Any] = None,
        echo: bool = False,
        pool_pre_ping: bool = True,
    ) -> DatabaseFactory
```

## Context Managers

### TransactionAsync

Async transaction context manager.

```python
class TransactionAsync(AbstractAsyncContextManager):
    def __init__(
        self,
        session: AsyncSession,
        isolation_level: str = "READ COMMITTED",
        log: bool = False,
    )
```

### TransactionSync

Sync transaction context manager.

```python
class TransactionSync(AbstractContextManager):
    def __init__(
        self,
        session: Session,
        isolation_level: str = "READ COMMITTED",
        log: bool = False,
    )
```

### RetryAsync

Async retry context manager.

```python
class RetryAsync(AbstractAsyncContextManager):
    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: tuple[type[Exception], ...] = RETRYABLE_EXCEPTIONS,
        log: bool = False,
    )
```

### RetrySync

Sync retry context manager.

```python
class RetrySync(AbstractContextManager):
    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: tuple[type[Exception], ...] = RETRYABLE_EXCEPTIONS,
        log: bool = False,
    )
```

### TimeoutAsync

Async timeout context manager.

```python
class TimeoutAsync(AbstractAsyncContextManager):
    def __init__(
        self,
        seconds: float,
        timeout_exception: type[Exception] = TimeoutError,
        log: bool = False,
    )
```

### TimeoutSync

Sync timeout context manager.

```python
class TimeoutSync(AbstractContextManager):
    def __init__(
        self,
        seconds: float,
        timeout_exception: type[Exception] = TimeoutError,
        log: bool = False,
    )
```

### ReadOnlyAsync

Async read-only context manager.

```python
class ReadOnlyAsync(AbstractAsyncContextManager):
    def __init__(
        self,
        session: AsyncSession | None = None,
        strict: bool = True,
        log: bool = False,
        session_param: str | None = None,
    )
```

### ReadOnlySync

Sync read-only context manager.

```python
class ReadOnlySync(AbstractContextManager):
    def __init__(
        self,
        session: Session | None = None,
        strict: bool = True,
        log: bool = False,
        session_param: str | None = None,
    )
```

## Exceptions

### Database Exceptions

```python
class DatabaseError(Exception)
class ConnectionError(DatabaseError)
class TransactionError(DatabaseError)
class ReadOnlyViolationError(DatabaseError)
class IsolationLevelError(DatabaseError)
class NotFoundError(DatabaseError)
class ValidationError(DatabaseError)
```

### Query Exceptions

```python
class QueryBuilderError(Exception)
class FilterValidationError(QueryBuilderError)
class FilterValueTypeError(FilterValidationError)
class SortValidationError(QueryBuilderError)
class FieldValidationError(QueryBuilderError)
class IncludeValidationError(QueryBuilderError)
```

## Models

### BaseModel

Base model with UUID, timestamps, and soft delete.

```python
class BaseModel(PrimaryKeyMixin, UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __abstract__ = True
```

### BaseModelWithUUIDPK

Base model with UUID primary key.

```python
class BaseModelWithUUIDPK(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __abstract__ = True
```

### Mixins

```python
class PrimaryKeyMixin
class UUIDMixin
class TimestampMixin
class SoftDeleteMixin
```

### GUID

Platform-independent GUID type.

```python
class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True
```

## Utility Functions

### parse_query_params

Parse query parameters from request.

```python
def parse_query_params(
    query_params: Mapping[str, Union[str, List[str]]]
) -> QueryParams
```

## Session Helpers

### get_async_db

Async session dependency.

```python
def get_async_db() -> AsyncSession
```

### get_sync_db

Sync session dependency.

```python
def get_sync_db() -> Session
```

---

**Previous:** [Advanced Features](advanced-features.md) | **Back to:** [Home](index.md)


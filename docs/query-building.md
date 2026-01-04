# Query Building

FastAPI CRUD Kit provides powerful query building capabilities including filtering, sorting, field selection, and relationship loading.

## Query Parameters

Query parameters are parsed from the request URL and converted into a `QueryParams` object:

```python
from fastapi_crud_kit.query import parse_query_params

query_params = parse_query_params(request.query_params)
```

The `QueryParams` object contains:
- `filters`: List of filter conditions
- `sort`: List of sort fields
- `include`: List of relationships to load
- `fields`: List of fields to select
- `page`, `per_page`: Pagination parameters
- `limit`, `offset`: Alternative pagination parameters

## Filtering

### Basic Filtering

Filter results using query parameters:

```
GET /categories?filter[name]=Tech
GET /categories?filter[name][eq]=Tech
GET /categories?filter[description][like]=%web%
```

### Filter Operators

Supported operators:

- `eq` - Equal (default)
- `ne` - Not equal
- `lt` - Less than
- `lte` - Less than or equal
- `gt` - Greater than
- `gte` - Greater than or equal
- `like` - LIKE pattern matching (case-sensitive)
- `ilike` - ILIKE pattern matching (case-insensitive)
- `in` - Value in list

### Filter Configuration

Configure allowed filters using `QueryBuilderConfig`:

```python
from fastapi_crud_kit.query import AllowedFilters, QueryBuilderConfig

query_config = QueryBuilderConfig(
    allowed_filters=[
        # Exact match only
        AllowedFilters.exact("name"),
        
        # Partial match (LIKE)
        AllowedFilters.partial("description"),
        
        # Multiple operators
        AllowedFilters(
            field="created_at",
            default_operator="gte",
            allowed_operators=["gte", "lte", "gt", "lt"],
        ),
        
        # Custom filter with callback
        AllowedFilters.custom(
            field="status",
            callback=lambda query, value: query.where(
                Category.status == value.upper()
            ),
        ),
    ],
    ignore_invalid_errors=False,  # Raise error on invalid filters
)
```

### Filter Examples

**Exact Match:**
```
GET /categories?filter[name]=Tech
```

**Comparison:**
```
GET /categories?filter[price][gte]=100
GET /categories?filter[price][lte]=500
GET /categories?filter[created_at][gt]=2024-01-01
```

**Pattern Matching:**
```
GET /categories?filter[description][like]=%web%
GET /categories?filter[description][ilike]=%WEB%
```

**In List:**
```
GET /categories?filter[id][in]=1,2,3
```

**Multiple Filters:**
```
GET /categories?filter[name]=Tech&filter[price][gte]=100
```

### Custom Filter Callbacks

For complex filtering logic, use custom callbacks:

```python
def filter_by_category(query, value):
    # Custom logic: filter by category name or ID
    if value.isdigit():
        return query.where(Category.id == int(value))
    else:
        return query.where(Category.name == value)

query_config = QueryBuilderConfig(
    allowed_filters=[
        AllowedFilters.custom("category", filter_by_category),
    ],
)
```

## Sorting

### Basic Sorting

Sort results using the `sort` parameter:

```
GET /categories?sort=name
GET /categories?sort=-created_at  # Descending
GET /categories?sort=name&sort=-created_at  # Multiple sorts
```

Prefix with `-` for descending order.

### Sort Configuration

Configure allowed sort fields:

```python
from fastapi_crud_kit.query import AllowedSort, QueryBuilderConfig

query_config = QueryBuilderConfig(
    allowed_sorts=[
        AllowedSort("name"),
        AllowedSort("created_at", direction="desc"),
        AllowedSort("price", "name"),  # Multiple fields
    ],
)
```

### Sort Examples

**Single Field:**
```
GET /categories?sort=name
GET /categories?sort=-name  # Descending
```

**Multiple Fields:**
```
GET /categories?sort=name&sort=-created_at
```

## Field Selection

Select specific fields to return:

```
GET /categories?fields=id,name
GET /categories?fields=id,name,description
```

### Field Configuration

Configure allowed fields:

```python
from fastapi_crud_kit.query import AllowedField, QueryBuilderConfig

query_config = QueryBuilderConfig(
    allowed_fields=[
        AllowedField("id"),
        AllowedField("name"),
        AllowedField("description"),
        AllowedField("created_at"),
    ],
)
```

**Note:** Field selection is useful for reducing response size and improving performance.

## Include Relations

Eagerly load relationships:

```
GET /categories?include=products
GET /categories?include=products,tags
```

### Include Configuration

Configure allowed includes:

```python
from fastapi_crud_kit.query import AllowedInclude, QueryBuilderConfig

query_config = QueryBuilderConfig(
    allowed_includes=[
        AllowedInclude("products"),
        AllowedInclude("tags"),
        AllowedInclude("author", alias="user"),  # Use alias in URL
    ],
)
```

### Include Examples

**Single Relation:**
```
GET /categories?include=products
```

**Multiple Relations:**
```
GET /categories?include=products,tags
```

**Nested Relations:**
```
GET /categories?include=products.tags
```

## Pagination

### Page-based Pagination

```
GET /categories?page=1&per_page=20
```

**Response:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8,
  "has_next": true,
  "has_prev": false
}
```

### Limit/Offset Pagination

```
GET /categories?limit=20&offset=0
```

## Complete Example

```python
from fastapi_crud_kit.crud.base import CRUDBase
from fastapi_crud_kit.query import (
    AllowedFilters,
    AllowedSort,
    AllowedField,
    AllowedInclude,
    QueryBuilderConfig,
)

class CategoryCRUD(CRUDBase[Category]):
    def __init__(self):
        query_config = QueryBuilderConfig(
            allowed_filters=[
                AllowedFilters.exact("name"),
                AllowedFilters.partial("description"),
                AllowedFilters(
                    field="created_at",
                    default_operator="gte",
                    allowed_operators=["gte", "lte", "gt", "lt"],
                ),
            ],
            allowed_sorts=[
                AllowedSort("name"),
                AllowedSort("created_at", direction="desc"),
            ],
            allowed_fields=[
                AllowedField("id"),
                AllowedField("name"),
                AllowedField("description"),
                AllowedField("created_at"),
            ],
            allowed_includes=[
                AllowedInclude("products"),
                AllowedInclude("tags"),
            ],
            ignore_invalid_errors=False,
        )
        super().__init__(model=Category, use_async=True, query_config=query_config)
```

## Query Examples

### Complex Query

```
GET /categories?filter[name]=Tech&filter[price][gte]=100&sort=-created_at&include=products&fields=id,name,price&page=1&per_page=20
```

This query:
- Filters by name="Tech" and price >= 100
- Sorts by created_at descending
- Includes products relationship
- Selects only id, name, and price fields
- Returns page 1 with 20 items per page

### Search with Pagination

```
GET /categories?filter[description][ilike]=%web%&sort=name&page=2&per_page=10
```

## Validation

When `ignore_invalid_errors=False` (default), invalid filters, sorts, fields, or includes will raise exceptions:

- `FilterValidationError`: Invalid filter field or operator
- `SortValidationError`: Invalid sort field
- `FieldValidationError`: Invalid field selection
- `IncludeValidationError`: Invalid relationship include

Set `ignore_invalid_errors=True` to silently ignore invalid parameters:

```python
query_config = QueryBuilderConfig(
    allowed_filters=[...],
    ignore_invalid_errors=True,  # Ignore invalid parameters
)
```

## Best Practices

1. **Always configure allowed filters**: Prevents SQL injection and improves security
2. **Use field selection**: Reduce response size for better performance
3. **Configure includes**: Control which relationships can be loaded
4. **Use pagination**: Always paginate large result sets
5. **Validate inputs**: Set `ignore_invalid_errors=False` in production
6. **Use indexes**: Ensure filtered and sorted fields are indexed

## Next Steps

- Learn about [Database Setup](database-setup.md) for session management
- Explore [Advanced Features](advanced-features.md) for transactions
- Check the [API Reference](api-reference.md) for complete details

---

**Previous:** [CRUD Operations](crud-operations.md) | **Next:** [Database Setup →](database-setup.md)


# Models

FastAPI CRUD Kit provides base model classes and mixins to simplify your SQLAlchemy model definitions.

## Base Models

### BaseModel

The `BaseModel` class combines all common mixins to provide a complete base model:

```python
from fastapi_crud_kit.models import BaseModel
from sqlalchemy import Column, String

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
```

**Features:**
- Auto-increment integer primary key (`id`) - internal identifier
- UUID field (`uuid`) - external/public identifier, NOT primary key
- Automatic timestamps (`created_at`, `updated_at`)
- Soft delete support (`deleted_at`)

### BaseModelWithUUIDPK

If you prefer UUID as the primary key:

```python
from fastapi_crud_kit.models import BaseModelWithUUIDPK
from sqlalchemy import Column, String

class User(BaseModelWithUUIDPK):
    __tablename__ = "users"
    
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
```

**Features:**
- UUID primary key (`id`)
- Automatic timestamps (`created_at`, `updated_at`)
- Soft delete support (`deleted_at`)

## Mixins

You can also use individual mixins to build custom base models:

### PrimaryKeyMixin

Adds an auto-increment integer primary key:

```python
from fastapi_crud_kit.models import PrimaryKeyMixin
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(PrimaryKeyMixin, Base):
    __tablename__ = "users"
    # id is automatically added as Integer primary key
```

### UUIDMixin

Adds a UUID field (not primary key by default):

```python
from fastapi_crud_kit.models import PrimaryKeyMixin, UUIDMixin

class User(PrimaryKeyMixin, UUIDMixin, Base):
    __tablename__ = "users"
    # id (Integer, PK) added by PrimaryKeyMixin
    # uuid (UUID) added by UUIDMixin, external identifier
```

The UUID field is useful for:
- External/public identifiers (API responses)
- Security (hiding internal IDs)
- Distributed systems

### TimestampMixin

Adds automatic timestamps:

```python
from fastapi_crud_kit.models import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users"
    # created_at and updated_at are automatically added
```

**Fields:**
- `created_at`: Set automatically on creation
- `updated_at`: Set automatically on creation and update

Both use UTC timezone.

### SoftDeleteMixin

Adds soft delete functionality:

```python
from fastapi_crud_kit.models import SoftDeleteMixin

class User(SoftDeleteMixin, Base):
    __tablename__ = "users"
    # deleted_at is automatically added
```

**Features:**
- `deleted_at`: DateTime field (nullable)
- `soft_delete()`: Method to mark as deleted
- `restore()`: Method to restore a deleted record
- `is_deleted`: Property to check deletion status

**Usage:**

```python
# Soft delete
user.soft_delete()

# Check if deleted
if user.is_deleted:
    print("User is deleted")

# Restore
user.restore()
```

The CRUD operations automatically exclude soft-deleted records unless `include_deleted=True` is specified.

## GUID Type

The package provides a `GUID` type decorator for platform-independent UUID storage:

```python
from fastapi_crud_kit.models import GUID
from sqlalchemy import Column

class User(Base):
    __tablename__ = "users"
    uuid = Column(GUID(), primary_key=True)
```

**Features:**
- Uses PostgreSQL UUID type when available
- Falls back to CHAR(36) for other databases
- Handles conversion between UUID objects and strings

## Custom Base Models

You can create custom base models by combining mixins:

```python
from fastapi_crud_kit.models import (
    PrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin
)
from fastapi_crud_kit.database.base import Base

class MyBaseModel(PrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    __abstract__ = True

class User(MyBaseModel):
    __tablename__ = "users"
    name = Column(String)
```

## Model Examples

### Simple Model

```python
from fastapi_crud_kit.models import BaseModel
from sqlalchemy import Column, String, Integer

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
```

### Model with Relationships

```python
from fastapi_crud_kit.models import BaseModel
from sqlalchemy import Column, String, ForeignKey, relationship

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="category")

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
```

### Model with UUID Primary Key

```python
from fastapi_crud_kit.models import BaseModelWithUUIDPK
from sqlalchemy import Column, String

class User(BaseModelWithUUIDPK):
    __tablename__ = "users"
    
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
```

## Best Practices

1. **Use BaseModel for most cases**: It provides all common features out of the box
2. **Use UUID for external identifiers**: The `uuid` field in `BaseModel` is perfect for API responses
3. **Enable soft delete for important data**: Prevents accidental data loss
4. **Combine mixins for flexibility**: Create custom base models when needed
5. **Use relationships for related data**: SQLAlchemy relationships work seamlessly with the CRUD operations

## Next Steps

- Learn about [CRUD Operations](crud-operations.md)
- Explore [Query Building](query-building.md) for filtering and sorting
- Check out [Database Setup](database-setup.md) for configuration

---

**Previous:** [Getting Started](getting-started.md) | **Next:** [CRUD Operations →](crud-operations.md)


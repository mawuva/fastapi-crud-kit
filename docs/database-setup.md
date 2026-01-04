# Database Setup

FastAPI CRUD Kit provides flexible database configuration supporting both async and sync SQLAlchemy sessions.

## DatabaseFactory

The `DatabaseFactory` class simplifies database setup by automatically detecting the database type and configuring the appropriate drivers.

### Basic Setup

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

### Sync Mode

```python
# Sync mode
factory = DatabaseFactory(
    database_url="postgresql+psycopg2://user:pass@localhost/db",
    use_async=False
)

engine = factory.get_engine()
SessionLocal = factory.get_session_maker(engine)
```

## Supported Databases

The factory automatically detects and configures:

- **PostgreSQL**: `postgresql://` or `postgres://`
  - Async: `postgresql+asyncpg://`
  - Sync: `postgresql+psycopg2://`
- **MySQL**: `mysql://`
  - Async: `mysql+aiomysql://`
  - Sync: `mysql+pymysql://`
- **SQLite**: `sqlite://`
  - Async: `sqlite+aiosqlite://`
  - Sync: `sqlite://`

## Factory Options

```python
factory = DatabaseFactory(
    database_url="postgresql://user:pass@localhost/db",
    database_type=None,  # Auto-detect from URL
    use_async=True,  # Async or sync mode
    base=None,  # Custom Base class (optional)
    echo=False,  # Log SQL queries
    pool_pre_ping=True,  # Verify connections before use
)
```

### Parameters

- `database_url`: Database connection URL
- `database_type`: Database type (auto-detected if None)
- `use_async`: Use async mode (default: True)
- `base`: Custom SQLAlchemy Base class
- `echo`: Log SQL queries for debugging
- `pool_pre_ping`: Check connections before use (recommended)

## Creating Tables

### Async Mode

```python
async def init_db():
    factory = DatabaseFactory("postgresql+asyncpg://...", use_async=True)
    engine = factory.get_engine()
    base = factory.get_base()
    
    async with engine.begin() as conn:
        await factory.create_all_tables_async(engine)
```

### Sync Mode

```python
def init_db():
    factory = DatabaseFactory("postgresql+psycopg2://...", use_async=False)
    engine = factory.get_engine()
    base = factory.get_base()
    
    factory.create_all_tables(engine)
```

## Session Management

### Async Session Dependency

```python
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Sync Session Dependency

```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    with SessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
```

## Using with Settings

Create factory from a settings object:

```python
from fastapi_crud_kit.database import DatabaseFactory

class Settings:
    DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
    DATABASE_TYPE = "postgresql"  # Optional

settings = Settings()
factory = DatabaseFactory.from_settings(settings, use_async=True)
```

## Custom Base Class

Use a custom Base class:

```python
from sqlalchemy.orm import DeclarativeBase

class CustomBase(DeclarativeBase):
    pass

factory = DatabaseFactory(
    database_url="postgresql+asyncpg://...",
    base=CustomBase
)
```

## Database Modes

### AsyncModeHandler

For async operations:

```python
from fastapi_crud_kit.database.mode import AsyncModeHandler

handler = AsyncModeHandler()
engine = handler.create_engine("postgresql+asyncpg://...")
session_maker = handler.create_session_maker(engine)
```

### SyncModeHandler

For sync operations:

```python
from fastapi_crud_kit.database.mode import SyncModeHandler

handler = SyncModeHandler()
engine = handler.create_engine("postgresql+psycopg2://...")
session_maker = handler.create_session_maker(engine)
```

## Helper Functions

### get_async_db

Pre-configured async session dependency:

```python
from fastapi_crud_kit.database import get_async_db
from fastapi import Depends

@router.get("/items")
async def list_items(db: AsyncSession = Depends(get_async_db)):
    # Use db session
    pass
```

**Note:** You need to configure the session maker first:

```python
from fastapi_crud_kit.database.session import configure_async_db

factory = DatabaseFactory("postgresql+asyncpg://...")
SessionLocal = factory.get_session_maker()
configure_async_db(SessionLocal)
```

### get_sync_db

Pre-configured sync session dependency:

```python
from fastapi_crud_kit.database import get_sync_db
from fastapi import Depends

@router.get("/items")
def list_items(db: Session = Depends(get_sync_db)):
    # Use db session
    pass
```

## Complete Setup Example

### Async Setup

```python
from fastapi import FastAPI
from fastapi_crud_kit.database import DatabaseFactory
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

factory = None
SessionLocal = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global factory, SessionLocal
    factory = DatabaseFactory(
        database_url="postgresql+asyncpg://user:pass@localhost/db",
        use_async=True,
        echo=False,
        pool_pre_ping=True,
    )
    engine = factory.get_engine()
    SessionLocal = factory.get_session_maker(engine)
    
    # Create tables
    async with engine.begin() as conn:
        await factory.create_all_tables_async(engine)
    
    yield
    
    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Sync Setup

```python
from fastapi import FastAPI
from fastapi_crud_kit.database import DatabaseFactory
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

factory = None
SessionLocal = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global factory, SessionLocal
    factory = DatabaseFactory(
        database_url="postgresql+psycopg2://user:pass@localhost/db",
        use_async=False,
        echo=False,
        pool_pre_ping=True,
    )
    engine = factory.get_engine()
    SessionLocal = factory.get_session_maker(engine)
    
    # Create tables
    factory.create_all_tables(engine)
    
    yield
    
    # Shutdown
    engine.dispose()

app = FastAPI(lifespan=lifespan)

def get_db():
    with SessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
```

## Connection Pooling

The factory automatically configures connection pooling. For advanced configuration:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Custom engine configuration
engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

## Best Practices

1. **Use async mode**: Better performance for I/O-bound operations
2. **Enable pool_pre_ping**: Prevents stale connections
3. **Set appropriate pool size**: Based on your application's needs
4. **Use context managers**: Ensure proper session cleanup
5. **Handle exceptions**: Always rollback on errors
6. **Close sessions**: Use try/finally or context managers

## Next Steps

- Learn about [Advanced Features](advanced-features.md) for transactions
- Explore [CRUD Operations](crud-operations.md) usage
- Check the [API Reference](api-reference.md) for complete details

---

**Previous:** [Query Building](query-building.md) | **Next:** [Advanced Features →](advanced-features.md)


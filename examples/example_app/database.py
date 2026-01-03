"""Database configuration using fastapi-crud-kit."""

from fastapi_crud_kit.database import DatabaseFactory, get_async_db
from fastapi_crud_kit.database.base import Base

# Import models to register them with SQLAlchemy
from .catalogs.models import Category, Tag
from .articles.models import Article

# Database URL - using SQLite for simplicity
# Change this to your database URL (e.g., PostgreSQL, MySQL, etc.)
DATABASE_URL = "sqlite+aiosqlite:///./example.db"

# Create database factory
factory = DatabaseFactory(
    database_url=DATABASE_URL,
    use_async=True,
    base=Base,
    echo=True,  # Set to False in production
)

# Get session maker (async or sync depending on use_async)
AsyncSessionLocal = factory.get_session_maker()

# Get engine for creating tables
engine = factory.get_engine()

# FastAPI dependency for getting database session
get_db = get_async_db(AsyncSessionLocal)


async def init_db() -> None:
    """Initialize database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()


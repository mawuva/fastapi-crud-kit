from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from fastapi_crud_kit.database.context import ReadOnlyAsync, TransactionAsync
from .base import CRUDManager


class AsyncCRUDManager(CRUDManager):
    """
    CRUD manager for asynchronous SQLAlchemy sessions.
    
    Executes async database operations directly without blocking the event loop.
    Uses context managers for read-only operations and transactions.
    """
    
    async def list(self, session: AsyncSession, query: Select[Any]):
        """Execute async query with read-only context."""
        async with ReadOnlyAsync(session):
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get(self, session: AsyncSession, query: Select[Any]):
        """Execute async query and return single result with read-only context."""
        async with ReadOnlyAsync(session):
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    async def _flush_and_refresh(self, session: AsyncSession, obj: Any) -> None:
        """
        Flush changes to database and refresh object to get updated values.
        
        Args:
            session: AsyncSession instance
            obj: Model instance to flush and refresh
        """
        await session.flush()
        await session.refresh(obj)
    
    async def create(self, session: AsyncSession, obj: Any):
        """Create async with transaction context."""
        async with TransactionAsync(session, commit=True):
            session.add(obj)
            await self._flush_and_refresh(session, obj)
            return obj
    
    async def update(self, session: AsyncSession, obj: Any):
        """Update async with transaction context."""
        async with TransactionAsync(session, commit=True):
            await self._flush_and_refresh(session, obj)
            return obj
    
    async def delete(self, session: AsyncSession, obj: Any):
        """Delete async with transaction context."""
        async with TransactionAsync(session, commit=True):
            await session.delete(obj)
            return obj


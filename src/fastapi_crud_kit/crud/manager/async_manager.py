from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from .base import CRUDManager


class AsyncCRUDManager(CRUDManager):
    """
    CRUD manager for asynchronous SQLAlchemy sessions.
    
    Executes async database operations directly without blocking the event loop.
    """
    
    async def list(self, session: AsyncSession, query: Select[Any]):
        """Execute async query."""
        result = await session.execute(query)
        return result.scalars().all()


import asyncio
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import Select
from .base import CRUDManager


class SyncCRUDManager(CRUDManager):
    """
    CRUD manager for synchronous SQLAlchemy sessions.
    
    Executes sync database operations in a thread pool to avoid blocking
    the event loop when used in async contexts.
    """
    
    async def list(self, session: Session, query: Select[Any]):
        """Execute sync query in thread pool."""
        return await asyncio.to_thread(self._execute_sync, session, query)
    
    def _execute_sync(self, session: Session, query: Select[Any]) -> list[Any]:
        """
        Private method to execute a synchronous database query.
        
        Args:
            session: Synchronous SQLAlchemy session
            query: Select statement to execute
            
        Returns:
            List of results from the query
        """
        result = session.execute(query)
        return result.scalars().all()

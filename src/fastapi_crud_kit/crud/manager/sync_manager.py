import asyncio
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import Select

from fastapi_crud_kit.database.context import ReadOnlySync, TransactionSync
from .base import CRUDManager


class SyncCRUDManager(CRUDManager):
    """
    CRUD manager for synchronous SQLAlchemy sessions.
    
    Executes sync database operations in a thread pool to avoid blocking
    the event loop when used in async contexts.
    Uses context managers for read-only operations and transactions.
    """
    
    async def list(self, session: Session, query: Select[Any]):
        """Execute sync query in thread pool with read-only context."""
        return await asyncio.to_thread(self._execute_sync, session, query)
    
    async def get(self, session: Session, query: Select[Any]):
        """Execute sync query and return single result in thread pool with read-only context."""
        return await asyncio.to_thread(self._get_sync, session, query)
    
    async def create(self, session: Session, obj: Any):
        """Create sync in thread pool with transaction context."""
        return await asyncio.to_thread(self._create_sync, session, obj)
    
    async def update(self, session: Session, obj: Any):
        """Update sync in thread pool with transaction context."""
        return await asyncio.to_thread(self._update_sync, session, obj)
    
    async def delete(self, session: Session, obj: Any):
        """Delete sync in thread pool with transaction context."""
        return await asyncio.to_thread(self._delete_sync, session, obj)
    
    def _execute_sync(self, session: Session, query: Select[Any]) -> list[Any]:
        """
        Private method to execute a synchronous database query with read-only context.
        
        Args:
            session: Synchronous SQLAlchemy session
            query: Select statement to execute
            
        Returns:
            List of results from the query
        """
        with ReadOnlySync(session):
            result = session.execute(query)
            return result.scalars().all()
    
    def _get_sync(self, session: Session, query: Select[Any]) -> Any:
        """Private method to get a single result with read-only context."""
        with ReadOnlySync(session):
            result = session.execute(query)
            return result.scalar_one_or_none()
    
    def _flush_and_refresh(self, session: Session, obj: Any) -> None:
        """
        Flush changes to database and refresh object to get updated values.
        
        Args:
            session: Session instance
            obj: Model instance to flush and refresh
        """
        session.flush()
        session.refresh(obj)
    
    def _create_sync(self, session: Session, obj: Any) -> Any:
        """Private method to create a record with transaction context."""
        with TransactionSync(session, commit=True):
            session.add(obj)
            self._flush_and_refresh(session, obj)
            return obj
    
    def _update_sync(self, session: Session, obj: Any) -> Any:
        """Private method to update a record with transaction context."""
        with TransactionSync(session, commit=True):
            self._flush_and_refresh(session, obj)
            return obj
    
    def _delete_sync(self, session: Session, obj: Any) -> Any:
        """Private method to delete a record with transaction context."""
        with TransactionSync(session, commit=True):
            session.delete(obj)
            return obj

from abc import ABC, abstractmethod
from typing import Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class CRUDManager(ABC):
    """
    Abstract base class for CRUD managers.
    
    Provides a common interface for executing database queries with different
    session types (async or sync).
    """
    
    @abstractmethod
    async def list(self, session: Union[AsyncSession, Session], query):
        """
        Execute a database query and return all results.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            query: Select statement to execute
            
        Returns:
            List of results from the query
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, session: Union[AsyncSession, Session], query):
        """
        Execute a database query and return a single result.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            query: Select statement to execute
            
        Returns:
            Single result or None if not found
        """
        raise NotImplementedError
    
    @abstractmethod
    async def create(self, session: Union[AsyncSession, Session], obj: Any):
        """
        Create a new database record.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            obj: Model instance to create
            
        Returns:
            Created model instance
        """
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, session: Union[AsyncSession, Session], obj: Any):
        """
        Update an existing database record.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            obj: Model instance to update
            
        Returns:
            Updated model instance
        """
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, session: Union[AsyncSession, Session], obj: Any):
        """
        Delete a database record.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            obj: Model instance to delete
            
        Returns:
            Deleted model instance
        """
        raise NotImplementedError
    
    
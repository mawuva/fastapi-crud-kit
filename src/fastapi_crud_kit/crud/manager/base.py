from abc import ABC, abstractmethod
from typing import Union
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
    
    
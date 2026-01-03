"""
Base class for CRUD operations.
"""

from typing import Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from fastapi_crud_kit.crud.manager import AsyncCRUDManager, SyncCRUDManager
from fastapi_crud_kit.query import QueryBuilder, QueryParams

ModelType = TypeVar("ModelType")


class CRUDBase:
    def __init__(self, model: Type[ModelType], use_async: bool | None = None):
        self.model = model
        
        if use_async is None:
            use_async = getattr(self, "use_async", True)
        self.use_async = use_async
        
        self.manager = AsyncCRUDManager() if use_async else SyncCRUDManager()
        
    def _build_query(self, query_params: QueryParams):
        """
        Build a query from query parameters.
        
        Args:
            query_params: Query parameters (filters, sort, include, fields)
            
        Returns:
            Select statement ready to execute
        """
        builder = QueryBuilder(self.model)
        return builder.apply(query_params)
    
    async def list(
        self, 
        session: Union[AsyncSession, Session], 
        query_params: QueryParams
    ):
        """
        List all items matching the query parameters.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            query_params: Query parameters (filters, sort, include, fields)
            
        Returns:
            List of results from the query
        """
        query = self._build_query(query_params)
        return await self.manager.list(session, query)
"""
Base class for CRUD operations.
"""

from typing import Any, Dict, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from fastapi_crud_kit.crud.manager import AsyncCRUDManager, SyncCRUDManager
from fastapi_crud_kit.database.exceptions import NotFoundError, ValidationError
from fastapi_crud_kit.query import QueryBuilder, QueryParams, FilterSchema

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


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
    
    async def get(
        self,
        session: Union[AsyncSession, Session],
        id: Any,
        query_params: QueryParams | None = None
    ):
        """
        Get a single item by ID.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            id: Primary key value (id or uuid depending on model)
            query_params: Optional query parameters (for includes, fields)
            
        Returns:
            Model instance or None if not found
        """
        # Determine the primary key field name
        # Try 'id' first, then 'uuid'
        pk_field = "id" if hasattr(self.model, "id") else "uuid"
        
        # Build query with id filter
        filters = [FilterSchema(field=pk_field, operator="eq", value=id)]
        if query_params:
            # Merge with existing filters if provided
            filters = filters + query_params.filters
            query_params = QueryParams(
                filters=filters,
                sort=query_params.sort,
                include=query_params.include,
                fields=query_params.fields
            )
        else:
            query_params = QueryParams(filters=filters)
        
        query = self._build_query(query_params)
        return await self.manager.get(session, query)
    
    async def create(
        self,
        session: Union[AsyncSession, Session],
        obj_in: Dict[str, Any] | Any
    ):
        """
        Create a new item.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            obj_in: Dictionary with data or model instance
            
        Returns:
            Created model instance
            
        Raises:
            ValidationError: If the creation data is invalid
        """
        try:
            if isinstance(obj_in, dict):
                obj = self.model(**obj_in)
            else:
                obj = obj_in
        except Exception as e:
            model_name = self.model.__name__
            raise ValidationError(
                f"Failed to create {model_name}: {str(e)}",
                field=None
            ) from e
        
        return await self.manager.create(session, obj)
    
    async def update(
        self,
        session: Union[AsyncSession, Session],
        id: Any,
        obj_in: Dict[str, Any] | Any
    ):
        """
        Update an existing item.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            id: Primary key value (id or uuid depending on model)
            obj_in: Dictionary with data to update or model instance
            
        Returns:
            Updated model instance
            
        Raises:
            NotFoundError: If the object with the given id is not found
            ValidationError: If the update data is invalid
        """
        # Get existing object
        db_obj = await self.get(session, id)
        if db_obj is None:
            model_name = self.model.__name__
            raise NotFoundError(model_name, id)
        
        # Update object
        try:
            if isinstance(obj_in, dict):
                for key, value in obj_in.items():
                    if hasattr(db_obj, key):
                        setattr(db_obj, key, value)
            else:
                # If obj_in is a model instance, copy its attributes
                for key in dir(obj_in):
                    if not key.startswith("_") and hasattr(db_obj, key):
                        value = getattr(obj_in, key)
                        if value is not None:
                            setattr(db_obj, key, value)
        except Exception as e:
            raise ValidationError(f"Failed to update object: {str(e)}") from e
        
        return await self.manager.update(session, db_obj)
    
    async def delete(
        self,
        session: Union[AsyncSession, Session],
        id: Any
    ):
        """
        Delete an item.
        
        Args:
            session: SQLAlchemy session (AsyncSession or Session)
            id: Primary key value (id or uuid depending on model)
            
        Returns:
            Deleted model instance
            
        Raises:
            NotFoundError: If the object with the given id is not found
        """
        db_obj = await self.get(session, id)
        if db_obj is None:
            model_name = self.model.__name__
            raise NotFoundError(model_name, id)
        
        return await self.manager.delete(session, db_obj)
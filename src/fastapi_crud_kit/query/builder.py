from typing import Type, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import load_only, selectinload
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select

from .schema import FilterSchema, QueryParams

class QueryBuilder:
    OPERATOR_MAP = {
        "eq": lambda col, val: col == val,
        "ne": lambda col, val: col != val,
        "lt": lambda col, val: col < val,
        "lte": lambda col, val: col <= val,
        "gt": lambda col, val: col > val,
        "gte": lambda col, val: col >= val,
        "like": lambda col, val: col.like(val),
        "ilike": lambda col, val: col.ilike(val),
        "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
    }
    
    def __init__(self, session: Session, model: Type[Any]):
        self.session = session
        self.model = model
        self.query: Query[Any] = session.query(model)
        
    def apply_filters(self, filters: list[FilterSchema]) -> "QueryBuilder":
        for f in filters:
            column: InstrumentedAttribute | None = getattr(self.model, f.field, None)
            if column is None:
                continue

            operator = self.OPERATOR_MAP.get(f.operator)
            if not operator:
                continue

            self.query = self.query.filter(operator(column, f.value))

        return self
    
    def apply_sort(self, sort: list[str]) -> "QueryBuilder":
        order_by = []

        for s in sort:
            desc = s.startswith("-")
            field = s[1:] if desc else s

            column = getattr(self.model, field, None)
            if column is None:
                continue

            order_by.append(column.desc() if desc else column.asc())

        if order_by:
            self.query = self.query.order_by(*order_by)

        return self

    def apply_fields(self, fields: list[str]) -> "QueryBuilder":
        if not fields:
            return self

        columns = [getattr(self.model, f) for f in fields if hasattr(self.model, f)]
        if columns:
            self.query = self.query.options(load_only(*columns))

        return self
    
    def apply_includes(self, includes: list[str]) -> "QueryBuilder":
        if not includes:
            return self
        
        inspector = inspect(self.model)
        relationships = {rel.key: rel for rel in inspector.relationships}
        
        options = []
        for include in includes:
            if include in relationships:
                options.append(selectinload(getattr(self.model, include)))
        
        if options:
            self.query = self.query.options(*options)
        
        return self
    
    def apply(self, params: QueryParams) -> Query[Any]:
        return (
            self
            .apply_filters(params.filters)
            .apply_sort(params.sort)
            .apply_fields(params.fields)
            .apply_includes(params.include)
            .query
        )


class AsyncQueryBuilder:
    """
    Query builder for asynchronous SQLAlchemy sessions.
    
    Uses the modern select() API instead of session.query().
    """
    OPERATOR_MAP = {
        "eq": lambda col, val: col == val,
        "ne": lambda col, val: col != val,
        "lt": lambda col, val: col < val,
        "lte": lambda col, val: col <= val,
        "gt": lambda col, val: col > val,
        "gte": lambda col, val: col >= val,
        "like": lambda col, val: col.like(val),
        "ilike": lambda col, val: col.ilike(val),
        "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
    }
    
    def __init__(self, session: AsyncSession, model: Type[Any]):
        self.session = session
        self.model = model
        self.statement: Select[Any] = select(model)
        
    def apply_filters(self, filters: list[FilterSchema]) -> "AsyncQueryBuilder":
        for f in filters:
            column: InstrumentedAttribute | None = getattr(self.model, f.field, None)
            if column is None:
                continue

            operator = self.OPERATOR_MAP.get(f.operator)
            if not operator:
                continue

            self.statement = self.statement.filter(operator(column, f.value))

        return self
    
    def apply_sort(self, sort: list[str]) -> "AsyncQueryBuilder":
        order_by = []

        for s in sort:
            desc = s.startswith("-")
            field = s[1:] if desc else s

            column = getattr(self.model, field, None)
            if column is None:
                continue

            order_by.append(column.desc() if desc else column.asc())

        if order_by:
            self.statement = self.statement.order_by(*order_by)

        return self

    def apply_fields(self, fields: list[str]) -> "AsyncQueryBuilder":
        if not fields:
            return self

        columns = [getattr(self.model, f) for f in fields if hasattr(self.model, f)]
        if columns:
            # For async, load_only() works with select() in SQLAlchemy 2.0+
            self.statement = self.statement.options(load_only(*columns))

        return self
    
    def apply_includes(self, includes: list[str]) -> "AsyncQueryBuilder":
        if not includes:
            return self
        
        inspector = inspect(self.model)
        relationships = {rel.key: rel for rel in inspector.relationships}
        
        options = []
        for include in includes:
            if include in relationships:
                options.append(selectinload(getattr(self.model, include)))
        
        if options:
            self.statement = self.statement.options(*options)
        
        return self
    
    def apply(self, params: QueryParams) -> Select[Any]:
        """
        Apply all query parameters and return a Select statement.
        
        The returned statement can be executed with:
            result = await session.execute(statement)
            items = result.scalars().all()
        """
        return (
            self
            .apply_filters(params.filters)
            .apply_sort(params.sort)
            .apply_fields(params.fields)
            .apply_includes(params.include)
            .statement
        )


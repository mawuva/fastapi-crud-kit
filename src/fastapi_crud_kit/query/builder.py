from typing import Any, Type

from sqlalchemy import Select, inspect, select
from sqlalchemy.orm import selectinload

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

    def __init__(self, model: Type[Any]):
        self.model = model
        self.query: Select[Any] = select(model)

    def apply_filters(self, filters: list[FilterSchema]) -> "QueryBuilder":
        for f in filters:
            col = getattr(self.model, f.field, None)
            if col is None:
                continue

            op = self.OPERATOR_MAP.get(f.operator)
            if not op:
                continue

            self.query = self.query.where(op(col, f.value))
        return self

    def apply_sort(self, sort: list[str]) -> "QueryBuilder":
        for s in sort:
            desc = s.startswith("-")
            field = s[1:] if desc else s

            col = getattr(self.model, field, None)
            if col is None:
                continue

            self.query = self.query.order_by(col.desc() if desc else col.asc())
        return self

    def apply_fields(self, fields: list[str]) -> "QueryBuilder":
        if not fields:
            return self

        columns = [getattr(self.model, f) for f in fields if hasattr(self.model, f)]
        if columns:
            self.query = self.query.with_only_columns(*columns)

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

    def apply(self, params: QueryParams) -> Select[Any]:
        return (
            self.apply_filters(params.filters)
            .apply_sort(params.sort)
            .apply_fields(params.fields)
            .apply_includes(params.include)
            .query
        )

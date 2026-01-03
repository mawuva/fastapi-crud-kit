from typing import Any, Optional, Type

from sqlalchemy import Select, inspect, select
from sqlalchemy.orm import selectinload

from .config import QueryBuilderConfig
from .filters.validator import FilterValidator
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

    def __init__(
        self, model: Type[Any], config: Optional[QueryBuilderConfig] = None
    ) -> None:
        """
        Initialize QueryBuilder.

        Args:
            model: SQLAlchemy model class
            config: Optional QueryBuilderConfig for filter validation
        """
        self.model = model
        self.config = config
        self.query: Select[Any] = select(model)

    def apply_filters(self, filters: list[FilterSchema]) -> "QueryBuilder":
        """
        Apply filters to the query.

        If a QueryBuilderConfig is provided, filters are validated before application.
        Custom callbacks from AllowedFilters are used if available.

        Args:
            filters: List of FilterSchema to apply

        Returns:
            Self for method chaining
        """
        # Validate filters if config is provided
        if self.config:
            validator = FilterValidator(self.config)
            filters = validator.validate(filters)

        for f in filters:
            # Check if there's a custom callback for this filter
            if self.config:
                allowed_filter = self.config.get_allowed_filter(f.field)
                if allowed_filter and allowed_filter.callback:
                    # Use custom callback: callback(query, value) -> query
                    self.query = allowed_filter.callback(self.query, f.value)
                    continue

            # Use standard operator-based filtering
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

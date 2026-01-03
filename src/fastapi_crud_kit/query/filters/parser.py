"""
Query string parser for filters.

This module provides functionality to parse filter query parameters
from the format: filter[field][operator]=value
"""

from __future__ import annotations

import re
from collections import defaultdict
from urllib.parse import parse_qs, unquote

from fastapi import Request

from .schema import FilterSchema
from .operators import FilterOperator


def parse_filter_params(request: Request) -> list[FilterSchema]:
    """
    Parse filter parameters from query string.

    Supports the format: filter[field][operator]=value
    If operator is not specified, defaults to 'eq'.

    Examples:
        - filter[name][eq]=John -> FilterSchema(field="name", operator="eq", value="John")
        - filter[age][gt]=18 -> FilterSchema(field="age", operator="gt", value="18")
        - filter[status]=active -> FilterSchema(field="status", operator="eq", value="active")
        - filter[id][in]=1,2,3 -> FilterSchema(field="id", operator="in", value=["1", "2", "3"])

    Args:
        request: FastAPI Request object containing query parameters

    Returns:
        List of FilterSchema objects parsed from the query string

    Raises:
        ValueError: If a filter parameter has invalid format
    """
    # Parse query string to handle multiple values properly
    query_string = str(request.url.query)
    parsed_params = parse_qs(query_string, keep_blank_values=True)

    filters: list[FilterSchema] = []

    # Pattern to match filter[field][operator] or filter[field]
    filter_pattern = re.compile(r"^filter\[([^\]]+)\](\[([^\]]+)\])?$")

    # Group filters by field and operator
    filter_groups: dict[tuple[str, str], list[str]] = defaultdict(list)

    for key, values in parsed_params.items():
        match = filter_pattern.match(key)
        if not match:
            continue

        field = unquote(match.group(1))
        operator_group = match.group(3)

        # If operator is not specified, use default (eq)
        operator = operator_group if operator_group else FilterOperator.default()

        # Collect all values for this filter
        for value in values:
            filter_groups[(field, operator)].append(unquote(value))

    # Build FilterSchema objects
    for (field, operator), values in filter_groups.items():
        # Handle multiple values
        if len(values) > 1:
            # If multiple values and operator not explicitly set, use 'in'
            if operator == FilterOperator.default():
                operator = FilterOperator.IN.value
            filter_value = values
        else:
            filter_value = values[0]

        # Special handling for null checks
        if operator in (FilterOperator.IS_NULL.value, FilterOperator.IS_NOT_NULL.value):
            # For null checks, value should be boolean-like
            filter_value = str(filter_value).lower() in ("true", "1", "yes")

        # Handle 'in' operator with comma-separated values
        if operator == FilterOperator.IN.value and isinstance(filter_value, str):
            # Split comma-separated values
            filter_value = [v.strip() for v in filter_value.split(",") if v.strip()]

        filters.append(
            FilterSchema(
                field=field,
                operator=operator,
                value=filter_value,
            )
        )

    return filters


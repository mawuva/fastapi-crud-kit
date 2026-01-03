"""
Filter validation and resolution.

This module provides functionality to validate and resolve raw filter parameters
into validated FilterSchema objects.
"""

from __future__ import annotations

from typing import Any

from fastapi_crud_kit.query.exceptions import (
    FilterNotAllowedError,
    FilterOperatorNotAllowedError,
)

from .allowed import AllowedFilter
from .operators import FilterOperator
from .schema import FilterSchema, RawFilterSchema


def resolve_and_validate_filters(
    raw_filters: list[RawFilterSchema],
    allowed_filters: dict[str, AllowedFilter] | None = None,
) -> list[FilterSchema]:
    """
    Resolve aliases, apply default operators, and validate filters.

    This function takes raw filter data from the parser and:
    1. Resolves aliases to actual field names
    2. Applies default operators when not specified
    3. Validates that filters and operators are allowed
    4. Normalizes values (multiple values, comma-separated, etc.)

    Args:
        raw_filters: List of raw filter schemas from the parser
        allowed_filters: Optional dictionary mapping filter names (aliases) to AllowedFilter
            instances. If provided, only filters in this dictionary are allowed and
            default operators are used when no operator is specified.

    Returns:
        List of validated FilterSchema objects

    Raises:
        FilterNotAllowedError: If a filter is not in the allowed_filters dictionary
        FilterOperatorNotAllowedError: If an operator is not allowed for a filter
    """
    if not allowed_filters:
        # No validation configured, use fallback behavior
        return _resolve_filters_without_validation(raw_filters)

    # Build lookup maps
    allowed_filters_by_alias: dict[str, AllowedFilter] = {}
    allowed_filters_by_field: dict[str, AllowedFilter] = {}
    for allowed_filter in allowed_filters.values():
        allowed_filters_by_alias[allowed_filter.alias] = allowed_filter
        allowed_filters_by_field[allowed_filter.field] = allowed_filter

    validated_filters: list[FilterSchema] = []

    for raw_filter in raw_filters:
        alias_or_field = raw_filter.alias_or_field
        explicit_operator = raw_filter.operator

        # Resolve the actual field name and get AllowedFilter
        allowed_filter: AllowedFilter | None = None
        actual_field: str = alias_or_field

        # Try to find by alias first, then by field name
        allowed_filter = allowed_filters_by_alias.get(alias_or_field)
        if allowed_filter:
            actual_field = allowed_filter.field
        else:
            # Try by field name
            allowed_filter = allowed_filters_by_field.get(alias_or_field)
            if allowed_filter:
                actual_field = alias_or_field
            else:
                # Filter not allowed
                allowed_filter_names = list(allowed_filters_by_alias.keys())
                raise FilterNotAllowedError(alias_or_field, allowed_filter_names)

        # Determine the operator to use
        if explicit_operator:
            # Operator explicitly specified in URL
            operator_str = explicit_operator
            # Validate that the operator is allowed
            if not allowed_filter.is_operator_allowed(operator_str):
                raise FilterOperatorNotAllowedError(
                    alias_or_field,
                    operator_str,
                    allowed_filter.get_allowed_operators(),
                )
        else:
            # No operator specified, use default
            operator_str = allowed_filter.get_default_operator()

        # Normalize values
        normalized_value = _normalize_filter_value(
            raw_filter.values, operator_str, explicit_operator is not None
        )

        validated_filters.append(
            FilterSchema(
                field=actual_field,
                operator=operator_str,
                value=normalized_value,
            )
        )

    return validated_filters


def _resolve_filters_without_validation(
    raw_filters: list[RawFilterSchema],
) -> list[FilterSchema]:
    """
    Resolve filters without validation (fallback behavior).

    Used when no allowed_filters are configured. Applies basic defaults.
    """
    resolved_filters: list[FilterSchema] = []

    for raw_filter in raw_filters:
        field = raw_filter.alias_or_field
        operator = raw_filter.operator or FilterOperator.default()

        # Normalize values
        normalized_value = _normalize_filter_value(
            raw_filter.values, operator, raw_filter.operator is not None
        )

        resolved_filters.append(
            FilterSchema(
                field=field,
                operator=operator,
                value=normalized_value,
            )
        )

    return resolved_filters


def _normalize_filter_value(
    values: list[str], operator: str, operator_was_explicit: bool
) -> Any:
    """
    Normalize filter values based on operator and number of values.

    Handles:
    - Multiple values (list)
    - Comma-separated values in a single string
    - Null checks (boolean conversion)
    - Type conversion based on operator
    """
    # Handle multiple values
    if len(values) > 1:
        # If multiple values and operator is default (eq), convert to 'in'
        if operator == FilterOperator.default() and not operator_was_explicit:
            operator = FilterOperator.IN.value
        filter_value = values
    else:
        filter_value = values[0]

    # Special handling for null checks
    if operator in (FilterOperator.IS_NULL.value, FilterOperator.IS_NOT_NULL.value):
        # For null checks, value should be boolean-like
        if isinstance(filter_value, list):
            filter_value = filter_value[0] if filter_value else "false"
        filter_value = str(filter_value).lower() in ("true", "1", "yes")
        return filter_value

    # Handle 'in' operator with comma-separated values
    if operator == FilterOperator.IN.value:
        if isinstance(filter_value, str):
            # Split comma-separated values
            filter_value = [v.strip() for v in filter_value.split(",") if v.strip()]
        elif isinstance(filter_value, list):
            # Already a list, but might contain comma-separated strings
            expanded_values = []
            for v in filter_value:
                if "," in v:
                    expanded_values.extend([v.strip() for v in v.split(",") if v.strip()])
                else:
                    expanded_values.append(v.strip())
            filter_value = expanded_values
        return filter_value

    # For other operators, return as-is (single value or list)
    return filter_value


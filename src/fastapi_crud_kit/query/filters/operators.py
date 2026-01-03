"""
Operators supported for filtering.

This module defines the available operators that can be used in query filters.
"""

from enum import Enum
from typing import Tuple


class FilterOperator(str, Enum):
    """Supported filter operators."""

    EQUAL = "eq"
    NOT_EQUAL = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    STARTS_WITH = "starts_with"
    ISTARTS_WITH = "istarts_with"
    ENDS_WITH = "ends_with"
    IENDS_WITH = "iends_with"
    IN = "in"
    NOT_IN = "nin"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    BETWEEN = "between"
    NOT_BETWEEN = "not_between"

    @classmethod
    def default(cls) -> str:
        """Return the default operator (equal)."""
        return cls.EQUAL.value

    @classmethod
    def get_all(cls) -> list[str]:
        """Return all operators."""
        return [op.value for op in cls]

    @classmethod
    def from_string(cls, value: str) -> "FilterOperator":
        """Return the operator from a string."""
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid operator: {value}. Supported operators: {cls.get_all()}")

    def numeric_operators(cls) -> Tuple["FilterOperator", ...]:
        """Return all numeric operators."""
        return (
            cls.GREATER_THAN,
            cls.GREATER_THAN_OR_EQUAL,
            cls.LESS_THAN,
            cls.LESS_THAN_OR_EQUAL
        )

    def comparison_operators(cls) -> Tuple["FilterOperator", ...]:
        """Return all comparison operators."""
        return (
            cls.EQUAL,
            cls.NOT_EQUAL,
            cls.GREATER_THAN,
            cls.GREATER_THAN_OR_EQUAL,
            cls.LESS_THAN,
            cls.LESS_THAN_OR_EQUAL
        )

    def string_operators(cls) -> Tuple["FilterOperator", ...]:
        """Return all string operators."""
        return (
            cls.CONTAINS,
            cls.ICONTAINS,
            cls.STARTS_WITH,
            cls.ISTARTS_WITH,
            cls.ENDS_WITH,
            cls.IENDS_WITH
        )

    def list_operators(cls) -> Tuple["FilterOperator", ...]:
        """Return all list operators."""
        return (
            cls.IN,
            cls.NOT_IN
        )

    def null_operators(cls) -> Tuple["FilterOperator", ...]:
        """Return all null operators."""
        return (
            cls.IS_NULL,
            cls.IS_NOT_NULL
        )

    def range_operators(cls) -> Tuple["FilterOperator", ...]:
        """Return all range operators."""
        return (
            cls.BETWEEN,
            cls.NOT_BETWEEN
        )


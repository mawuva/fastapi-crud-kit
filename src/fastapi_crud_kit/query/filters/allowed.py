"""
Allowed filter configuration.

This module provides the AllowedFilter class to configure which filters
are allowed and how they should behave (default operator, allowed operators, etc.).
"""

from __future__ import annotations

from typing import Any

from .operators import FilterOperator


class AllowedFilter:
    """
    Represents an allowed filter with its configuration.

    This class defines how a filter should behave when used in queries:
    - The default operator to use when no operator is specified
    - Which operators are allowed for this filter
    - Optional configuration like aliases, ignored values, etc.

    Examples:
        >>> # Simple filter with default operator
        >>> AllowedFilter.partial('name')
        >>> # Filter with explicit configuration
        >>> AllowedFilter('id', FilterOperator.EQUAL, [FilterOperator.EQUAL, FilterOperator.IN])
        >>> # Filter with alias
        >>> AllowedFilter.exact('name', 'user_passport_full_name')
    """

    def __init__(
        self,
        field: str,
        default_operator: FilterOperator | str,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
        alias: str | None = None,
    ) -> None:
        """
        Initialize an AllowedFilter.

        Args:
            field: The field name to filter on (database column name)
            default_operator: The default operator to use when no operator is specified
            allowed_operators: List of operators allowed for this filter.
                If None, only the default_operator is allowed.
            alias: Optional alias name for the filter (exposed name in URL).
                If None, uses the field name.

        Raises:
            ValueError: If default_operator is not in allowed_operators
        """
        self.field = field
        self.alias = alias or field

        # Normalize default_operator
        if isinstance(default_operator, str):
            self.default_operator = FilterOperator.from_string(default_operator)
        else:
            self.default_operator = default_operator

        # Normalize allowed_operators
        if allowed_operators is None:
            self.allowed_operators = [self.default_operator]
        else:
            self.allowed_operators = [
                FilterOperator.from_string(op) if isinstance(op, str) else op
                for op in allowed_operators
            ]

        # Validate that default_operator is in allowed_operators
        if self.default_operator not in self.allowed_operators:
            raise ValueError(
                f"Default operator '{self.default_operator.value}' must be in "
                f"allowed_operators: {[op.value for op in self.allowed_operators]}"
            )

    def is_operator_allowed(self, operator: FilterOperator | str) -> bool:
        """
        Check if an operator is allowed for this filter.

        Args:
            operator: The operator to check

        Returns:
            True if the operator is allowed, False otherwise
        """
        if isinstance(operator, str):
            try:
                operator = FilterOperator.from_string(operator)
            except ValueError:
                return False

        return operator in self.allowed_operators

    def get_default_operator(self) -> str:
        """Get the default operator as a string value."""
        return self.default_operator.value

    def get_allowed_operators(self) -> list[str]:
        """Get all allowed operators as string values."""
        return [op.value for op in self.allowed_operators]

    @classmethod
    def partial(
        cls,
        field: str,
        alias: str | None = None,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
    ) -> AllowedFilter:
        """
        Create a partial filter (case-insensitive contains).

        This is useful for text fields where you want to search for partial matches.
        Default operator: ICONTAINS

        Args:
            field: The field name
            alias: Optional alias for the filter
            allowed_operators: Optional list of allowed operators.
                Defaults to [ICONTAINS, CONTAINS, STARTS_WITH, ENDS_WITH, EQ]

        Returns:
            AllowedFilter configured for partial matching
        """
        if allowed_operators is None:
            allowed_operators = [
                FilterOperator.ICONTAINS,
                FilterOperator.CONTAINS,
                FilterOperator.STARTS_WITH,
                FilterOperator.ISTARTS_WITH,
                FilterOperator.ENDS_WITH,
                FilterOperator.IENDS_WITH,
                FilterOperator.EQUAL,
            ]

        return cls(
            field=field,
            default_operator=FilterOperator.ICONTAINS,
            allowed_operators=allowed_operators,
            alias=alias,
        )

    @classmethod
    def exact(
        cls,
        field: str,
        alias: str | None = None,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
    ) -> AllowedFilter:
        """
        Create an exact filter (equality).

        This is useful for IDs, enums, or fields requiring exact matches.
        Default operator: EQUAL

        Args:
            field: The field name
            alias: Optional alias for the filter
            allowed_operators: Optional list of allowed operators.
                Defaults to [EQUAL, NOT_EQUAL, IN, NOT_IN]

        Returns:
            AllowedFilter configured for exact matching
        """
        if allowed_operators is None:
            allowed_operators = [
                FilterOperator.EQUAL,
                FilterOperator.NOT_EQUAL,
                FilterOperator.IN,
                FilterOperator.NOT_IN,
            ]

        return cls(
            field=field,
            default_operator=FilterOperator.EQUAL,
            allowed_operators=allowed_operators,
            alias=alias,
        )

    @classmethod
    def begins_with(
        cls,
        field: str,
        alias: str | None = None,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
    ) -> AllowedFilter:
        """
        Create a begins-with filter (starts with value).

        Default operator: ISTARTS_WITH

        Args:
            field: The field name
            alias: Optional alias for the filter
            allowed_operators: Optional list of allowed operators

        Returns:
            AllowedFilter configured for begins-with matching
        """
        if allowed_operators is None:
            allowed_operators = [
                FilterOperator.ISTARTS_WITH,
                FilterOperator.STARTS_WITH,
                FilterOperator.ICONTAINS,
                FilterOperator.CONTAINS,
                FilterOperator.EQUAL,
            ]

        return cls(
            field=field,
            default_operator=FilterOperator.ISTARTS_WITH,
            allowed_operators=allowed_operators,
            alias=alias,
        )

    @classmethod
    def ends_with(
        cls,
        field: str,
        alias: str | None = None,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
    ) -> AllowedFilter:
        """
        Create an ends-with filter (ends with value).

        Default operator: IENDS_WITH

        Args:
            field: The field name
            alias: Optional alias for the filter
            allowed_operators: Optional list of allowed operators

        Returns:
            AllowedFilter configured for ends-with matching
        """
        if allowed_operators is None:
            allowed_operators = [
                FilterOperator.IENDS_WITH,
                FilterOperator.ENDS_WITH,
                FilterOperator.ICONTAINS,
                FilterOperator.CONTAINS,
                FilterOperator.EQUAL,
            ]

        return cls(
            field=field,
            default_operator=FilterOperator.IENDS_WITH,
            allowed_operators=allowed_operators,
            alias=alias,
        )

    @classmethod
    def operator(
        cls,
        field: str,
        default_operator: FilterOperator | str,
        allowed_operators: list[FilterOperator] | list[str] | None = None,
        alias: str | None = None,
    ) -> AllowedFilter:
        """
        Create a filter with a specific operator configuration.

        This is useful for numeric fields, dates, or custom operator requirements.

        Args:
            field: The field name
            default_operator: The default operator to use
            allowed_operators: Optional list of allowed operators.
                If None, only the default_operator is allowed.
            alias: Optional alias for the filter

        Returns:
            AllowedFilter with the specified operator configuration

        Examples:
            >>> # Numeric field with comparison operators
            >>> AllowedFilter.operator(
            ...     'salary',
            ...     FilterOperator.GREATER_THAN,
            ...     [FilterOperator.GT, FilterOperator.GTE, FilterOperator.LT, FilterOperator.LTE, FilterOperator.EQ]
            ... )
            >>> # Date field
            >>> AllowedFilter.operator('created_at', FilterOperator.EQUAL, [FilterOperator.EQ, FilterOperator.GT, FilterOperator.LT])
        """
        return cls(
            field=field,
            default_operator=default_operator,
            allowed_operators=allowed_operators,
            alias=alias,
        )

    def __repr__(self) -> str:
        """String representation of the filter."""
        return (
            f"AllowedFilter(field='{self.field}', "
            f"alias='{self.alias}', "
            f"default_operator='{self.default_operator.value}', "
            f"allowed_operators={[op.value for op in self.allowed_operators]})"
        )

    def __eq__(self, other: Any) -> bool:
        """Check equality with another AllowedFilter."""
        if not isinstance(other, AllowedFilter):
            return False
        return (
            self.field == other.field
            and self.alias == other.alias
            and self.default_operator == other.default_operator
            and set(self.allowed_operators) == set(other.allowed_operators)
        )


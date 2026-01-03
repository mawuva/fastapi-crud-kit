"""Custom exceptions for query building and filtering."""


class QueryBuilderError(Exception):
    """Base exception for query builder errors."""

    pass


class FilterValidationError(QueryBuilderError):
    """Exception raised when a filter validation fails."""

    def __init__(self, message: str, field: str) -> None:
        """
        Initialize filter validation error.

        Args:
            message: Error message
            field: Field name that caused the error
        """
        self.field = field
        super().__init__(message)


class FilterValueTypeError(QueryBuilderError):
    """Exception raised when a filter value type is invalid for the operator."""

    def __init__(self, message: str, field: str, operator: str, value: any) -> None:
        """
        Initialize filter value type error.

        Args:
            message: Error message
            field: Field name
            operator: Operator that was used
            value: Invalid value
        """
        self.field = field
        self.operator = operator
        self.value = value
        super().__init__(message)


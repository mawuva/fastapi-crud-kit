"""
Exceptions for query parsing and validation.
"""


class FilterNotAllowedError(ValueError):
    """Raised when a filter is not in the allowed filters list."""

    def __init__(self, filter_name: str, allowed_filters: list[str] | None = None) -> None:
        message = f"Filter '{filter_name}' is not allowed."
        if allowed_filters:
            message += f" Allowed filters: {', '.join(allowed_filters)}"
        super().__init__(message)
        self.filter_name = filter_name
        self.allowed_filters = allowed_filters


class FilterOperatorNotAllowedError(ValueError):
    """Raised when an operator is not allowed for a filter."""

    def __init__(
        self, filter_name: str, operator: str, allowed_operators: list[str] | None = None
    ) -> None:
        message = f"Operator '{operator}' is not allowed for filter '{filter_name}'."
        if allowed_operators:
            message += f" Allowed operators: {', '.join(allowed_operators)}"
        super().__init__(message)
        self.filter_name = filter_name
        self.operator = operator
        self.allowed_operators = allowed_operators


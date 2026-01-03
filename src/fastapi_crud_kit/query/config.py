"""
Configuration for query parsing.

This module provides a configuration class to centralize query parsing settings.
"""

from __future__ import annotations

from .filters import AllowedFilter


class QueryConfig:
    """
    Configuration for query parsing.

    This class centralizes all configuration options for query parsing,
    including allowed filters, sorting options, field selection, etc.
    """

    def __init__(
        self,
        allowed_filters: dict[str, AllowedFilter] | None = None,
    ) -> None:
        """
        Initialize QueryConfig.

        Args:
            allowed_filters: Optional dictionary mapping filter names to AllowedFilter
                instances. If provided, filters will be validated and resolved.
        """
        self.allowed_filters = allowed_filters or {}

    def has_allowed_filters(self) -> bool:
        """Check if any allowed filters are configured."""
        return bool(self.allowed_filters)

    def get_allowed_filters(self) -> dict[str, AllowedFilter]:
        """Get the allowed filters dictionary."""
        return self.allowed_filters


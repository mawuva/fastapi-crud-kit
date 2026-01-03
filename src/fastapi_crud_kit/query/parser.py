"""
Query parser for FastAPI.

This module provides a minimal QueryParser that can be used as a FastAPI dependency.
"""

from __future__ import annotations

from fastapi import Request

from .config import QueryConfig
from .filters import FilterSchema, parse_filter_params, resolve_and_validate_filters


class QueryParser:
    """
    Minimal query parser for FastAPI routes.

    This parser handles filter query parameters and can be extended
    to support sort, include, and fields in the future.
    """

    def __init__(self, config: QueryConfig | None = None) -> None:
        """
        Initialize QueryParser.

        Args:
            config: Optional QueryConfig instance. If None, uses default config
                (no validation, no allowed filters).
        """
        self.config = config or QueryConfig()

    def __call__(self, request: Request) -> QueryParams:
        """
        Parse query parameters from the request.

        Args:
            request: FastAPI Request object

        Returns:
            QueryParams object containing parsed query parameters
        """
        # Parse raw filters from URL
        raw_filters = parse_filter_params(request)

        # Resolve and validate if config has allowed_filters
        if self.config.has_allowed_filters():
            filters = resolve_and_validate_filters(
                raw_filters, self.config.get_allowed_filters()
            )
        else:
            filters = resolve_and_validate_filters(raw_filters, None)

        return QueryParams(filters=filters)


class QueryParams:
    """Container for parsed query parameters."""

    def __init__(self, filters: list[FilterSchema]) -> None:
        """
        Initialize QueryParams.

        Args:
            filters: List of FilterSchema objects parsed from query string
        """
        self.filters = filters

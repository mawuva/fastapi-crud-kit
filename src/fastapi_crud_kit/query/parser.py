"""
Query parser for FastAPI.

This module provides a minimal QueryParser that can be used as a FastAPI dependency.
"""

from __future__ import annotations

from fastapi import Request

from .filters import FilterSchema, parse_filter_params


class QueryParser:
    """
    Minimal query parser for FastAPI routes.

    This parser handles filter query parameters and can be extended
    to support sort, include, and fields in the future.
    """

    def __call__(self, request: Request) -> QueryParams:
        """
        Parse query parameters from the request.

        Args:
            request: FastAPI Request object

        Returns:
            QueryParams object containing parsed query parameters
        """
        return QueryParams(
            filters=parse_filter_params(request),
        )


class QueryParams:
    """Container for parsed query parameters."""

    def __init__(self, filters: list[FilterSchema]) -> None:
        """
        Initialize QueryParams.

        Args:
            filters: List of FilterSchema objects parsed from query string
        """
        self.filters = filters

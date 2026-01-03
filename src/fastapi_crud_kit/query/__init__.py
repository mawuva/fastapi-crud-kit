"""
Query string parsing utilities for FastAPI.

This module provides tools to parse and validate query string parameters,
particularly for filtering, sorting, and field selection.
"""

from .config import QueryConfig
from .dependencies import create_query_parser_dependency, get_query_parser
from .exceptions import FilterNotAllowedError, FilterOperatorNotAllowedError
from .filters import (
    AllowedFilter,
    FilterSchema,
    FilterOperator,
    RawFilterSchema,
    parse_filter_params,
    resolve_and_validate_filters,
)
from .parser import QueryParams, QueryParser

__all__ = [
    "AllowedFilter",
    "FilterNotAllowedError",
    "FilterOperatorNotAllowedError",
    "FilterSchema",
    "FilterOperator",
    "QueryConfig",
    "QueryParams",
    "QueryParser",
    "RawFilterSchema",
    "create_query_parser_dependency",
    "get_query_parser",
    "parse_filter_params",
    "resolve_and_validate_filters",
]

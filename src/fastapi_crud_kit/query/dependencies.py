"""
FastAPI dependencies for query parsing.

This module provides FastAPI dependency functions to easily integrate
query parsing into routes.
"""

from fastapi import Request

from .config import QueryConfig
from .parser import QueryParams, QueryParser


def get_query_parser(request: Request) -> QueryParams:
    """
    FastAPI dependency to parse query parameters from the request.

    This function parses query parameters from the request and returns
    a QueryParams object containing the parsed filters, sort, include, etc.

    Uses default config (no validation, no allowed filters).

    Args:
        request: FastAPI Request object

    Returns:
        QueryParams object containing parsed query parameters

    Example:
        >>> from fastapi_crud_kit.query import get_query_parser, QueryParams
        >>>
        >>> @router.get("/items")
        >>> async def list_items(
        ...     query: QueryParams = Depends(get_query_parser)
        ... ):
        ...     filters = query.filters
        ...     return {"items": []}
    """
    parser = QueryParser()
    return parser(request)


def create_query_parser_dependency(config: QueryConfig):
    """
    Create a FastAPI dependency function with a specific QueryConfig.

    This is useful when you want to use different configurations for different routes.

    Args:
        config: QueryConfig instance to use for parsing

    Returns:
        A dependency function that can be used with FastAPI's Depends()

    Example:
        >>> from fastapi_crud_kit.query import QueryConfig, AllowedFilter, create_query_parser_dependency
        >>>
        >>> config = QueryConfig(allowed_filters={
        ...     'name': AllowedFilter.partial('name'),
        ...     'id': AllowedFilter.exact('id'),
        ... })
        >>>
        >>> @router.get("/items")
        >>> async def list_items(
        ...     query: QueryParams = Depends(create_query_parser_dependency(config))
        ... ):
        ...     filters = query.filters
        ...     return {"items": []}
    """
    parser = QueryParser(config=config)

    def dependency(request: Request) -> QueryParams:
        return parser(request)

    return dependency


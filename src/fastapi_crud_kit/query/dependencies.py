"""
FastAPI dependencies for query parsing.

This module provides FastAPI dependency functions to easily integrate
query parsing into routes.
"""

from fastapi import Request

from .parser import QueryParams, QueryParser


def get_query_parser(request: Request) -> QueryParams:
    """
    FastAPI dependency to parse query parameters from the request.

    This function parses query parameters from the request and returns
    a QueryParams object containing the parsed filters, sort, include, etc.

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


"""
Query string parser for filters.

This module provides functionality to parse filter query parameters
from the format: filter[field][operator]=value

This is a pure parser that extracts raw data from the URL without validation.
Use the validator module to validate and resolve the parsed filters.
"""

from __future__ import annotations

import re
from collections import defaultdict
from urllib.parse import parse_qs, unquote

from fastapi import Request

from .schema import RawFilterSchema


def parse_filter_params(request: Request) -> list[RawFilterSchema]:
    """
    Parse filter parameters from query string (pure parsing, no validation).

    This function extracts raw filter data from the URL without any validation
    or resolution. It returns RawFilterSchema objects that can then be validated
    and resolved using the validator module.

    Supports the format: filter[field][operator]=value

    Examples:
        - filter[name][eq]=John -> RawFilterSchema(alias_or_field="name", operator="eq", values=["John"])
        - filter[age][gt]=18 -> RawFilterSchema(alias_or_field="age", operator="gt", values=["18"])
        - filter[status]=active -> RawFilterSchema(alias_or_field="status", operator=None, values=["active"])
        - filter[id][in]=1,2,3 -> RawFilterSchema(alias_or_field="id", operator="in", values=["1,2,3"])

    Args:
        request: FastAPI Request object containing query parameters

    Returns:
        List of RawFilterSchema objects parsed from the query string

    Raises:
        ValueError: If a filter parameter has invalid format
    """
    # Parse query string to handle multiple values properly
    query_string = str(request.url.query)
    parsed_params = parse_qs(query_string, keep_blank_values=True)

    raw_filters: list[RawFilterSchema] = []

    # Pattern to match filter[field][operator] or filter[field]
    filter_pattern = re.compile(r"^filter\[([^\]]+)\](\[([^\]]+)\])?$")

    # Group filters by field/alias and operator
    filter_groups: dict[tuple[str, str | None], list[str]] = defaultdict(list)

    for key, values in parsed_params.items():
        match = filter_pattern.match(key)
        if not match:
            continue

        alias_or_field = unquote(match.group(1))
        operator_group = match.group(3)
        operator = unquote(operator_group) if operator_group else None

        # Collect all values for this filter (preserve original values)
        for value in values:
            filter_groups[(alias_or_field, operator)].append(unquote(value))

    # Build RawFilterSchema objects
    for (alias_or_field, operator), values in filter_groups.items():
        raw_filters.append(
            RawFilterSchema(
                alias_or_field=alias_or_field,
                operator=operator,
                values=values,
            )
        )

    return raw_filters


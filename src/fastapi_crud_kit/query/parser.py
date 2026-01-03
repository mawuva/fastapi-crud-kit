import re
from typing import List, Mapping

from .schema import FilterSchema, QueryParams
from .utils import split_comma_separated

FILTER_REGEX = re.compile(r"^filter\[(?P<field>[^\]]+)\](?:\[(?P<operator>[^\]]+)\])?$")


def parse_filters(query_params: Mapping[str, str]) -> List[FilterSchema]:
    filters: list[FilterSchema] = []

    for key, value in query_params.items():
        match = FILTER_REGEX.match(key)
        if not match:
            continue

        filters.append(
            FilterSchema(
                field=match.group("field"),
                operator=match.group("operator") or "eq",
                value=value,
            )
        )

    return filters


def parse_sort(query_params: Mapping[str, str]) -> List[str]:
    sort = query_params.get("sort")
    if not sort:
        return []
    return split_comma_separated(sort)


def parse_include(query_params: Mapping[str, str]) -> List[str]:
    include = query_params.get("include")
    if not include:
        return []
    return split_comma_separated(include)


def parse_fields(query_params: Mapping[str, str]) -> List[str]:
    fields = query_params.get("fields")
    if not fields:
        return []
    return split_comma_separated(fields)


def parse_query_params(query_params: Mapping[str, str]) -> QueryParams:
    return QueryParams(
        filters=parse_filters(query_params),
        sort=parse_sort(query_params),
        include=parse_include(query_params),
        fields=parse_fields(query_params),
    )

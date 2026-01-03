from typing import Any, List

from pydantic import BaseModel


class FilterSchema(BaseModel):
    field: str
    operator: str = "eq"
    value: Any


class QueryParams(BaseModel):
    filters: List[FilterSchema] = []
    sort: List[str] = []
    include: List[str] = []
    fields: List[str] = []

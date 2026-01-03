from pydantic import BaseModel
from typing import Any, List

class FilterSchema(BaseModel):
    field: str
    operator: str = "eq"
    value: Any
    
class QueryParams(BaseModel):
    filters: List[FilterSchema] = []
    sort: List[str] = []
    include: List[str] = []
    fields: List[str] = []
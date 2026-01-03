"""
Pydantic schemas for filters.

This module defines the data structures used to represent filter conditions.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from .operators import FilterOperator


class RawFilterSchema(BaseModel):
    """
    Represents a raw filter condition as parsed from the URL.

    This is an intermediate structure before validation and resolution.
    The field name may be an alias, and the operator may be None (to be resolved).
    """

    alias_or_field: str = Field(..., description="The field name or alias from the URL")
    operator: str | None = Field(
        default=None,
        description="The operator from the URL, or None if not specified",
    )
    values: list[str] = Field(..., description="The raw string values from the URL")

    class Config:
        """Pydantic configuration."""

        frozen = True


class FilterSchema(BaseModel):
    """Represents a single filter condition."""

    field: str = Field(..., description="The field name to filter on")
    operator: str = Field(
        default=FilterOperator.default(),
        description="The operator to use for filtering",
    )
    value: Any = Field(..., description="The value to filter by")

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: str) -> str:
        """Validate that the operator is supported."""
        valid_operators = [op.value for op in FilterOperator]
        if v not in valid_operators:
            raise ValueError(
                f"Invalid operator '{v}'. "
                f"Supported operators: {', '.join(valid_operators)}"
            )
        return v

    class Config:
        """Pydantic configuration."""

        frozen = True
        json_schema_extra = {
            "example": {
                "field": "name",
                "operator": "eq",
                "value": "John",
            }
        }


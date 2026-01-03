"""
Database module for fastapi-crud-kit.

This module provides database factory, session management, decorators, and context managers.
"""

from fastapi_crud_kit.database.exceptions import (
    ConnectionError,
    DatabaseError,
    IsolationLevelError,
    ReadOnlyViolationError,
    TransactionError,
)
from fastapi_crud_kit.database.factory import DatabaseFactory
from fastapi_crud_kit.database.session import get_async_db, get_sync_db

__all__ = [
    "DatabaseFactory",
    "get_async_db",
    "get_sync_db",
    
    "DatabaseError",
    "ConnectionError",
    "TransactionError",
    "ReadOnlyViolationError",
    "IsolationLevelError",
]

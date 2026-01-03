"""
Custom exceptions for database operations.

This module provides a hierarchy of exceptions for database-related errors
including connections, transactions, and isolation levels.
"""


class DatabaseError(Exception):
    """Base exception for database-related errors."""

    pass


class TransactionError(DatabaseError):
    """Exception raised for transaction-related errors."""

    pass


class ReadOnlyViolationError(DatabaseError):
    """Exception raised when a write operation is attempted in read-only mode."""

    pass


class IsolationLevelError(DatabaseError):
    """Exception raised for isolation level configuration errors."""

    pass


class ConnectionError(DatabaseError):
    """Exception raised for connection-related errors."""

    pass

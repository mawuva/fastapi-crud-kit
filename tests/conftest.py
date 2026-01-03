"""Shared fixtures and test models for database mode tests."""

from __future__ import annotations

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from fastapi_crud_kit.database.mode.async_mode import AsyncModeHandler
from fastapi_crud_kit.database.mode.sync_mode import SyncModeHandler


class Base(DeclarativeBase):
    """Base class for test models."""


class UserModel(Base):
    """Test model for database operations."""

    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


@pytest.fixture
def async_handler() -> AsyncModeHandler:
    """Create an AsyncModeHandler instance."""
    return AsyncModeHandler()


@pytest.fixture
def sync_handler() -> SyncModeHandler:
    """Create a SyncModeHandler instance."""
    return SyncModeHandler()


@pytest.fixture
def async_database_url() -> str:
    """Create a test database URL for async mode."""
    return "postgresql+asyncpg://user:pass@host/db"


@pytest.fixture
def sync_database_url() -> str:
    """Create a test database URL for sync mode."""
    return "sqlite:///:memory:"

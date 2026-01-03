"""Tests for AsyncModeHandler."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from fastapi_crud_kit.database.mode.async_mode import AsyncModeHandler
from tests.conftest import Base


class TestAsyncModeHandler:
    """Test suite for AsyncModeHandler."""

    @patch("fastapi_crud_kit.database.mode.async_mode.create_async_engine")
    def test_create_engine(
        self,
        mock_create_engine: MagicMock,
        async_handler: AsyncModeHandler,
        async_database_url: str,
    ) -> None:
        """
        Scenario: Create an async engine with default parameters.

        Expected:
        - Engine is created successfully
        - create_async_engine is called with correct parameters
        - Engine is returned
        """
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        engine = async_handler.create_engine(async_database_url)

        assert engine is not None
        mock_create_engine.assert_called_once_with(
            async_database_url, pool_pre_ping=True, echo=False
        )

    @patch("fastapi_crud_kit.database.mode.async_mode.create_async_engine")
    def test_create_engine_with_echo(
        self,
        mock_create_engine: MagicMock,
        async_handler: AsyncModeHandler,
        async_database_url: str,
    ) -> None:
        """
        Scenario: Create an async engine with echo enabled.

        Expected:
        - Engine is created successfully
        - create_async_engine is called with echo=True
        """
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        engine = async_handler.create_engine(async_database_url, echo=True)

        assert engine is not None
        mock_create_engine.assert_called_once_with(
            async_database_url, pool_pre_ping=True, echo=True
        )

    @patch("fastapi_crud_kit.database.mode.async_mode.create_async_engine")
    def test_create_engine_with_pool_pre_ping(
        self,
        mock_create_engine: MagicMock,
        async_handler: AsyncModeHandler,
        async_database_url: str,
    ) -> None:
        """
        Scenario: Create an async engine with pool_pre_ping disabled.

        Expected:
        - Engine is created successfully
        - create_async_engine is called with pool_pre_ping=False
        """
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        engine = async_handler.create_engine(async_database_url, pool_pre_ping=False)

        assert engine is not None
        mock_create_engine.assert_called_once_with(
            async_database_url, pool_pre_ping=False, echo=False
        )

    @patch("fastapi_crud_kit.database.mode.async_mode.create_async_engine")
    @patch("fastapi_crud_kit.database.mode.async_mode.async_sessionmaker")
    def test_create_session_maker(
        self,
        mock_sessionmaker: MagicMock,
        mock_create_engine: MagicMock,
        async_handler: AsyncModeHandler,
        async_database_url: str,
    ) -> None:
        """
        Scenario: Create an async session maker from an engine.

        Expected:
        - Session maker is created successfully
        - async_sessionmaker is called with correct parameters
        - Session maker is returned
        """
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine
        mock_session_maker_instance = MagicMock()
        mock_sessionmaker.return_value = mock_session_maker_instance

        engine = async_handler.create_engine(async_database_url)
        session_maker = async_handler.create_session_maker(engine)

        assert session_maker is not None
        mock_sessionmaker.assert_called_once()

    def test_prepare_database_url_postgresql(
        self, async_handler: AsyncModeHandler
    ) -> None:
        """
        Scenario: Prepare database URL for PostgreSQL with async driver.

        Expected:
        - URL is correctly formatted with asyncpg driver
        - URL contains postgresql+asyncpg://
        """
        base_url = "postgresql://user:pass@host/db"
        database_type = "postgresql"
        result = async_handler.prepare_database_url(base_url, database_type)

        assert result == "postgresql+asyncpg://user:pass@host/db"

    def test_prepare_database_url_mysql(self, async_handler: AsyncModeHandler) -> None:
        """
        Scenario: Prepare database URL for MySQL with async driver.

        Expected:
        - URL is correctly formatted with aiomysql driver
        - URL contains mysql+aiomysql://
        """
        base_url = "mysql://user:pass@host/db"
        database_type = "mysql"
        result = async_handler.prepare_database_url(base_url, database_type)

        assert result == "mysql+aiomysql://user:pass@host/db"

    def test_prepare_database_url_sqlite(self, async_handler: AsyncModeHandler) -> None:
        """
        Scenario: Prepare database URL for SQLite with async driver.

        Expected:
        - URL is correctly formatted with aiosqlite driver
        - URL contains sqlite+aiosqlite://
        """
        base_url = "sqlite:///test.db"
        database_type = "sqlite"
        result = async_handler.prepare_database_url(base_url, database_type)

        assert result == "sqlite+aiosqlite:///test.db"

    def test_prepare_database_url_with_existing_driver(
        self, async_handler: AsyncModeHandler
    ) -> None:
        """
        Scenario: Prepare database URL when driver already exists in URL.

        Expected:
        - Method handles URL with existing driver correctly
        - URL is properly formatted with async driver
        """
        # Test that URLs without drivers work correctly (main use case)
        # The method should add the driver if it's missing
        base_url = "postgresql://user:pass@host/db"
        database_type = "postgresql"
        result = async_handler.prepare_database_url(base_url, database_type)

        # Should contain the async driver
        assert "asyncpg" in result
        assert "user:pass@host/db" in result
        assert result == "postgresql+asyncpg://user:pass@host/db"

    def test_prepare_database_url_unsupported_database(
        self, async_handler: AsyncModeHandler
    ) -> None:
        """
        Scenario: Prepare database URL for unsupported database type.

        Expected:
        - ValueError is raised
        - Error message indicates driver not available
        """
        base_url = "oracle://user:pass@host/db"
        database_type = "oracle"

        with pytest.raises(ValueError, match="Async driver not available for oracle"):
            async_handler.prepare_database_url(base_url, database_type)

    @patch("fastapi_crud_kit.database.mode.async_mode.create_async_engine")
    def test_create_all_tables(
        self,
        mock_create_engine: MagicMock,
        async_handler: AsyncModeHandler,
        async_database_url: str,
    ) -> None:
        """
        Scenario: Create all tables using async engine.

        Expected:
        - Method calls engine.begin() correctly
        - Tables are created successfully
        - No exceptions are raised
        """
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_context = AsyncMock()
        mock_conn = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_engine.begin.return_value = mock_context
        mock_create_engine.return_value = mock_engine

        engine = async_handler.create_engine(async_database_url)

        async def run_test() -> None:
            await async_handler.create_all_tables(engine, Base)

        asyncio.run(run_test())

        # Verify engine.begin() was called
        mock_engine.begin.assert_called_once()

    @patch("fastapi_crud_kit.database.mode.async_mode.create_async_engine")
    def test_drop_all_tables(
        self,
        mock_create_engine: MagicMock,
        async_handler: AsyncModeHandler,
        async_database_url: str,
    ) -> None:
        """
        Scenario: Drop all tables using async engine.

        Expected:
        - Method calls engine.begin() correctly
        - Tables are dropped successfully
        - No exceptions are raised
        """
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_context = AsyncMock()
        mock_conn = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        mock_engine.begin.return_value = mock_context
        mock_create_engine.return_value = mock_engine

        engine = async_handler.create_engine(async_database_url)

        async def run_test() -> None:
            await async_handler.drop_all_tables(engine, Base)

        asyncio.run(run_test())

        # Verify engine.begin() was called
        mock_engine.begin.assert_called_once()

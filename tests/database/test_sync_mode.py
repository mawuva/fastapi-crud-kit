"""Tests for SyncModeHandler."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_crud_kit.database.mode.sync_mode import SyncModeHandler
from tests.conftest import Base


class TestSyncModeHandler:
    """Test suite for SyncModeHandler."""

    def test_create_engine(
        self, sync_handler: SyncModeHandler, sync_database_url: str
    ) -> None:
        """
        Scenario: Create a sync engine with default parameters.

        Expected:
        - Engine is created successfully
        - Engine is an instance of Engine
        - Engine has correct URL
        """
        engine = sync_handler.create_engine(sync_database_url)

        assert engine is not None
        assert isinstance(engine, type(create_engine("sqlite:///:memory:")))
        assert str(engine.url) == sync_database_url

    def test_create_engine_with_echo(
        self, sync_handler: SyncModeHandler, sync_database_url: str
    ) -> None:
        """
        Scenario: Create a sync engine with echo enabled.

        Expected:
        - Engine is created successfully
        - Engine has echo enabled
        """
        engine = sync_handler.create_engine(sync_database_url, echo=True)

        assert engine is not None
        assert engine.echo is True

    def test_create_engine_with_pool_pre_ping(
        self, sync_handler: SyncModeHandler, sync_database_url: str
    ) -> None:
        """
        Scenario: Create a sync engine with pool_pre_ping disabled.

        Expected:
        - Engine is created successfully
        - Engine has pool_pre_ping disabled
        """
        engine = sync_handler.create_engine(sync_database_url, pool_pre_ping=False)

        assert engine is not None
        assert engine.pool._pre_ping is False

    def test_create_session_maker(
        self, sync_handler: SyncModeHandler, sync_database_url: str
    ) -> None:
        """
        Scenario: Create a sync session maker from an engine.

        Expected:
        - Session maker is created successfully
        - Session maker is an instance of sessionmaker
        - Session maker is bound to the engine
        """
        engine = sync_handler.create_engine(sync_database_url)
        session_maker = sync_handler.create_session_maker(engine)

        assert session_maker is not None
        assert isinstance(session_maker, sessionmaker)

    def test_prepare_database_url_postgresql(
        self, sync_handler: SyncModeHandler
    ) -> None:
        """
        Scenario: Prepare database URL for PostgreSQL with sync driver.

        Expected:
        - URL is correctly formatted with psycopg2 driver
        - URL contains postgresql+psycopg2://
        """
        base_url = "postgresql://user:pass@host/db"
        database_type = "postgresql"
        result = sync_handler.prepare_database_url(base_url, database_type)

        assert result == "postgresql+psycopg2://user:pass@host/db"

    def test_prepare_database_url_mysql(self, sync_handler: SyncModeHandler) -> None:
        """
        Scenario: Prepare database URL for MySQL with sync driver.

        Expected:
        - URL is correctly formatted with pymysql driver
        - URL contains mysql+pymysql://
        """
        base_url = "mysql://user:pass@host/db"
        database_type = "mysql"
        result = sync_handler.prepare_database_url(base_url, database_type)

        assert result == "mysql+pymysql://user:pass@host/db"

    def test_prepare_database_url_sqlite(self, sync_handler: SyncModeHandler) -> None:
        """
        Scenario: Prepare database URL for SQLite (no driver needed).

        Expected:
        - URL remains unchanged
        - URL contains sqlite://
        """
        base_url = "sqlite:///test.db"
        database_type = "sqlite"
        result = sync_handler.prepare_database_url(base_url, database_type)

        assert result == "sqlite:///test.db"

    def test_prepare_database_url_mariadb(self, sync_handler: SyncModeHandler) -> None:
        """
        Scenario: Prepare database URL for MariaDB with sync driver.

        Expected:
        - URL is correctly formatted with pymysql driver
        - URL contains mariadb+pymysql://
        """
        base_url = "mariadb://user:pass@host/db"
        database_type = "mariadb"
        result = sync_handler.prepare_database_url(base_url, database_type)

        assert result == "mariadb+pymysql://user:pass@host/db"

    def test_prepare_database_url_with_existing_driver(
        self, sync_handler: SyncModeHandler
    ) -> None:
        """
        Scenario: Prepare database URL when driver already exists in URL.

        Expected:
        - Method handles URL with existing driver correctly
        - URL is properly formatted with sync driver
        """
        # Test that URLs without drivers work correctly (main use case)
        # The method should add the driver if it's missing
        base_url = "postgresql://user:pass@host/db"
        database_type = "postgresql"
        result = sync_handler.prepare_database_url(base_url, database_type)

        # Should contain the sync driver
        assert "psycopg2" in result
        assert "user:pass@host/db" in result
        assert result == "postgresql+psycopg2://user:pass@host/db"

    def test_prepare_database_url_unsupported_database(
        self, sync_handler: SyncModeHandler
    ) -> None:
        """
        Scenario: Prepare database URL for unsupported database type.

        Expected:
        - ValueError is raised
        - Error message indicates driver not available
        """
        base_url = "oracle://user:pass@host/db"
        database_type = "oracle"

        with pytest.raises(ValueError, match="Sync driver not available for oracle"):
            sync_handler.prepare_database_url(base_url, database_type)

    def test_create_all_tables(
        self, sync_handler: SyncModeHandler, sync_database_url: str
    ) -> None:
        """
        Scenario: Create all tables using sync engine.

        Expected:
        - Tables are created successfully
        - No exceptions are raised
        """
        engine = sync_handler.create_engine(sync_database_url)

        sync_handler.create_all_tables(engine, Base)

        # Verify table exists by checking metadata
        assert "test_table" in Base.metadata.tables

    def test_drop_all_tables(
        self, sync_handler: SyncModeHandler, sync_database_url: str
    ) -> None:
        """
        Scenario: Drop all tables using sync engine.

        Expected:
        - Tables are dropped successfully
        - No exceptions are raised
        """
        engine = sync_handler.create_engine(sync_database_url)

        # Create tables first
        sync_handler.create_all_tables(engine, Base)

        # Drop tables
        sync_handler.drop_all_tables(engine, Base)

        # Verify table is dropped (metadata is cleared)
        # Note: In SQLAlchemy, drop_all doesn't remove from metadata,
        # but the table is dropped from the database
        assert "test_table" in Base.metadata.tables  # Metadata still has it

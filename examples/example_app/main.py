"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connections
    await close_db()


app = FastAPI(
    title="FastAPI CRUD Kit Example",
    description="Example application demonstrating fastapi-crud-kit usage",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to FastAPI CRUD Kit Example",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }

import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app.db import get_session
from app.main import app

TEST_DB_NAME = "pytest"
POSTGRES_USER: str = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@psql:5432/{TEST_DB_NAME}"
)

engine = create_async_engine(TEST_DATABASE_URL)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session: sessionmaker[AsyncSession] = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture()
def test_app() -> TestClient:
    client = TestClient(app)
    return client


async def create_db() -> None:
    engine = create_async_engine(
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@psql:5432/postgres",
        isolation_level="AUTOCOMMIT",
    )
    async with engine.connect() as conn:
        await conn.execute(
            text(f"CREATE DATABASE {TEST_DB_NAME} OWNER {POSTGRES_USER}")
        )
        await conn.close()
    await init_db()


async def drop_db() -> None:
    await dispose_db()
    engine = create_async_engine(
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@psql:5432/postgres",
        isolation_level="AUTOCOMMIT",
    )
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE {TEST_DB_NAME}"))
        await conn.close()


@pytest.fixture()
def test_app_async() -> Generator[AsyncClient, None, None]:
    asyncio.get_event_loop().run_until_complete(create_db())
    try:
        client = AsyncClient(app=app, base_url="http://localhost")
        yield client
    finally:
        asyncio.get_event_loop().run_until_complete(drop_db())

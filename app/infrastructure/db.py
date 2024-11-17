import asyncio
from typing import AsyncGenerator
import databases
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from asyncpg.exceptions import (
    CannotConnectNowError,
    ConnectionDoesNotExistError
)

from app.infrastructure.config import config

from app.infrastructure.models.user_model import Base



db_uri = config.DB_CONN_STR
engine= create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True
)

async_session = sessionmaker(engine, class_=AsyncSession)

database = databases.Database(
    db_uri,
    force_rollback=True
)

async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db(retries: int = 5, delay: int = 5) -> None:

    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("hello")
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
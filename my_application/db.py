from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base

from config import LOGIN_DB, PASSWORD_DB, HOST_DB, PORT_DB, NAME_DB

url: str = f"postgresql+asyncpg://{LOGIN_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"

SQLALCHEMY_DATABASE_URL: str = url

engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)

Base: Any = declarative_base()


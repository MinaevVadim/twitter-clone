from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from db import SessionLocal


async def connect_db() -> AsyncGenerator[AsyncSession, Any]:
    async with SessionLocal() as session:
        async with session.begin():
            yield session


import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from starlette.testclient import TestClient

from config import LOGIN_DB, PASSWORD_DB, HOST_DB, PORT_DB
from models import Base, User
from dependencies import connect_db
from main import app


class MyEngine:
    def __init__(self) -> None:
        self.path = f'postgresql+psycopg://{LOGIN_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/tweet'
        self.engine = create_async_engine(self.path, future=True)

    def async_session(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )


my_engine: MyEngine = MyEngine()
result: AsyncEngine = my_engine.engine
async_session: async_sessionmaker[AsyncSession] = my_engine.async_session()


async def create_tables_and_objects():
    async with result.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override():
        async with async_session() as session_for_override:
            async with session_for_override.begin():
                yield session_for_override

    async with async_session() as session_for_create_objects:
        async with session_for_create_objects.begin():
            create_user_vadim = User(api_key='user_vadim', name='Vadim')
            create_user_veronika = User(api_key='user_veronika', name='Veronika')
            session_for_create_objects.add(create_user_vadim)
            session_for_create_objects.add(create_user_veronika)

    app.dependency_overrides[connect_db] = override


async def drop_tables():
    async with result.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
def db_create():
    asyncio.run(create_tables_and_objects())
    yield
    asyncio.run(drop_tables())


@pytest.fixture
def db_client():
    client: TestClient = TestClient(app)
    yield client

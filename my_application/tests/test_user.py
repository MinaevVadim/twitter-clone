import json

import pytest
from sqlalchemy import select, cast, String
from sqlalchemy.orm import selectinload

from conftest import async_session
from models import User


@pytest.mark.asyncio
async def test_create_follower_with_correct_user(db_client):
    response = db_client.post(
        '/api/users/2/follow',
        headers={'api-key': 'user_vadim'}
    )
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(selectinload(User.following)).where(
                    User.api_key == cast('user_vadim', String)))
            result = result.scalar_one_or_none()
            result = result.following[0].id
    assert response.status_code == 201
    assert result == 2


@pytest.mark.asyncio
async def test_create_follower_with_unknown_user(db_client):
    response = db_client.post(
        '/api/users/2/follow',
        headers={'api-key': 'unknown_user'}
    )
    result = json.loads(response.content.decode())
    result = result['message']
    assert response.status_code == 400
    assert result == 'There is no such user or follower.'


@pytest.mark.asyncio
async def test_create_unknown_follower(db_client):
    response = db_client.post(
        '/api/users/3/follow',
        headers={'api-key': 'user_vadim'}
    )
    result = json.loads(response.content.decode())
    result = result['message']
    assert response.status_code == 400
    assert result == 'There is no such user or follower.'


@pytest.mark.asyncio
async def test_delete_follower_with_unknown_user(db_client):
    response = db_client.delete(
        '/api/users/2/follow',
        headers={'api-key': 'unknown_user'}
    )
    result = json.loads(response.content.decode())
    result = result['message']
    assert response.status_code == 400
    assert result == 'There is no such user or follower.'


@pytest.mark.asyncio
async def test_delete_unknown_follower(db_client):
    response = db_client.delete(
        '/api/users/3/follow',
        headers={'api-key': 'user_vadim'}
    )
    result = json.loads(response.content.decode())
    result = result['message']
    assert response.status_code == 400
    assert result == 'There is no such user or follower.'


@pytest.mark.asyncio
async def test_delete_follower_with_correct_user(db_client):
    response = db_client.delete(
        '/api/users/2/follow',
        headers={'api-key': 'user_vadim'}
    )
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(selectinload(User.following)).where(
                    User.api_key == cast('user_vadim', String)))
            result = result.scalar_one_or_none()
            result = result.following
    assert response.status_code == 200
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_correct_user_api_key(db_client):
    response = db_client.get(
        '/api/users/me',
        headers={'api-key': 'user_vadim'}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_unknown_user_api_key(db_client):
    response = db_client.get(
        '/api/users/me',
        headers={'api-key': 'unknown_user'}
    )

    result = json.loads(response.content.decode())
    result = result['message']
    assert response.status_code == 400
    assert result == 'There is no such user.'


@pytest.mark.asyncio
async def test_get_correct_user_id(db_client):
    response = db_client.get('/api/users/1')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_unknown_user_id(db_client):
    response = db_client.get('/api/users/3')
    result = json.loads(response.content.decode())
    result = result['message']
    assert response.status_code == 400
    assert result == 'There is no such user.'

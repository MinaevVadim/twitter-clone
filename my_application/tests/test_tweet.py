import json

import pytest
from sqlalchemy import select, cast, Integer

from conftest import async_session
from models import Tweet, Like


@pytest.mark.asyncio
async def test_create_tweet_with_correct_user(db_client):
    response = db_client.post(
        '/api/tweets',
        json={"tweet_data": "Hello World"},
        headers={"api-key": "user_vadim"})
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Tweet).where(Tweet.id == cast(1, Integer)))
            result = result.scalars().all()
    assert len(result) == 1
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_tweet_with_unknown_user(db_client):
    response = db_client.post(
        '/api/tweets',
        json={"tweet_data": "Good Bye World"},
        headers={"api-key": "not_found_user"})
    not_user = json.loads(response.content.decode())
    assert not_user['message'] == 'There is no such user.'
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_tweets_with_correct_user(db_client):
    response = db_client.get(
        '/api/tweets',
        headers={"api-key": "user_vadim"})
    user = json.loads(response.content.decode())
    assert len(user['tweets']) == 1
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_tweets_with_unknown_user(db_client):
    response = db_client.get(
        '/api/tweets',
        headers={"api-key": "not_found_user"})
    user = json.loads(response.content.decode())
    assert len(user['tweets']) == 0
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_like_with_correct_tweet_id(db_client):
    response = db_client.post(
        '/api/tweets/1/likes',
        headers={"api-key": "user_veronika"})
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Like))
            result = result.scalars().first()
    assert result.user_id == 2
    assert result.tweet_id == 1
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_like_with_incorrect_tweet_id(db_client):
    response = db_client.post(
        '/api/tweets/2/likes',
        headers={"api-key": "user_veronika"})
    user = json.loads(response.content.decode())
    assert user['message'] == 'There is no such user or tweet.'
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_tweet_with_incorrect_tweet_id(db_client):
    response = db_client.delete(
        '/api/tweets/2',
        headers={"api-key": "not_found_user"})
    user = json.loads(response.content.decode())
    assert user['message'] == 'There is no such tweet.'
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_like_with_incorrect_tweet_id(db_client):
    response = db_client.delete(
        '/api/tweets/2/likes',
        headers={"api-key": "not_found_user"})
    user = json.loads(response.content.decode())
    assert user['message'] == 'There is no such user or tweet.'
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_like_with_correct_tweet_id(db_client):
    response = db_client.delete(
        '/api/tweets/1/likes',
        headers={"api-key": "user_veronika"})
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Like))
            result = result.scalars().first()
    assert result is None
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_delete_tweet_with_correct_tweet_id(db_client):
    response = db_client.delete(
        '/api/tweets/1',
        headers={"api-key": "user_vadim"})
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Tweet).where(Tweet.id == cast(1, Integer)))
            result = result.scalar_one_or_none()
    assert result is None
    assert response.status_code == 202

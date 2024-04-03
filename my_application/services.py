import os
from distutils.util import execute
from logging import Logger
from typing import Optional, Any

import aiofiles as aiofiles
from fastapi import UploadFile
from sqlalchemy import select, cast, String, Integer
from sqlalchemy.orm import selectinload

import twitter_logging
from models import Tweet, User, user_following, Like

logger: Logger = twitter_logging.add_logger(__name__)

base_dir: str = os.path.dirname(os.path.dirname(__file__))


def decorator_log(func: Any):
    def wrapper(*args, **kwargs):
        logger.info(f'Start {func.__name__}.')
        result = func(*args, **kwargs)
        logger.info(f'Finished {func.__name__}.')
        return result
    return wrapper


@decorator_log
async def get_tweet_one(session: {execute}, id_tweets: int, api_key: Optional[str]):
    tweet: Any = await session.execute(select(
        Tweet, User).join(User, Tweet.author == cast(User.id, Integer)).where(
        User.api_key == cast(api_key, String), Tweet.id == cast(id_tweets, Integer)))
    tweet: Any = tweet.scalar_one_or_none()
    return tweet


@decorator_log
async def get_tweet_for_likes(session: {execute}, id_tweets: int):
    tweet: Any = await session.execute(select(
        Tweet).where(Tweet.id == cast(id_tweets, Integer)))
    tweet: Any = tweet.scalar_one_or_none()
    return tweet


@decorator_log
async def get_tweet_list(session: {execute}, api_key: Optional[str]):
    tweet: Any = await session.execute(
        select(Tweet, User).options(selectinload(Tweet.users)).join(
            User, Tweet.author == cast(User.id, Integer)).where(
            User.api_key == cast(api_key, String)))
    tweet: Any = tweet.scalars().all()
    return tweet


@decorator_log
async def get_user_api_key(session: {execute}, api_key: Optional[str]):
    user: Any = await session.execute(
        select(User).options(selectinload(User.following)).where(
            User.api_key == cast(api_key, String)))
    user: Any = user.scalar_one_or_none()
    return user


@decorator_log
async def get_id_user(session: {execute}, id_user: int):
    user: Any = await session.execute(
        select(User).where(User.id == cast(id_user, Integer)))
    user: Any = user.scalar_one_or_none()
    return user


@decorator_log
async def info_user_id(session: {execute}, id_user: int):
    user: Any = await session.execute(select(User).options(selectinload(User.following)).where(
        User.id == cast(id_user, Integer)))
    user: Any = user.scalar_one_or_none()
    return user


@decorator_log
async def info_user_api_key(session: {execute}, api_key: Optional[str]):
    user: Any = await session.execute(select(User).options(selectinload(User.following)).where(
        User.api_key == cast(api_key, String)))
    user: Any = user.scalar_one_or_none()
    return user


@decorator_log
async def get_user_following(session: {execute}, user: Any):
    following: Any = await session.execute(select(User).join(
        user_following, user_following.c.followers == User.id).where(
            user_following.c.following == cast(user.id, Integer)))
    following_list: Any = following.scalars().all()
    following: list[dict] = [i.to_json() for i in following_list]
    result: dict = user.get_user_json()
    result.update({'following': following})
    return result


@decorator_log
async def get_likes(session: {execute}, user: Any, tweet: Any):
    like: Any = await session.execute(select(Like).where(
        Like.user_id == user.id, Like.tweet_id == tweet.id))
    like: Any = like.scalar_one_or_none()
    return like


@decorator_log
async def upload_media(file: UploadFile, request) -> Optional[str]:
    content: str = file.filename.replace(" ", "")
    url: str = f'{request.url}/image/{content}'
    path: str = os.path.join(base_dir, 'my_application', 'storage', 'media', content)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    await file.seek(0)
    if file_size <= 2 * 1024 * 1024:
        async with aiofiles.open(path, 'wb') as f:
            await f.write(file.file.read())
        return url
    logger.error(f'Error file size.')
    return None


@decorator_log
async def give_media(image: str) -> Optional[bytes]:
    path: bytes | str = os.path.join(
        base_dir, 'my_application', 'storage', 'media', image)
    try:
        async with aiofiles.open(path, 'rb') as f:
            result: bytes = await f.read()
    except Exception as exc:
        logger.error(f'Error file {exc}.')
        return None
    return result

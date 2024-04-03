from logging import Logger
from typing import Any, Annotated
from fastapi import Request
from asyncpg import UniqueViolationError
from fastapi import APIRouter, Header, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from starlette.responses import JSONResponse

import twitter_logging
from config_swagger import error_response
from dependencies import connect_db
from schemas import TweetCreateBase, TweetResponseBase, ResultBase, ResponseCreatedTweetBase

from models import Tweet, Like
from services import get_user_api_key, get_tweet_one, get_likes, get_tweet_list, get_tweet_for_likes

logger: Logger = twitter_logging.add_logger(__name__)


router: APIRouter = APIRouter(
    prefix='/api/tweets',
    tags=['tweets'],

)


@router.get(
    "",
    status_code=200,
    responses=error_response,
    response_model=TweetResponseBase,
)
async def get_all_tweets(
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> dict[str, bool | list]:
    tweet_list: Any = await get_tweet_list(session, api_key)
    result: list = [i.to_json() for i in tweet_list]
    return {'result': True, 'tweets': result}


@router.post(
    "",
    status_code=201,
    response_model=ResponseCreatedTweetBase,
    responses=error_response,
)
async def create_tweet(
        tweet: TweetCreateBase,
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool | int]:
    """
        Create an item with all the information:
        - **tweet_data**: tweet content
        - **tweet_media_ids**: optional parameter for media
    """
    user: Any = await get_user_api_key(session, api_key)
    if user is None:
        logger.error('There is no such user.')
        return JSONResponse(
            status_code=400,
            content={"message": "There is no such user."})
    add_new_tweet: Tweet = Tweet(
        content=tweet.tweet_data,
        author=user.id
    )
    session.add(add_new_tweet)
    await session.flush()
    return {'result': True, 'tweet_id': add_new_tweet.id}


@router.delete(
    "/{id_tweet}",
    status_code=202,
    response_model=ResultBase,
    responses=error_response,
)
async def delete_tweet(
        id_tweet: Annotated[int, Path(title="The ID of the tweet to get")],
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db),
) -> JSONResponse | dict[str, bool]:
    tweet: Any = await get_tweet_one(session, id_tweet, api_key)
    if tweet is None:
        logger.error('There is no such tweet.')
        return JSONResponse(
            status_code=400,
            content={"message": "There is no such tweet."})
    await session.delete(tweet)
    await session.commit()
    return {'result': True}


@router.post(
    "/{id_tweet}/likes",
    status_code=201,
    response_model=ResultBase,
    responses=error_response,
)
async def create_like(
        id_tweet: Annotated[int, Path(title="The ID of the tweet to get")],
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool]:
    user: Any = await get_user_api_key(session, api_key)
    tweet: Any = await get_tweet_for_likes(session, id_tweet)
    if user is None or tweet is None:
        logger.error('There is no such user or tweet.')
        return JSONResponse(
            status_code=400,
            content={"message": "There is no such user or tweet."})
    add_like: Like = Like(
        user_id=user.id,
        tweet_id=tweet.id
    )
    session.add(add_like)
    try:
        await session.commit()
    except (IntegrityError, UniqueViolationError):
        return JSONResponse(
            status_code=400,
            content={"message": f"You can't put likes more than once."})
    return {'result': True}


@router.delete(
    "/{id_tweet}/likes",
    status_code=202,
    response_model=ResultBase,
    responses=error_response,
)
async def delete_like(
        id_tweet: Annotated[int, Path(title="The ID of the tweet to get")],
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool]:
    user: Any = await get_user_api_key(session, api_key)
    tweet: Any = await get_tweet_for_likes(session, id_tweet)
    if user is None or tweet is None:
        logger.error('There is no such user or tweet')
        return JSONResponse(
            status_code=400,
            content={"message": "There is no such user or tweet."})
    likes: Any = await get_likes(session, user, tweet)
    await session.delete(likes)
    await session.commit()
    return {'result': True}

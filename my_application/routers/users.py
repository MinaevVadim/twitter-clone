from logging import Logger
from typing import Any, Annotated

from fastapi import APIRouter, Header, Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from starlette.responses import JSONResponse

import twitter_logging
from config_swagger import error_response
from dependencies import connect_db
from schemas import UserResponseBase, ResultBase

from services import get_user_api_key, get_id_user, info_user_api_key, get_user_following,\
    info_user_id

from my_application.utils import error_no_such

logger: Logger = twitter_logging.add_logger(__name__)


router: APIRouter = APIRouter(
    prefix='/api/users',
    tags=['users'],

)


@router.post(
    "/{id_user}/follow",
    status_code=201,
    response_model=ResultBase,
    responses=error_response,
)
async def create_follow(
        id_user: Annotated[int, Path(title="The ID of the user to get")],
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool]:
    user_api_key = await get_user_api_key(session, api_key)
    follower = await get_id_user(session, id_user)
    if user_api_key is None or follower is None:
        error_no_such('follower')
    user_api_key.following.append(follower)
    await session.commit()
    return {'result': True}


@router.delete(
    "/{id_user}/follow",
    status_code=200,
    response_model=ResultBase,
    responses=error_response,
)
async def delete_follow(
        id_user: Annotated[int, Path(title="The ID of the user to get")],
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool]:
    user_api_key = await get_user_api_key(session, api_key)
    follower = await get_id_user(session, id_user)
    if user_api_key is None or follower is None:
        error_no_such('user or follower')
    user_api_key.following.remove(follower)
    await session.commit()
    return {'result': True}


@router.get(
    "/me",
    status_code=200,
    responses=error_response,
    response_model=UserResponseBase,
)
async def get_user(
        api_key: Annotated[str | None, Header()] = None,
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool]:
    user = await info_user_api_key(session, api_key)
    if user is None:
        error_no_such('user')
    result = await get_user_following(session, user)
    return {'result': True, 'user': result}


@router.get(
    "/{id_user}",
    status_code=200,
    response_model=UserResponseBase,
    responses=error_response,
)
async def get_user_id(
        id_user: Annotated[int, Path(title="The ID of the user to get")],
        session: AsyncSession = Depends(connect_db)
) -> JSONResponse | dict[str, bool]:
    user = await info_user_id(session, id_user)
    if user is None:
        error_no_such('user')
    result = await get_user_following(session, user)
    return {'result': True, 'user': result}

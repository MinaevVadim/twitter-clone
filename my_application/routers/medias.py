from logging import Logger
from typing import Optional, Any, Annotated

from fastapi import File, UploadFile, APIRouter, Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from starlette.responses import Response, JSONResponse
import twitter_logging
from config_swagger import error_response
from dependencies import connect_db
from schemas import ResponseMediaBase
from models import Media
from services import upload_media, give_media
from utils import file_check
from fastapi import Request

logger: Logger = twitter_logging.add_logger(__name__)


router: APIRouter = APIRouter(
    prefix='/api/medias',
    tags=['medias'],

)


@router.post(
    "",
    status_code=201,
    responses=error_response,
    response_model=ResponseMediaBase,
)
async def load_media(
        request: Request,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(connect_db)
) -> dict[str, bool | int] | JSONResponse:
    if file and await file_check(file.filename):
        url = await upload_media(file, request)
        if url:
            add_file = Media(media=url)
            session.add(add_file)
            await session.commit()
            return {'result': True, 'media_id': add_file.id}
        return JSONResponse(
            status_code=400,
            content={"message": "The file size is too large."})
    return JSONResponse(
            status_code=400,
            content={"message": "This file extension is not supported."})


@router.get(
    "/image/{image}",
    status_code=200,
    responses=error_response,
)
async def give_image(
        image: Annotated[str, Path(title="The name of the image to get")]
) -> Any:
    content = await give_media(image)
    if content:
        return Response(content=content, media_type="image/png")
    return JSONResponse(
            status_code=400,
            content={"message": "Wrong path to the image."})

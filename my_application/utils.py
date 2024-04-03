from logging import Logger

from starlette.responses import JSONResponse

from my_application import twitter_logging

ALLOWED_EXTENSIONS: list[str] = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

logger: Logger = twitter_logging.add_logger(__name__)


async def file_check(file_name) -> bool:
    return '.' in file_name and file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def error_no_such(name: str) -> JSONResponse:
    logger.error(f'There is no such {name}.')
    return JSONResponse(
        status_code=400,
        content={"message": f"There is no such {name}."})

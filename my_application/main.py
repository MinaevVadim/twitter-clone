from logging import Logger
from typing import Any, Optional, Coroutine

import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status
from starlette.responses import JSONResponse

import twitter_logging
from config_swagger import tags_metadata

from routers import medias, tweets, users

logger: Logger = twitter_logging.add_logger(__name__)


app: FastAPI = FastAPI(
    title='Corporate microlog service',
    description='Allows users to write short notes and post them;'
                ' each such message can be viewed and commented on in chat mode.',
    openapi_tags=tags_metadata,
)

app.include_router(medias.router)
app.include_router(tweets.router)
app.include_router(users.router)


app.mount('/static', StaticFiles(directory='static'), name='static')

templates: Jinja2Templates = Jinja2Templates(directory='templates')


@app.middleware('http')
async def logger_user(request: Any, call_next: Any) -> Coroutine:
    api_key = request.headers.get('api-key')
    method = request.method
    path = request.url.path
    logger.info(f'User with an * {api_key} * has entered the endpoint {method} {path}')
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    error_dict = exc.errors()[0]
    message, type_error = error_dict['msg'], error_dict['type']
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'result': False, 'type': type_error, 'msg': message}),
    )


@app.get(
    '/',
    response_class=HTMLResponse
)
async def first_endpoint(request: Request) -> Any:
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

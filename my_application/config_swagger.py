from typing import Type

from schemas import ValidatorError, ResponseErrorBase

tags_metadata: list[dict[str, str] | dict[str, str] | dict[str, str]] = [
    {
        "name": "tweets",
        "description": "Operations with tweets.",
    },
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "medias",
        "description": "Operations with medias.",
    },
]


error_response: dict[int, dict[str, Type[ResponseErrorBase]] | dict[
    str, str | Type[ValidatorError]]] = {
    400: {
        'model': ResponseErrorBase,
    },
    422: {
        'model': ValidatorError,
        'description': 'Value Error.',
    }
}

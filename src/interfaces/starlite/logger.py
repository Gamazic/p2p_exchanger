import logging

import httpx
from starlite import LoggingConfig
from starlite.middleware import LoggingMiddlewareConfig
from starlite.response import Response
from starlite.utils import create_exception_response

logging_config = LoggingConfig()

logging_middleware_config = LoggingMiddlewareConfig(logger_name="starlite-app")


def logging_exception_handler(_, exc: Exception) -> Response:
    logging.error("App exc", exc_info=exc)
    return create_exception_response(exc)


async def log_request(request: httpx.Request):
    print(
        f"HTTPX request | {request.method} {request.url} | CONTENT: {request.content!r}"
    )


async def log_response(response: httpx.Response):
    request = response.request
    print(
        f"HTTPX response | {request.method} {request.url} | STATUS {response.status_code}"
    )

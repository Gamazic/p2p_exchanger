import logging
from uuid import uuid4

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
    request_id = str(uuid4())
    request.headers["X-Request-ID"] = request_id
    print(
        f"HTTPX request | ID {request_id} | {request.method} {request.url} | CONTENT: {request.content!r}"
    )


async def log_response(response: httpx.Response):
    request = response.request
    request_id = request.headers["X-Request-ID"]
    print(
        f"HTTPX response | ID {request_id} | {request.method} {request.url} | STATUS {response.status_code}"
    )

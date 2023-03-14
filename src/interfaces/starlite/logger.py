import logging
from uuid import uuid4

import httpx
from starlite import LoggingConfig
from starlite.middleware import LoggingMiddlewareConfig
from starlite.response import Response
from starlite.utils import create_exception_response

__all__ = ["log_request", "log_response", "logging_exception_handler"]


logging_config = LoggingConfig()

logging_middleware_config = LoggingMiddlewareConfig(logger_name="starlite-app")


def logging_exception_handler(_, exc: Exception) -> Response:
    logging.error("App exc", exc_info=exc)
    return create_exception_response(exc)


httpx_logger = logging.getLogger("httpx")


async def log_request(request: httpx.Request):
    request_id = str(uuid4())
    request.headers["X-Request-ID"] = request_id
    httpx_logger.info(
        f"HTTPX request | ID {request_id} | {request.method} {request.url} | CONTENT: {request.content!r}"
    )


async def log_response(response: httpx.Response):
    request = response.request
    request_id = request.headers["X-Request-ID"]
    httpx_logger.info(
        f"HTTPX response | ID {request_id} | {request.method} {request.url} | STATUS {response.status_code}"
    )

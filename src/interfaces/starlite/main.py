from starlite.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from starlite import Starlite, Provide

from src.interfaces.starlite.container import get_exchanger
from src.interfaces.starlite.controllers import ExchangeRateController
from src.interfaces.starlite.logger import logging_config, logging_middleware_config, logging_exception_handler


dependencies = {
    "exchanger_service": Provide(get_exchanger)
}

app = Starlite(
    route_handlers=[ExchangeRateController],
    dependencies=dependencies,
    logging_config=logging_config,
    middleware=[logging_middleware_config.middleware],
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: logging_exception_handler},
    debug=False
)

if __name__ == "__main__":
    # DEBUG
    import uvicorn

    # logging.config.fileConfig()
    uvicorn.run(app, host="0.0.0.0", port=8000)

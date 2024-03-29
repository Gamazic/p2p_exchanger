from starlite import OpenAPIConfig, Provide, Starlite
from starlite.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from src.interfaces.starlite.container import get_exchanger
from src.interfaces.starlite.controllers import ExchangeRateController
from src.interfaces.starlite.logger import logging_config, logging_exception_handler, logging_middleware_config

dependencies = {"exchanger_service": Provide(get_exchanger)}

app = Starlite(
    route_handlers=[ExchangeRateController],
    dependencies=dependencies,
    logging_config=logging_config,
    middleware=[logging_middleware_config.middleware],
    exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: logging_exception_handler},
    debug=False,
    openapi_config=OpenAPIConfig(title="P2P Exchanger Backend", version="0.0.1", root_schema_site="swagger"),
)

if __name__ == "__main__":
    # DEBUG
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

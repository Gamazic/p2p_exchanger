from fastapi import FastAPI

from src.interfaces.fastapi.api import api
from src.interfaces.fastapi.container import fiat_any_crypto_exchanger
from src.services.exchangers import FiatAnyCryptoExchangerService


def create_app() -> FastAPI:
    application = FastAPI()
    application.include_router(api, prefix="/api")
    # application.dependency_overrides[FiatAnyCryptoExchangerService] = fiat_any_crypto_exchanger
    return application


if __name__ == "__main__":
    # DEBUG
    import uvicorn  # type: ignore

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)

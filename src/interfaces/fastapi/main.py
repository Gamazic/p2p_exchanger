from fastapi import FastAPI

from src.interfaces.fastapi.api import api


def create_app() -> FastAPI:
    application = FastAPI()
    application.include_router(api, prefix="/api")
    return application


if __name__ == "__main__":
    # DEBUG
    import uvicorn  # type: ignore

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)

import os

from pydantic import AnyHttpUrl, BaseSettings, PositiveInt

__all__ = ["BotWebhookSettings"]


class BotWebhookSettings(BaseSettings):
    WEBHOOK_HOST: AnyHttpUrl
    WEBHOOK_PATH: str

    WEBAPP_PORT: PositiveInt
    WEBAPP_HOST: str


TG_TOKEN = os.environ["TG_TOKEN"]

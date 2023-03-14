import os

from pydantic import AnyHttpUrl, BaseSettings, PositiveInt


class BotWebhookSettings(BaseSettings):
    WEBHOOK_HOST: AnyHttpUrl
    WEBHOOK_PATH: str

    WEBAPP_PORT: PositiveInt
    WEBAPP_HOST: str


TG_TOKEN = os.environ["TG_TOKEN"]

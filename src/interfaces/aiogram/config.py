import os

from pydantic import AnyHttpUrl, BaseSettings, PositiveInt


class BotWebhookSettings(BaseSettings):
    WEBHOOK_HOST: AnyHttpUrl
    WEBHOOK_PATH: str

    WEBAPP_PORT: PositiveInt
    WEBAPP_HOST: str


class AppSettings(BaseSettings):
    TG_TOKEN: str
    EXCHANGER_API_URL: str

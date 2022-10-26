from pydantic import BaseSettings, FilePath, PositiveInt, AnyHttpUrl, validator


class BotWebhookConfig(BaseSettings):
    WEBHOOK_HOST: AnyHttpUrl
    WEBHOOK_PATH: str

    WEBAPP_PORT: PositiveInt
    WEBAPP_HOST: str

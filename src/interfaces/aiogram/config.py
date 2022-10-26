from pydantic import BaseSettings, FilePath, PositiveInt, AnyHttpUrl, validator


class BotWebhookConfig(BaseSettings):
    WEBHOOK_HOST: AnyHttpUrl
    WEBHOOK_PATH: str
    WEBHOOK_URL: AnyHttpUrl

    @validator("WEBHOOK_URL", pre=True)
    def assemble_webhook_url(cls, v, values):
        host = values["WEBHOOK_HOST"]
        path = values["WEBHOOK_PATH"]
        return f"{host}{path}"

    WEBAPP_PORT: PositiveInt
    WEBAPP_HOST: AnyHttpUrl = AnyHttpUrl("localhost", scheme="http")

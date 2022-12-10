from functools import partial

import typer
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

from src.interfaces.aiogram.config import TG_TOKEN, BotWebhookConfig
from src.interfaces.aiogram.dialog import crypto_dialog
from src.interfaces.aiogram.handlers import exchange, help, start
from src.interfaces.aiogram.middlewares import CustomLoggingMiddleware


def start_polling():
    bot = configure_bot()
    dp = configure_dp(bot)
    executor.start_polling(dp, skip_updates=True, relax=0.1)


def start_webhook():
    bot = configure_bot()
    dp = configure_dp(bot)
    webhook_config = BotWebhookConfig()
    on_startup = partial(on_webhook_startup, webhook_config=webhook_config, bot=bot)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=webhook_config.WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=True,
        host=webhook_config.WEBAPP_HOST,
        port=webhook_config.WEBAPP_PORT,
    )


def configure_bot():
    bot = Bot(token=TG_TOKEN)
    return bot


def configure_dp(bot):
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    registry = DialogRegistry(dp)
    registry.register(crypto_dialog)
    register_handlers(dp)
    dp.middleware.setup(CustomLoggingMiddleware())
    return dp


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(exchange, commands=["exchange"])


async def on_webhook_startup(app, webhook_config: BotWebhookConfig, bot: Bot):
    webhook = await bot.get_webhook_info()
    webhook_url = f"{webhook_config.WEBHOOK_HOST}{webhook_config.WEBHOOK_PATH}"
    if webhook.url != webhook_url:
        if not webhook.url:
            await bot.delete_webhook()

        await bot.set_webhook(webhook_url)


cli = typer.Typer()

cli.command()(start_polling)
cli.command()(start_webhook)


if __name__ == "__main__":
    cli()

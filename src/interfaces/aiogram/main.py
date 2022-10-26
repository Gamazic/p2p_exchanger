import os
import ssl
from functools import partial

import typer
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, DialogRegistry

from src.interfaces.aiogram.dialogs import crypto_dialog, ExchangerSG
from src.interfaces.aiogram.config import BotWebhookConfig


storage = MemoryStorage()
bot = Bot(token=os.environ.get("TG_TOKEN"))
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


registry.register(crypto_dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExchangerSG.source_currency, mode=StartMode.NEW_STACK)


def start_polling():
    executor.start_polling(dp, skip_updates=True, relax=0.1)


def start_webhook():
    webhook_config = BotWebhookConfig()
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(webhook_config.WEBHOOK_SSL_CERT, webhook_config.WEBHOOK_SSL_PRIVATE)
    on_startup = partial(on_webhook_startup, webhook_config=webhook_config)
    executor.start_webhook(dispatcher=dp, webhook_path=webhook_config.WEBHOOK_PATH, on_startup=on_startup,
                           skip_updates=True, host="0.0.0.0", port=webhook_config.WEBAPP_PORT, ssl_context=context)


async def on_webhook_startup(app, webhook_config):
    webhook = await bot.get_webhook_info()

    if webhook.url != webhook_config.WEBHOOK_URL:
        if not webhook.url:
            await bot.delete_webhook()

        await bot.set_webhook(webhook_config.WEBHOOK_URL, certificate=open(webhook_config.WEBHOOK_SSL_CERT, 'rb'))


cli = typer.Typer()

cli.command()(start_polling)
cli.command()(start_webhook)


if __name__ == "__main__":
    cli()

import logging
import os
import sys
from functools import partial

import typer
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogRegistry, StartMode
from aiogram.types import ParseMode

from src.interfaces.aiogram.config import BotWebhookConfig
from src.interfaces.aiogram.dialog import ExchangerSG, crypto_dialog

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
storage = MemoryStorage()
bot = Bot(token=os.environ.get("TG_TOKEN"))
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
registry = DialogRegistry(dp)


registry.register(crypto_dialog)

p2p_instruction_url = "https://www.binance.com/ru/blog/p2p/%D0%B2%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-p2p%D1%82%D0%BE%D1%80%D0%B3%D0%BE%D0%B2%D0%BB%D1%8E-%D1%87%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0%BE%D0%B5-%D1%82%D0%BE%D1%80%D0%B3%D0%BE%D0%B2%D0%BB%D1%8F-peertopeer-%D0%B8-%D0%BA%D0%B0%D0%BA-%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%B0-%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B1%D0%B8%D1%80%D0%B6%D0%B0-421499824684901839"


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await m.answer("Привет! Я покажу по какому курсу можно обменять валюты через P2P сделки.\n\n"
                   "/exchange - Меню обмена\n"
                   "/help - Помощь и инструкция.\n\n"
                   "Информация не является указанием к действиям.")


@dp.message_handler(commands=["help"])
async def help(m: Message, dialog_manager: DialogManager):
    await m.answer("Наша цель - облегчить расчет курса обмена "
                   "валют фиатных валют через P2P сделки.\n\n"
                   "Фиатные валюты, это привычные "
                   "валюты, вроде рублей, долларов, тенге и т.д.\n"
                   f"Подробнее про P2P сделки [см. описание от binance]({p2p_instruction_url})\n\n"
                   "Обмен состоит из двух шагов:\n"
                   "1) Обменять исходную фиатную валюту на какую-то криптовалюту.\n"
                   "2) Обменять полученную криптовалюту на целевую фиатную валюту.\n"
                   "Из этих двух сделок складывается курс обмена.\n\n"
                   "К примеру, Вы хотите обменять рубли на тенге.\n"
                   "Для этого Вы обменяете 60 рублей на криптовалюту USDT через P2P сделку. "
                   "За эту сделку Вы получите примерно 1 USDT.\n"
                   "Далее, Вы обменяете 1 USDT на тенге. За эту сделку Вы получите примерно 420 тенге.\n"
                   "В результате, Вы обменяли рубли на тенге по курс 7 рублей за тенге.\n"
                   "Именно этот курс обмена (7 рублей) и покажет бот.",
                   disable_web_page_preview=True,
                   parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=["exchange"])
async def exchange(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExchangerSG.source_currency, mode=StartMode.NEW_STACK)


@dp.message_handler(commands=["favourites"])
async def favourites(m: Message, dialog_manager: DialogManager):
    await m.answer("Coming soon...")


def start_polling():
    executor.start_polling(dp, skip_updates=True, relax=0.1)


def start_webhook():
    webhook_config = BotWebhookConfig()
    on_startup = partial(on_webhook_startup, webhook_config=webhook_config)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=webhook_config.WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=True,
        host=webhook_config.WEBAPP_HOST,
        port=webhook_config.WEBAPP_PORT,
    )


async def on_webhook_startup(app, webhook_config: BotWebhookConfig):
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

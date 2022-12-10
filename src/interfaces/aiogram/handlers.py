import logging

from aiogram.types import Message, ParseMode
from aiogram_dialog import DialogManager, StartMode

from src.interfaces.aiogram.constants import (COMING_SOON_MESSAGE,
                                              HELP_MESSAGE, START_MESSAGE)
from src.interfaces.aiogram.dialog import ExchangerSG

logger = logging.getLogger("bot")
logging.basicConfig(level=logging.INFO)


async def start(m: Message, dialog_manager: DialogManager):
    await m.answer(START_MESSAGE)


async def help(m: Message, dialog_manager: DialogManager):
    await m.answer(
        HELP_MESSAGE,
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )


async def exchange(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExchangerSG.source_currency, mode=StartMode.NEW_STACK)


async def favourites(m: Message, dialog_manager: DialogManager):
    await m.answer(COMING_SOON_MESSAGE)

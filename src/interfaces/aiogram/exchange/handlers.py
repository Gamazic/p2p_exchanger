from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.interfaces.aiogram.exchange.dialog import ExchangerSG


async def exchange(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExchangerSG.source_currency, mode=StartMode.NEW_STACK)

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.interfaces.aiogram.exchange.dialog import ExchangerSG

__all__ = ["exchange"]


async def exchange(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExchangerSG.source_currency, mode=StartMode.NEW_STACK)

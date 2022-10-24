import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (Dialog, DialogManager, DialogRegistry, StartMode,
                            Window)
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const, Format

from src.domain.fiat import FiatFixedCryptoFilter, FiatParams
from src.interfaces.fastapi.container import (AsyncClient,
                                              FiatFixedCryptoExchangerService,
                                              P2PBinanceApi,
                                              P2PBinanceRepository,
                                              P2PExhcnagerService)
from src.repository.binance_api.models import CryptoCurrency, FiatCurrency

storage = MemoryStorage()
bot = Bot(token=os.environ.get("TG_TOKEN"))
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


client = AsyncClient()
exchanger_service = FiatFixedCryptoExchangerService(
    P2PExhcnagerService(P2PBinanceRepository(P2PBinanceApi(client)))
)


class ExchangerSG(StatesGroup):
    source_currency = State()
    target_currency = State()
    intermediate_crypto = State()
    send_request = State()


class SelectFromEnum(Select):
    def __init__(self, enum, id, when=None):
        text = Format("{item}")
        self.__id = id
        enums = [e.value for e in enum]
        super().__init__(text, id, str, enums, self.__on_click, when)

    async def __on_click(
        self, call: CallbackQuery, select, manager: DialogManager, item: str
    ):
        manager.current_context().dialog_data[self.__id] = item
        await manager.dialog().next()


async def get_result(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().dialog_data
    filter = FiatFixedCryptoFilter.parse_obj(
        dict(
            source_params=FiatParams.parse_obj(
                dict(
                    currency=data["source_currency"],
                    min_amount=0,
                    payments=set(),
                )
            ),
            target_params=FiatParams.parse_obj(
                dict(
                    currency=data["target_currency"],
                    min_amount=0,
                    payments=set(),
                )
            ),
            intermediate_crypto=data["crypto"],
        )
    )
    fiat_order = await exchanger_service.find_best_price(filter)
    return {"price": fiat_order.price}


animals_dialog = Dialog(
    Window(
        Const("Выберите source валюту"),
        SelectFromEnum(FiatCurrency, "source_currency"),
        state=ExchangerSG.source_currency,
    ),
    Window(
        Const("Выберите target валюту"),
        SelectFromEnum(FiatCurrency, "target_currency"),
        state=ExchangerSG.target_currency,
    ),
    Window(
        Const("Выберите crypto валюту"),
        SelectFromEnum(CryptoCurrency, "crypto"),
        state=ExchangerSG.intermediate_crypto,
    ),
    Window(Format("Обмен: {price}"), state=ExchangerSG.send_request, getter=get_result),
)
registry.register(animals_dialog)


@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExchangerSG.source_currency, mode=StartMode.NEW_STACK)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, relax=1)

from enum import Enum

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Group, Multiselect, Next, Select
from aiogram_dialog.widgets.text import Const, Format, Text

from src.domain.fiat import FiatFixedCryptoFilter, FiatParams
from src.interfaces.aiogram.models import (PAYMENTS_CASE, CryptoCurrency,
                                           FiatCurrency)
from src.interfaces.fastapi.container import (AsyncClient,
                                              FiatFixedCryptoExchangerService,
                                              P2PBinanceApi,
                                              P2PBinanceRepository,
                                              P2PExhcnagerService)

client = AsyncClient()
exchanger_service = FiatFixedCryptoExchangerService(
    P2PExhcnagerService(P2PBinanceRepository(P2PBinanceApi(client)))
)


class ExchangerSG(StatesGroup):
    source_currency = State()
    source_payments = State()
    target_currency = State()
    target_payments = State()
    send_request = State()


class SelectFromEnum(Select):
    def __init__(
        self, enum: Enum, widget_id: str, exclude_button_from_id: str | None = None
    ):
        text = Format("{item}")
        items = [e.value for e in enum]
        super().__init__(text, widget_id, str, items, self.__on_click)

        self.items_getter = self.__items_getter
        self.__items = items
        self.__id = widget_id
        self.__exclude_button_from_id = exclude_button_from_id

    def __items_getter(self, data: dict):
        exclude_data = data["dialog_data"].get(self.__exclude_button_from_id, None)
        return (item for item in self.__items if item != exclude_data)

    async def __on_click(
        self, call: CallbackQuery, select, manager: DialogManager, item: str
    ):
        manager.current_context().dialog_data[self.__id] = item
        await manager.dialog().next()


class MultiselectRelatedPayment(Multiselect):
    def __init__(
        self,
        checked_text: Text,
        unchecked_text: Text,
        items: dict,
        widget_id: str,
        related_select_id: str,
    ):
        super().__init__(checked_text, unchecked_text, widget_id, str, items)

        self.__related_select_id = related_select_id
        self.items_getter = self.__items_getter
        self.__items = items
        self.__id = widget_id

    def __items_getter(self, data: dict):
        related_data_selector = data["dialog_data"].get(self.__related_select_id)
        return self.__items[related_data_selector]


async def get_result(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.current_context().dialog_data
    widget_data = dialog_manager.current_context().widget_data
    filter = FiatFixedCryptoFilter.parse_obj(
        dict(
            source_params=FiatParams.parse_obj(
                dict(
                    currency=dialog_data["source_currency"],
                    min_amount=0,
                    payments=set(widget_data["source_payments"]),
                )
            ),
            target_params=FiatParams.parse_obj(
                dict(
                    currency=dialog_data["target_currency"],
                    min_amount=0,
                    payments=set(widget_data["target_payments"]),
                )
            ),
            intermediate_crypto=CryptoCurrency.USDT.value,
        )
    )
    fiat_order = await exchanger_service.find_best_price(filter)
    best_crypto = fiat_order.source_order.target_currency.value
    source_currency = fiat_order.source_order.source_currency
    target_currency = fiat_order.target_order.target_currency
    source_order_url = (
        f"https://p2p.binance.com/ru/trade/all-payments/"
        f"{best_crypto}?fiat="
        f"{source_currency}"
    )
    target_order_url = (
        f"https://p2p.binance.com/ru/trade/sell/"
        f"{best_crypto}?fiat={target_currency}&payment=ALL"
    )
    return {
        "price": fiat_order.price,
        "crypto": best_crypto,
        "source_order_url": source_order_url,
        "target_order_url": target_order_url,
    }


crypto_dialog = Dialog(
    Window(
        Const("Выберите source валюту"),
        SelectFromEnum(FiatCurrency, "source_currency"),
        state=ExchangerSG.source_currency,
    ),
    Window(
        Const("Выберите source способы оплаты"),
        Group(
            MultiselectRelatedPayment(
                Format("+ {item}"),
                Format("{item}"),
                items=PAYMENTS_CASE,
                widget_id="source_payments",
                related_select_id="source_currency",
            ),
            Next(),
        ),
        state=ExchangerSG.source_payments,
    ),
    Window(
        Const("Выберите target валюту"),
        SelectFromEnum(
            FiatCurrency, "target_currency", exclude_button_from_id="source_currency"
        ),
        state=ExchangerSG.target_currency,
    ),
    Window(
        Const("Выберите target способы оплаты"),
        Group(
            MultiselectRelatedPayment(
                Format("+ {item}"),
                Format("{item}"),
                items=PAYMENTS_CASE,
                widget_id="target_payments",
                related_select_id="target_currency",
            ),
            Next(),
        ),
        state=ExchangerSG.target_payments,
    ),
    Window(
        Format(
            "Обмен: {price:.2f}\n"
            "Промежуточная валюта: {crypto}\n"
            "Ссылка на покупку: {source_order_url}\n"
            "Ссылка на продажу: {target_order_url}"
        ),
        state=ExchangerSG.send_request,
        getter=get_result,
    ),
)

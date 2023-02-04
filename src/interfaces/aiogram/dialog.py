from collections import defaultdict
from enum import Enum, EnumType
from typing import Any, Callable
from functools import partial

from emoji import emojize
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Jinja, Multi, Text, Case
from aiogram_dialog.widgets.kbd import Select, Multiselect, Group, Next
from aiogram_dialog.widgets.when import Whenable

from src.domain.fiat import FiatFixedCryptoFilter, FiatParams
from src.interfaces.aiogram.models import (PAYMENTS_CASE, CryptoCurrency,
                                           FiatCurrency, Payment)
from src.interfaces.aiogram.widgets import (RelatedMultiselect, SelectWithExclude)
from src.interfaces.fastapi.container import (AsyncClient,
                                              CachedP2PBinanceRepo,
                                              FiatFixedCryptoExchangerService,
                                              P2PBinanceApi,
                                              P2PExchangerService)


client = AsyncClient()
exchanger_service = FiatFixedCryptoExchangerService(
    P2PExchangerService(CachedP2PBinanceRepo(P2PBinanceApi(client)))
)


class ExchangerSG(StatesGroup):
    source_currency = State()
    source_payments = State()
    target_currency = State()
    target_payments = State()
    send_request = State()


async def save_on_click(
    c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    context = manager.current_context()
    context.dialog_data[widget.widget_id] = item_id
    await manager.dialog().next()


def build_enum_select_widget(enum: EnumType, widget_id: str, exclude_selected_by_id: str | None = None):
    return SelectWithExclude(
        Format("{item}"),
        id=widget_id,
        item_id_getter=str,
        items=list(enum),
        exclude_selected_by_id=exclude_selected_by_id,
        on_click=save_on_click
    )


def build_related_payments_widget(currency_widget_id: str, payments: dict, widget_id: str):
    def selector(data, case, manager):
        selected_data = manager.current_context().widget_data.get(widget_id)
        return 1 if selected_data else 0

    return Group(
        Next(
            Case({0: Const("Любая"), 1: Const("Далее")}, selector=selector)
        ),
        RelatedMultiselect(
            Format("✓ {item}"),
            Format("{item}"),
            widget_id,
            str,
            currency_widget_id,
            payments,
        )
    )


async def get_dialog_data(dialog_manager: DialogManager, **kwargs):
    context = dialog_manager.current_context()
    data = defaultdict(
        None,
        **(context.dialog_data | context.widget_data),
    )
    return data


async def get_result(recover_data: Callable, dialog_manager: DialogManager, **kwargs):
    data = await get_dialog_data(dialog_manager, **kwargs)
    backend_data = recover_data(data)
    filter = FiatFixedCryptoFilter.parse_obj(
        dict(
            source_params=FiatParams.parse_obj(
                dict(
                    currency=backend_data["source_currency"],
                    min_amount=0,
                    payments=set(backend_data["source_payments"]),
                )
            ),
            target_params=FiatParams.parse_obj(
                dict(
                    currency=backend_data["target_currency"],
                    min_amount=0,
                    payments=set(backend_data["target_payments"]),
                )
            ),
            intermediate_crypto=CryptoCurrency.USDT.value,
        )
    )
    fiat_order = await exchanger_service.find_best_price(filter)
    best_crypto = fiat_order.source_order.target_currency.value
    source_currency = fiat_order.source_order.source_currency
    target_currency = fiat_order.target_order.target_currency
    first_source_payment = next(iter(fiat_order.source_order.payments), "all-payments")
    first_target_payment = next(iter(fiat_order.target_order.payments), "ALL")
    source_order_url = (
        f"https://p2p.binance.com/ru/trade/{first_source_payment}/"
        f"{best_crypto}?fiat="
        f"{source_currency}"
    )
    target_order_url = (
        f"https://p2p.binance.com/ru/trade/sell/"
        f"{best_crypto}?fiat={target_currency}&payment={first_target_payment}"
    )
    return {
        "price": fiat_order.price,
        "crypto": best_crypto,
        "source_order_url": source_order_url,
        "target_order_url": target_order_url,
    } | data


def recover_payments(data: dict):
    keys = {
        "source_currency": "source_payments",
        "target_currency": "target_payments"
    }
    copied_data = data.copy()
    for currency_key, payments_key in keys.items():
        selected = copied_data[currency_key]
        payments_map = PAYMENTS_CASE[selected]
        copied_data[payments_key] = [payments_map[payment] for payment in copied_data[payments_key]]
    return copied_data



source_currency_widget = build_enum_select_widget(FiatCurrency, "source_currency")
source_payments_widget = build_related_payments_widget("source_currency", PAYMENTS_CASE, "source_payments")
target_currency_widget = build_enum_select_widget(FiatCurrency, "target_currency",
                                                  exclude_selected_by_id="source_currency")
target_payments_widget = build_related_payments_widget("target_currency", PAYMENTS_CASE, "target_payments")
dialog_template = Jinja(
    """
{% if source_currency %}
Исходная валюта: *{{source_currency}}*
{% endif %}
{% if source_payments %}
Способы оплаты: *{{"*,*".join(source_payments)}}*
{% endif %}
{% if target_currency %}
Целевая валюта: *{{target_currency}}*
{% endif %}
{% if target_payments %}
Способы оплаты: *{{"*,*".join(target_payments)}}*
{% endif %}
"""
)
crypto_dialog = Dialog(
    Window(
        Const(emojize(":up-right_arrow: Выберите исходную валюту")),
        source_currency_widget,
        state=ExchangerSG.source_currency,
        parse_mode=ParseMode.MARKDOWN,
    ),
    Window(
        Multi(
            dialog_template,
            Format("Выберите способы оплаты для *{source_currency}*"),
            # dialog_template
        ),
        source_payments_widget,
        state=ExchangerSG.source_payments,
        parse_mode=ParseMode.MARKDOWN,
        getter=get_dialog_data
    ),
    Window(
        Multi(
            dialog_template,
            Const(emojize(":down-right_arrow: Выберите целевую валюта")),
            # dialog_template
        ),
        target_currency_widget,
        state=ExchangerSG.target_currency,
        parse_mode=ParseMode.MARKDOWN,
        getter=get_dialog_data
    ),
    Window(
        Multi(
            dialog_template,
            Format("Выберите способ оплаты для {target_currency}"),
            # dialog_template
        ),
        target_payments_widget,
        state=ExchangerSG.target_payments,
        parse_mode=ParseMode.MARKDOWN,
        getter=get_dialog_data
    ),
    Window(
        Multi(
            # dialog_template,
            Format("Курс обмена: *{price:.2f}*"),
            dialog_template,
            Format(
                "Промежуточная валюта: *{crypto}*\n"
                "[Ссылка на покупку]({source_order_url})\n"
                "[Ссылка на продажу]({target_order_url})"
            ),
        ),
        parse_mode=ParseMode.MARKDOWN,
        state=ExchangerSG.send_request,
        getter=partial(get_result, recover_payments),
        preview_data={},
        disable_web_page_preview=True,
        )
)

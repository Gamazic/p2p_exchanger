from collections import defaultdict
from functools import partial
from typing import Any, Callable

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ParseMode
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Group, Next
from aiogram_dialog.widgets.text import Case, Const, Format, Jinja, Multi
from emoji import emojize
from httpx import AsyncClient

from src.domain.fiat import FiatFixedCryptoFilter, FiatParams
from src.interfaces.aiogram.exchange.models import FIAT_CURRENCIES, PAYMENTS_CASE
from src.interfaces.aiogram.exchange.widgets import RelatedMultiselect, SelectWithExclude
from src.services.exchangers import P2PExchangerService, FiatFixedCryptoExchangerService
from src.repository.p2p_binance_repo import CachedP2PBinanceRepo
from src.repository.binance_api.p2p_api import P2PBinanceApi

__all__ = [
    "ExchangerSG",
    "build_dict_select_widget",
    "build_related_payments_widget",
    "get_dialog_data",
    "get_result",
    "recover_payments",
    "save_on_click",
]


exchanger_service = FiatFixedCryptoExchangerService(
    P2PExchangerService(CachedP2PBinanceRepo(P2PBinanceApi(AsyncClient())))
)


class ExchangerSG(StatesGroup):
    source_currency = State()
    source_payments = State()
    target_currency = State()
    target_payments = State()
    send_request = State()


async def save_on_click(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    context = manager.current_context()
    context.dialog_data[widget.widget_id] = item_id
    await manager.dialog().next()


def build_dict_select_widget(
    items_map: dict, widget_id: str, exclude_selected_by_id: str | None = None, max_columns: int | None = None
):
    items = list(items_map)
    if max_columns and len(items) > max_columns:
        rows = []
        items_slises = [items[i : i + max_columns] for i in range(0, len(items), max_columns)]
        for slise in items_slises:
            slise_dict = {key: items_map[key] for key in slise}
            row_select = build_dict_select_widget(slise_dict, widget_id, exclude_selected_by_id, None)
            rows.append(row_select)
        return Group(*rows)
    inverse_items_map = {v: k for k, v in items_map.items()}
    return SelectWithExclude(
        Format("{item}"),
        id=widget_id,
        item_id_getter=inverse_items_map.get,
        items=items_map,
        exclude_selected_by_id=exclude_selected_by_id,
        on_click=save_on_click,
    )


def build_related_payments_widget(currency_widget_id: str, payments: dict, widget_id: str):
    def selector(data, case, manager):
        selected_data = manager.current_context().widget_data.get(widget_id)
        return 1 if selected_data else 0

    return Group(
        Next(Case({0: Const("Лю6aя"), 1: Const("Дaлee")}, selector=selector)),
        RelatedMultiselect(
            Format("✓ {item}"),
            Format("{item}"),
            widget_id,
            str,
            currency_widget_id,
            payments,
        ),
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
        {
            "source_params": FiatParams.parse_obj(
                {
                    "currency": backend_data["source_currency"],
                    "min_amount": 0,
                    "payments": set(backend_data["source_payments"]),
                }
            ),
            "target_params": FiatParams.parse_obj(
                {
                    "currency": backend_data["target_currency"],
                    "min_amount": 0,
                    "payments": set(backend_data["target_payments"]),
                }
            ),
            "intermediate_crypto": "USDT",
        }
    )
    fiat_order = await exchanger_service.find_best_price(filter)
    best_crypto = fiat_order.source_order.target_currency.value
    source_currency = fiat_order.source_order.source_currency
    target_currency = fiat_order.target_order.target_currency
    first_source_payment = next(iter(fiat_order.source_order.payments), "all-payments")
    first_target_payment = next(iter(fiat_order.target_order.payments), "ALL")
    source_order_url = (
        f"https://p2p.binance.com/ru/trade/{first_source_payment}/" f"{best_crypto}?fiat=" f"{source_currency}"
    )
    target_order_url = (
        f"https://p2p.binance.com/ru/trade/sell/" f"{best_crypto}?fiat={target_currency}&payment={first_target_payment}"
    )
    return {
        "price": fiat_order.price,
        "crypto": best_crypto,
        "source_order_url": source_order_url,
        "target_order_url": target_order_url,
    } | data


def recover_payments(data: dict):
    keys = {"source_currency": "source_payments", "target_currency": "target_payments"}
    copied_data = data.copy()
    for currency_key, payments_key in keys.items():
        selected = copied_data[currency_key]
        payments_map = PAYMENTS_CASE[selected]
        copied_data[payments_key] = [payments_map[payment] for payment in copied_data[payments_key]]
    return copied_data


source_currency_widget = build_dict_select_widget(FIAT_CURRENCIES, "source_currency", max_columns=4)
source_payments_widget = build_related_payments_widget("source_currency", PAYMENTS_CASE, "source_payments")
target_currency_widget = build_dict_select_widget(
    FIAT_CURRENCIES, "target_currency", exclude_selected_by_id="source_currency", max_columns=4
)
target_payments_widget = build_related_payments_widget("target_currency", PAYMENTS_CASE, "target_payments")
dialog_template = Jinja(
    """
{% if source_currency %}
Иcxoднaя вaлютa: *{{source_currency}}*
{% endif %}
{% if source_payments %}
Cпoco6ы oплaты: *{{"*,*".join(source_payments)}}*
{% endif %}
{% if target_currency %}
Цeлeвaя вaлютa: *{{target_currency}}*
{% endif %}
{% if target_payments %}
Cпoco6ы oплaты: *{{"*,*".join(target_payments)}}*
{% endif %}
"""
)
crypto_dialog = Dialog(
    Window(
        Const(emojize(":up-right_arrow: Bы6epитe иcxoднyю вaлютy")),
        source_currency_widget,
        state=ExchangerSG.source_currency,
        parse_mode=ParseMode.MARKDOWN,
    ),
    Window(
        Multi(
            dialog_template,
            Format("Bы6epитe cпoco6ы oплaты для *{source_currency}*"),
        ),
        source_payments_widget,
        state=ExchangerSG.source_payments,
        parse_mode=ParseMode.MARKDOWN,
        getter=get_dialog_data,
    ),
    Window(
        Multi(
            dialog_template,
            Const(emojize(":down-right_arrow: Bы6epитe цeлeвyю вaлютa")),
        ),
        target_currency_widget,
        state=ExchangerSG.target_currency,
        parse_mode=ParseMode.MARKDOWN,
        getter=get_dialog_data,
    ),
    Window(
        Multi(
            dialog_template,
            Format("Bы6epитe cпoco6 oплaты для {target_currency}"),
        ),
        target_payments_widget,
        state=ExchangerSG.target_payments,
        parse_mode=ParseMode.MARKDOWN,
        getter=get_dialog_data,
    ),
    Window(
        Multi(
            Format("Kypc o6мeнa: *{price:.2f}*"),
            dialog_template,
            Format(
                "Пpoмeжyтoчнaя вaлютa: *{crypto}*\n"
                "[Ccылкa нa пoкyпкy]({source_order_url})\n"
                "[Ccылкa нa пpoдaжy]({target_order_url})"
            ),
        ),
        parse_mode=ParseMode.MARKDOWN,
        state=ExchangerSG.send_request,
        getter=partial(get_result, recover_payments),
        preview_data={},
        disable_web_page_preview=True,
    ),
)

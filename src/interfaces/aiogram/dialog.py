from collections import defaultdict

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Jinja, Multi
from httpx import AsyncClient

from src.interfaces.aiogram.config import AppSettings
from src.interfaces.aiogram.models import (PAYMENTS_CASE,
                                           FiatCurrency)
from src.interfaces.aiogram.remote_service import (ExchangerService,
                                                   SearchFilter)
from src.interfaces.aiogram.widgets import (MultiselectRelatedPayment,
                                            SelectFromEnum)

exchanger_service = ExchangerService(
    AsyncClient(base_url=AppSettings().EXCHANGER_API_URL)
)


class ExchangerSG(StatesGroup):
    source_currency = State()
    source_payments = State()
    target_currency = State()
    target_payments = State()
    send_request = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    return defaultdict(
        None,
        **(
            dialog_manager.current_context().dialog_data
            | dialog_manager.current_context().widget_data
        ),
    )


async def get_result(dialog_manager: DialogManager, **kwargs):
    data = await get_data(dialog_manager, **kwargs)
    source_currency = data["source_currency"]
    target_currency = data["target_currency"]
    # search_filter = {
    #     "source_currency": source_currency,
    #     "target_currency": target_currency,
    #     "intermediate_cryptos": [],
    #     "min_amount": 0,
    #     "source_payments": data["source_payments"],
    #     "target_payments": data["target_payments"],
    # }
    search_filter = SearchFilter(
        source_currency=source_currency,
        target_currency=target_currency,
        intermediate_cryptos=[],
        min_amount=0,
        source_payments=data["source_payments"],
        target_payments=data["target_payments"],
    )
    best_order = await exchanger_service.get_best_exchange_rate(search_filter)
    # fiat_order = await exchanger_service.find_best_price(filter)
    best_crypto = best_order["intermediate_crypto"]
    first_source_payment = next(iter(best_order["source_payments"]), "all-payments")
    first_target_payment = next(iter(best_order["target_payments"]), "ALL")
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
        "price": best_order["exchange_rate"],
        "crypto": best_crypto,
        "source_order_url": source_order_url,
        "target_order_url": target_order_url,
    } | data


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
        Const("Выберите исходную валюту"),
        SelectFromEnum(FiatCurrency, "source_currency"),
        state=ExchangerSG.source_currency,
        parse_mode=ParseMode.MARKDOWN,
    ),
    Window(
        Multi(
            Format("Выберите способы оплаты для *{source_currency}*"), dialog_template
        ),
        MultiselectRelatedPayment(
            Format("✓ {item}"),
            Format("{item}"),
            items=PAYMENTS_CASE,
            widget_id="source_payments",
            related_select_id="source_currency",
        ),
        parse_mode=ParseMode.MARKDOWN,
        state=ExchangerSG.source_payments,
        getter=get_data,
    ),
    Window(
        Multi(Const("Выберите целевую валюта"), dialog_template),
        SelectFromEnum(
            FiatCurrency,
            "target_currency",
            exclude_button_from_id="source_currency",
        ),
        parse_mode=ParseMode.MARKDOWN,
        state=ExchangerSG.target_currency,
        getter=get_data,
    ),
    Window(
        Multi(Format("Выберите способ оплаты для {target_currency}"), dialog_template),
        MultiselectRelatedPayment(
            Format("✓ {item}"),
            Format("{item}"),
            items=PAYMENTS_CASE,
            widget_id="target_payments",
            related_select_id="target_currency",
        ),
        parse_mode=ParseMode.MARKDOWN,
        state=ExchangerSG.target_payments,
        getter=get_data,
    ),
    Window(
        Multi(
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
        getter=get_result,
        preview_data={},
        disable_web_page_preview=True,
    ),
)

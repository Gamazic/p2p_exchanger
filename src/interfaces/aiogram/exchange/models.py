from dataclasses import dataclass

from emoji import emojize


FIAT_CURRENCIES = {
    "RUB": emojize(":Russia:RUB"),
    "KZT": emojize(":Kazakhstan:KZT"),
    "TRY": emojize(":Turkey:TRY"),
    "GEL": emojize(":Georgia:GEL"),
    "EUR": emojize(":European_Union:EUR"),
    "USD": emojize(":United_States:USD"),
    "AED": emojize(":United_Arab_Emirates:AED"),
    "CNY": emojize(":China:CNY")
}

CRYPTO_CURRENCIES = {
    "USDT": "USDT",
    "ETH": "ETH",
    "BTC": "BTC"
}


@dataclass(frozen=True)
class Payment:
    view_name: str
    backend_name: str


RUB_PAYMENTS = {
    "Tinkoff": "TinkoffNew",
    "QIWI": "QIWI",
    "Payeer": "Payeer"
}
KZT_PAYMENTS = {
    "Kaspi": "KaspiBank",
    "Jysan": "JysanBank"
}
TRY_PAYMENTS = {
    "Ziraat": "Ziraat",
    "QNB": "QNB"
}
GEL_PAYMENTS = {
    "Bank Of Georgia": "BankofGeorgia",
    "Liberty": "LIBERTYBANK"
}
EUR_PAYMENTS = {
    "Zen": "Zen",
    "Wise": "Wise"
}
USD_PAYMENTS = {
    "AirTM": "AirTM"
}
AED_PAYMENTS = {
    "ADCB": "ADCB"
}
CNY_PAYMENTS = {
    "Alipay": "Alipay",
    "We Chat": "WeChat"
}

PAYMENTS_CASE = {
    "RUB": RUB_PAYMENTS,
    "KZT": KZT_PAYMENTS,
    "TRY": TRY_PAYMENTS,
    "GEL": GEL_PAYMENTS,
    "EUR": EUR_PAYMENTS,
    "USD": USD_PAYMENTS,
    "AED": AED_PAYMENTS,
    "CNY": CNY_PAYMENTS
}

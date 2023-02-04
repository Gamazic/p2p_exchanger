from dataclasses import dataclass
from enum import StrEnum


# RUB_PAYMENTS = ["TinkoffNew", "QIWI", "Payeer"]
# KZT_PAYMENTS = ["KaspiBank", "JysanBank"]


class FiatCurrency(StrEnum):
    RUB = "RUB"
    KZT = "KZT"
    TRY = "TRY"
    GEL = "GEL"


class CryptoCurrency(StrEnum):
    USDT = "USDT"
    ETH = "ETH"
    BTC = "BTC"


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

PAYMENTS_CASE = {
    FiatCurrency.RUB.value: RUB_PAYMENTS,
    FiatCurrency.KZT.value: KZT_PAYMENTS,
    FiatCurrency.TRY.value: TRY_PAYMENTS,
    FiatCurrency.GEL.value: GEL_PAYMENTS
}

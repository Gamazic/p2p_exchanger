from enum import Enum

RUB_PAYMENTS = ["TinkoffNew", "QIWI", "Payeer"]
KZT_PAYMENTS = ["KaspiBank", "JysanBank"]


class FiatCurrency(Enum):
    RUB = "RUB"
    KZT = "KZT"


class CryptoCurrency(Enum):
    USDT = "USDT"
    ETH = "ETH"
    BTC = "BTC"


PAYMENTS_CASE = {
    FiatCurrency.RUB.value: RUB_PAYMENTS,
    FiatCurrency.KZT.value: KZT_PAYMENTS,
}

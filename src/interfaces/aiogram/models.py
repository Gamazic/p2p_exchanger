from enum import Enum

RU_PAYMENTS = ["TinkoffNew", "QIWI", "Payeer"]
KZT_PAYMENTS = ["KaspiBank"]


class FiatCurrency(Enum):
    RUB = "RUB"
    KZT = "KZT"


class CryptoCurrency(Enum):
    USDT = "USDT"


PAYMENTS_CASE = {
    FiatCurrency.RUB.value: RU_PAYMENTS,
    FiatCurrency.KZT.value: KZT_PAYMENTS,
}

from enum import Enum

RUB_PAYMENTS = ["TinkoffNew", "QIWI", "Payeer"]
KZT_PAYMENTS = ["KaspiBank", "JysanBank"]
TRY_PAYMENTS = ["Ziraat", "QNB"]
GEL_PAYMENTS = ["BankofGeorgia", "LIBERTYBANK", "TBCbank"]


class FiatCurrency(Enum):
    RUB = "RUB"
    KZT = "KZT"
    TRY = "TRY"
    GEL = "GEL"


class CryptoCurrency(Enum):
    USDT = "USDT"
    ETH = "ETH"
    BTC = "BTC"


PAYMENTS_CASE = {
    FiatCurrency.RUB.value: RUB_PAYMENTS,
    FiatCurrency.KZT.value: KZT_PAYMENTS,
    FiatCurrency.TRY.value: TRY_PAYMENTS,
    FiatCurrency.GEL.value: GEL_PAYMENTS,
}
